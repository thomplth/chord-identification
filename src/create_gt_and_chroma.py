import time
import configparser
import csv
import os
import traceback


from utility.m21_utility import *
from utility import get_files

from preprocess.piece import Piece
from preprocess.note import Note
from segmentation import *
from identification.result_combination import *

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), "config.ini"))

try:
    DATA_PATH = CONFIG["locations"]["data_path"]
    DATASET_PATH = CONFIG["locations"]["dataset_path"]
    RESULT_PATH = CONFIG["locations"]["result_path"]
    CSV_PATH = CONFIG["locations"]["csv_path"]

    KeyThenChordMode = CONFIG["param"]["KeyThenChord"]
    ExportKey = CONFIG["export"]["keys"]
    ExportChord = CONFIG["export"]["chords"]
except KeyError:
    print("failed to read config.ini, or invalid index specified")
    raise SystemExit


def export_keys(out_list, dirname, filename):
    path = os.path.join(RESULT_PATH, dirname, filename + ".csv")
    file = open(path, "w", newline="")
    writer = csv.writer(file)

    writer.writerow(("offset", "key"))

    for el in out_list:
        writer.writerow((el[0], el[1]))

    file.close()


def export_chords(out_list, dirname, filename):
    path = os.path.join(RESULT_PATH, dirname, filename + ".csv")
    file = open(path, "w", newline="")
    writer = csv.writer(file)

    for segment in out_list:
        writer.writerow(
            (
                segment["offset"],
                segment["chord"].numeral,
                segment["chord"].scale.__str__(),
                round(segment["score"], 6),
            )
        )

    file.close()


def export_chromas(out_list, dirname, filename):
    path = os.path.join("../data/chroma" + dirname, filename + ".csv")
    file = open(path, "w", newline="")
    writer = csv.writer(file)

    header = tuple(map(str, "offset c c# d d# e f f# g g# a a# b total".split(" ")))
    writer.writerow(header)
    for segment in out_list:
        chroma: list[float] = [0.0 for _ in range(13)]  # the last one store total
        for note, duration in segment["note_profile"].items():
            pitch = Note(input_str=note).get_pitch_class()
            chroma[pitch] += duration
            chroma[12] += duration
        chroma = [round(dur, 3) for dur in chroma]

        result = tuple([segment["offset"]]) + tuple(chroma)
        writer.writerow(result)

    file.close()


def main():
    score_files = get_files(
        DATA_PATH + DATASET_PATH,
        (".mxl", ".xml"),
        "Mendelsshon_F._Songs_Without_Words_(Op._19_No._6).mxl",
    )

    for score_file in score_files:
        try:
            print(">> Currently handling: " + score_file)
            piece = Piece(score_file)
            piece._export_ground_truth()

            stream = piece.score
            segment_unit = get_segment_unit(stream)
            notes_in_measures = get_notes_in_segments(piece.chordified, segment_unit)
            beat_segments = generate_note_profiles_in_segments(notes_in_measures)
            export_chromas(beat_segments, DATASET_PATH, score_file[:-4])
        except Exception as error:
            traceback.print_exc()

    # for filename, metric in results:
    #     metric.show()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- Used %s seconds ---" % (time.time() - start_time))