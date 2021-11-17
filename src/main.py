import time
import configparser
import csv
import os

from utility.m21_utility import *

# from utility import note_input_convertor
from segmentation import *
from identification.key_identification import determine_key
from identification.note_to_chord import find_chords, print_chords_names


CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), "config.ini"))

INPUT_PATH = CONFIG["locations"]["input_path"]
OUTPUT_PATH = CONFIG["locations"]["output_path"]
CSV_PATH = CONFIG["locations"]["csv_path"]


def main():
    # stream = load_file("../Gymnopdie_n1_-_E._Satie.mxl")
    # stream = load_file("../Minuet_in_F_C.mxl")
    # filename = "anonymous_Twinkle_Twinkle"
    filename = "Chopin_F._Nocturne_in_E_Minor,_Op.72_No.1"

    stream = load_file("../data/" + filename + ".mxl")
    chordify_stream = chordify(stream)

    time_signature = get_initial_time_signature(chordify_stream)
    key_signature = get_initial_key_signature(chordify_stream)
    # initial_scale = Scale(key_signature.tonic.name)
    # print("Assume all measures are in ", scale_name)

    measures_key = determine_key(key_segmentation(stream))
    # for k, v in measures_key.items():
    #     print(k, v)

    # export_csv(measures_key, "key_segmentations", filename)

    # if True:
    #     segments = uniform_segmentation(chordify_stream, time_signature)
    #     combined_segments = merge_chord_segment(segments)
    #     # print(combined_segments)
    #     for segment in combined_segments[:2]:
    #         notes = [note_input_convertor(note) for note in segment[1]]
    #         result = find_chords(notes)
    #         print(">>>", segment[0], segment[1], notes_variation(segment[1]))
    #         print_chords_names(notes, result, "")

    # export_file(stream, "../result/Minuet_in_F_C_test")
    # export_file(stream, "../result/anonymous_Twinkle_Twinkle_test")
    # export_file(chordify_stream, "../result/test2")


def export_csv(outdict, dirname, filename):
    path = os.path.join(CSV_PATH, dirname, filename + ".csv")
    file = open(path, "w", newline="")
    writer = csv.writer(file)

    for k, v in outdict.items():
        writer.writerow((k, v))

    file.close()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- Used %s seconds ---" % (time.time() - start_time))