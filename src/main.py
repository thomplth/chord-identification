import time
import configparser
import csv
import os

from utility.m21_utility import *

from segmentation import *
from identification.key_identification import (
    determine_key_by_adjacent,
    determine_key_solo,
)
from identification.note_to_chord import find_chords
from identification.result_combination import *


CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), "config.ini"))

INPUT_PATH = CONFIG["locations"]["input_path"]
OUTPUT_PATH = CONFIG["locations"]["output_path"]
CSV_PATH = CONFIG["locations"]["csv_path"]


def main():
    filename = "Beethoven_L.V._Moonlight_Sonata_First_Movement"
    filename = "anonymous_Twinkle_Twinkle"
    stream = load_file("../data/" + filename + ".mxl")
    # filename = "Bartok_B._Sonatina_Movement_1"
    # stream = load_file("../data/testing/" + filename + ".mxl")
    # chordify_stream = chordify(stream)
    flatten_stream = flatten(stream)

    time_signature = get_initial_time_signature(flatten_stream)
    # print(time_signature)
    # key_signature = get_initial_key_signature(flatten_stream)
    # initial_scale = Scale(key_signature.tonic.name)
    # print("Assume all measures are in ", scale_name)

    def get_measures_key():
        measures_key = determine_key_by_adjacent(key_segmentation(stream))
        print("------------")
        print(measures_key)
        measures_key = determine_key_solo(key_segmentation(stream))
        print(measures_key)
        print("------------")
        return measures_key

    keys = get_measures_key()

    def get_beats_chord():
        notes_in_measures = get_notes_in_measures(stream)
        segments = uniform_segmentation(notes_in_measures, time_signature)
        combined_segments = merge_chord_segment(segments)

        res = []
        for segment in combined_segments:
            # print(segment)
            notes_frequencies = [
                (note_input_convertor(note_name), v)
                for note_name, v in segment[1].items()
            ]
            res.append((segment[0], find_chords(notes_frequencies)))
        # print(res)
        return res

    chords = get_beats_chord()
    result = determine_chord(keys, chords)

    # export_file(stream, "../result/Minuet_in_F_C_test")
    # export_file(stream, "../result/anonymous_Twinkle_Twinkle_test")
    # export_file(chordify_stream, "../result/test2")
    export_csv(result, "result", filename)
    # stream.show("text")


def export_csv(out_list, dirname, filename):
    path = os.path.join(CSV_PATH, dirname, filename + ".csv")
    file = open(path, "w", newline="")
    writer = csv.writer(file)

    for segment in out_list:
        writer.writerow(
            (
                segment["offset"],
                segment["chord"]["chord"],
                segment["chord"]["scale"].scale_str(),
                segment["score"],
            )
        )

    file.close()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- Used %s seconds ---" % (time.time() - start_time))