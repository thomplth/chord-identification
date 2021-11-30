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

directory = "../data/"
KeyThenChordMode = True


def get_files(filename=None):
    all_scores = [f for f in os.listdir(directory) if os.path.isfile(directory + f)]
    all_scores.remove(
        "Beethoven_L.V._Sonatina_in_A-Flat_Major_(Op.110_No.31)_2nd_Movement.mxl"
    )
    # RuntimeWarning: invalid value encountered in double_scalars correlation_value = corr_value_numerator / corr_value_denominator
    if filename in all_scores:
        return [filename]
    return all_scores


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


def main():
    score_files = get_files()  # "Chopin_F._Etude_in_G-Flat_Major,_Op.10_No.5.mxl"

    for score_file in score_files:
        try:
            print(">> Currently handling:" + score_file)
            stream = load_file(directory + score_file)
            chordify_stream = chordify(stream)
            flatten_stream = flatten(stream)

            time_signature = get_initial_time_signature(flatten_stream)
            # print(time_signature)
            # key_signature = get_initial_key_signature(flatten_stream)
            # initial_scale = Scale(key_signature.tonic.name)
            # print("Assume all measures are in ", scale_name)

            if KeyThenChordMode:
                # def get_measures_key():
                measures_key = determine_key_by_adjacent(key_segmentation(stream))
                # measures_key = determine_key_solo(key_segmentation(stream))
                # return measures_key

                keys = measures_key

                # def get_beats_chord():
                # notes_in_measures = get_notes_in_measures(stream)
                notes_in_measures = get_notes_in_measures(chordify_stream)
                segments = uniform_segmentation(notes_in_measures, time_signature)
                combined_segments = merge_chord_segment(segments)

                res = []
                for segment in combined_segments:
                    notes_frequencies = [
                        (note_input_convertor(note_name), v)
                        for note_name, v in segment[1].items()
                    ]
                    key_choices = find_scale_in_chord_segment(keys, segment)
                    possible_key = max(key_choices, key=key_choices.get)
                    res.append(
                        (segment[0], find_chords(notes_frequencies, possible_key))
                    )
                    # print(res)
                    # return res

                chords = res
                keys = None
                result = determine_chord(keys=keys, chords=chords)
                export_csv(result, "result", score_file.removesuffix(".mxl"))

            else:

                def get_measures_key():
                    measures_key = determine_key_by_adjacent(key_segmentation(stream))
                    # measures_key = determine_key_solo(key_segmentation(stream))
                    return measures_key

                keys = get_measures_key()

                def get_beats_chord():
                    # notes_in_measures = get_notes_in_measures(stream)
                    notes_in_measures = get_notes_in_measures(chordify_stream)
                    segments = uniform_segmentation(notes_in_measures, time_signature)
                    combined_segments = merge_chord_segment(segments)

                    res = []
                    for segment in combined_segments:
                        notes_frequencies = [
                            (note_input_convertor(note_name), v)
                            for note_name, v in segment[1].items()
                        ]
                        res.append((segment[0], find_chords(notes_frequencies)))
                    return res

                chords = get_beats_chord()
                result = determine_chord(keys, chords)
                export_csv(result, "result", score_file.removesuffix(".mxl"))

        except Exception as error:
            print(error)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- Used %s seconds ---" % (time.time() - start_time))