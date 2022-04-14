import time
import configparser
import csv
import os
import traceback


from itertools import zip_longest

from utility.m21_utility import *
from utility import get_files

from preprocess.piece import Piece
from preprocess.note import Note
from preprocess.scale import Scale
from segmentation import *
from identification.key_identification import determine_key_by_adjacent

from identification.note_to_chord import find_chords
from identification.result_combination import *
from evaluation import Metric

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), "config.ini"))


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


try:
    DATA_PATH = CONFIG["locations"]["data_path"]
    DATA_SCORE_PATH = CONFIG["locations"]["testing_data_path"]
    DATA_CHROMA_PATH = CONFIG["locations"]["testing_chroma_path"]
    RESULT_PATH = CONFIG["locations"]["result_path"]
    CSV_PATH = CONFIG["locations"]["csv_path"]
    KeyThenChordMode = CONFIG["param"]["KeyThenChord"] == "True"
    DTRFMode = CONFIG["param"]["UsingDTRF"] == "True"
    MODEL_PATH = CONFIG["locations"]["ml_path"]
    ExportKey = CONFIG["export"]["keys"]
    ExportChord = CONFIG["export"]["chords"]

except KeyError:
    print("failed to read config.ini, or invalid index specified")
    raise SystemExit

from joblib import load
import warnings


def load_model(dir: str):
    try:
        model = load(dir)
        return model
    except Exception as error:
        print(error)


def main():
    score_files = get_files(DATA_PATH + DATA_SCORE_PATH, (".mxl", ".xml"))
    warnings.filterwarnings("ignore")
    segmentation_models = None
    identification_models = None
    if DTRFMode:
        segmentation_models = [
            load_model("./model/segmentation/decision_tree_12.joblib"),
            load_model("./model/segmentation/random_forest_12.joblib"),
        ]
        identification_models = [
            load_model("./model/identification/decision_tree.joblib"),
            load_model("./model/identification/random_forest.joblib"),
        ]

    for score_file in score_files[1:2]:
        try:
            print(">> Currently handling: " + score_file)
            piece = Piece(score_file)
            stream = piece.score
            chordify_stream = piece.chordified
            # initial_key = get_initial_key_signature(chordify_stream)
            # initial_scale = Scale(
            #     tonic_note=Note(input_str=initial_key.tonic.name),
            #     is_major=initial_key.type == "major",
            # )

            # chord segmentation (in notes profile)
            segment_unit = get_segment_unit(stream)
            notes_in_measures = get_notes_in_segments(chordify_stream, segment_unit)
            note_profile_segments = generate_note_profiles_in_segments(
                notes_in_measures
            )
            combined_segments = merge_chord_segment(
                note_profile_segments, models=segmentation_models
            )

            def convert_offsetNoteProfile_to_offsetChroma(offset_note_profile):
                offset = offset_note_profile["offset"]
                note_profile = offset_note_profile["note_profile"]

                chroma: list[float] = [0.0 for _ in range(12)]
                for note, duration in note_profile.items():
                    pitch = Note(input_str=note).get_pitch_class()
                    chroma[pitch] += duration
                chroma = [round(dur, 6) for dur in chroma]

                result = {"chroma": chroma, "offset": offset}
                return result

            # key identification
            segmented_chroma_dict: Measure_OffsetChroma_dict = {}
            for idx in range(len(combined_segments)):
                offset_note_profile = combined_segments[idx]
                # the measure number is replaced by the index of chromas
                segmented_chroma_dict[idx] = convert_offsetNoteProfile_to_offsetChroma(
                    offset_note_profile
                )
            measures_key = determine_key_by_adjacent(segmented_chroma_dict)

            # Chord identification
            offset_chord_choices = []
            for segment in combined_segments:
                notes_frequencies = [
                    (Note(input_str=note_name), value)
                    for note_name, value in segment["note_profile"].items()
                ]
                if KeyThenChordMode:
                    key_choices = find_scale_in_chord_segment(measures_key, segment)
                    possible_key = max(key_choices, key=key_choices.get)
                    possible_chords = find_chords(notes_frequencies, possible_key)
                else:
                    possible_chords = find_chords(notes_frequencies)
                offset_chord_choices.append(
                    {"offset": segment["offset"], "chords": possible_chords}
                )

            chord_result = determine_chord(
                keys=measures_key,
                chords=offset_chord_choices,
                determine_mode=KeyThenChordMode,
            )

            if ExportKey:
                key_result = []
                for offs in chord_result:
                    if len(key_result) > 0:
                        original_scale = key_result[-1][1]
                        scale_equal = original_scale == offs["chord"].scale.__str__()

                    if len(key_result) == 0 or (not scale_equal):
                        key_result.append(
                            (
                                offs["offset"],
                                offs["chord"].scale.__str__(),
                            )
                        )
                export_keys(key_result, "keys", score_file.removesuffix(".mxl"))
            if ExportChord:
                merged_chord_result = []
                for chord_pack in chord_result:
                    if len(merged_chord_result) > 0:
                        original_chord = merged_chord_result[-1]["chord"]
                        new_chord = chord_pack["chord"]
                        chord_equal = original_chord.is_equal(new_chord)

                    if len(merged_chord_result) == 0 or (not chord_equal):
                        merged_chord_result.append(chord_pack)
                export_chords(
                    merged_chord_result, "chords", score_file.removesuffix(".mxl")
                )

            # raise SystemExit

        except Exception as error:
            traceback.print_exc()

    # for filename, metric in results:
    #     metric.show()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- Used %s seconds ---" % (time.time() - start_time))
