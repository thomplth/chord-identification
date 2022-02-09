import time
import configparser
import csv
import os
import traceback

from utility.m21_utility import *

from preprocess.piece import Piece
from segmentation import *
from identification.key_identification import (
    determine_key_by_adjacent,
    determine_key_solo,
)
from identification.note_to_chord import find_chords
from identification.result_combination import *
from evaluation import Metric

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), "config.ini"))

try:
    DATA_PATH = CONFIG["locations"]["data_path"]
    RESULT_PATH = CONFIG["locations"]["result_path"]
    CSV_PATH = CONFIG["locations"]["csv_path"]

    KeyThenChordMode = CONFIG["param"]["KeyThenChord"]
    ExportKey = CONFIG["export"]["keys"]
    ExportChord = CONFIG["export"]["chords"]
except KeyError:
    print("failed to read config.ini, or invalid index specified")
    raise SystemExit

def get_files(filename=None):
    # for x in os.listdir(DATA_PATH):
    #     print(x)
    all_scores = [f for f in os.listdir(DATA_PATH) if f.endswith('.mxl')]
    all_scores.remove(
        "Beethoven_L.V._Sonatina_in_A-Flat_Major_(Op.110_No.31)_2nd_Movement.mxl"
    )
    # RuntimeWarning: invalid value encountered in double_scalars correlation_value = corr_value_numerator / corr_value_denominator
    if filename in all_scores:
        return [filename]
    return all_scores


def export_keys(out_list, dirname, filename):
    path = os.path.join(RESULT_PATH, dirname, filename + ".csv")
    file = open(path, "w", newline="")
    writer = csv.writer(file)

    writer.writerow(('offset', 'key'))

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
                segment["chord"]["chord"],
                segment["chord"]["scale"].scale_str(),
                round(segment["score"], 6),
            )
        )

    file.close()


def main():
    score_files = get_files()
    results = []

    for score_file in score_files:
        try:
            print(">> Currently handling: " + score_file)
            piece = Piece(score_file)
            stream = piece.score
            chordify_stream = piece.chordified
            flatten_stream = piece.flattened

            time_signature = get_initial_time_signature(flatten_stream)
            # key_signature = get_initial_key_signature(flatten_stream) # Scale(key_signature.tonic.name)

            measures_key = determine_key_by_adjacent(key_segmentation(stream))
            # measures_key = determine_key_solo(key_segmentation(stream))

            keys = measures_key

            notes_in_measures = get_notes_in_measures(chordify_stream)
            segments = uniform_segmentation(notes_in_measures, time_signature)
            combined_segments = merge_chord_segment(segments)

            res = []
            for segment in combined_segments:
                notes_frequencies = [
                    (note_input_convertor(note_name), v)
                    for note_name, v in segment[1].items()
                ]
                if KeyThenChordMode:
                    key_choices = find_scale_in_chord_segment(keys, segment)
                    possible_key = max(key_choices, key=key_choices.get)
                    res.append(
                        (segment[0], find_chords(
                            notes_frequencies, possible_key))
                    )
                    if ExportKey:
                        try:
                            key_result = []
                            for offs in res:
                                key_result.append((offs[0], offs[1][0][0]['scale'].scale_str()))
                        except IndexError as ie:
                            pass
                        export_keys(key_result, "keys", score_file.removesuffix(".mxl"))
                else:
                    res.append((segment[0], find_chords(notes_frequencies)))

            if ExportChord:
                chords = res
                if KeyThenChordMode:
                    keys = None
                chord_result = determine_chord(keys=keys, chords=chords)
                export_chords(chord_result, "chords", score_file.removesuffix(".mxl"))

            metric = Metric(piece)
            print(metric.symbolic_recall(chord_result), piece.length)
            # metric.evaluate(key_result, type='key')
            # metric.evaluate(chord_result, type='chord')
            # results.append((score_file, metric))

            raise SystemExit

        except Exception as error:
            traceback.print_exc()

    # for filename, metric in results:
    #     metric.show()


if __name__ == "__main__":
    start_time = time.time()
    # main()
    from preprocess.scale import Scale
    from preprocess.chord import Chord, JazzChord

    g = Scale("G", 0, True)
    # x = Chord(g, numeral="I")
    j = JazzChord(g, "D", "maj7")
    print(j.chord_str())
    print(j.get_jazz_representation())
    print("--- Used %s seconds ---" % (time.time() - start_time))
