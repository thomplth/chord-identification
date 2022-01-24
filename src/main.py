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

DATA_PATH = CONFIG["locations"]["data_path"]
RESULT_PATH = CONFIG["locations"]["result_path"]
CSV_PATH = CONFIG["locations"]["csv_path"]
KeyThenChordMode = CONFIG["param"]["KeyThenChord"]


def get_files(filename=None):
    all_scores = [f for f in os.listdir(DATA_PATH) if os.path.isfile(DATA_PATH + f)]
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
    score_files = get_files()  #

    for score_file in score_files:
        try:
            print(">> Currently handling:" + score_file)
            stream = load_file(DATA_PATH + score_file)
            chordify_stream = chordify(stream)
            flatten_stream = flatten(stream)

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
                        (segment[0], find_chords(notes_frequencies, possible_key))
                    )
                else:
                    res.append((segment[0], find_chords(notes_frequencies)))
            # print(res)

            chords = res
            if KeyThenChordMode:
                keys = None
            result = determine_chord(keys=keys, chords=chords)
            export_csv(result, "result", score_file.removesuffix(".mxl"))

        except Exception as error:
            print(error)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- Used %s seconds ---" % (time.time() - start_time))
