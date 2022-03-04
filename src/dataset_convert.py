import configparser
import csv
import os
from preprocess.note import Note
from preprocess.scale import Scale
from preprocess.chord import JazzChord

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), "config_data_convert.ini"))
try:
    DATA_PATH = CONFIG["locations"]["data_path"]
    DATASET_PATH_KEY = CONFIG["locations"]["dataset_key_path"]
    DATASET_PATH_CHORD = CONFIG["locations"]["dataset_chord_path"]
    GT_PATH = CONFIG["locations"]["gt_path"]
except KeyError:
    print("failed to read config.ini, or invalid index specified")
    raise SystemExit


def get_files():
    all_scores = [
        f for f in os.listdir(DATA_PATH + DATASET_PATH_KEY) if f.endswith(".csv")
    ]
    # print(all_scores)
    return all_scores


def get_Schubert_key(csv_file):
    csv_reader = csv.reader(csv_file, delimiter=";")
    result = {}
    next(csv_reader)  # no need the header
    for row in csv_reader:
        tmp = row[2].split(":")
        scale = (tmp[0], "M" if tmp[1] == "maj" else "m")
        result[float(row[0])] = scale
    return result


def get_Schubert_chord(csv_file):
    def convert_form_Suchubert(dataset_form):
        convert_dict = {"": ""}
        convert_dict["min"] = "m"
        convert_dict["dim"] = "dim"
        convert_dict["7"] = "7"
        convert_dict["maj7"] = "maj7"
        convert_dict["min7"] = "m7"
        convert_dict["dim7"] = "o7"
        convert_dict["hdim7"] = "%7"

        standard_abbr = convert_dict[dataset_form]
        return standard_abbr

    csv_reader = csv.reader(csv_file, delimiter=";")
    result = {}
    next(csv_reader)  # no need the header
    for row in csv_reader:
        shorthand = row[2].split("/", 1)
        jazz_chord = shorthand[0].split(":", 1)
        chord_form = convert_form_Suchubert(
            jazz_chord[1] if len(jazz_chord) > 1 else ""
        )
        result[float(row[0])] = jazz_chord[0] + chord_form
    return result


def exporter(keys_dict, chords_dict, piece_name):
    path = os.path.join(GT_PATH, piece_name)
    export_file = open(path, "w", newline="")
    writer = csv.writer(export_file)
    writer.writerow(("offset", "tonic", "key", "numeral"))

    key_list = sorted(keys_dict.items(), key=lambda x: x[0])
    chord_list = sorted(chords_dict.items(), key=lambda x: x[0])
    key_ptr = 0
    for offset, chord in chord_list:
        if key_ptr < len(key_list) - 1 and key_list[key_ptr + 1][0] <= offset:
            key_ptr += 1

        scale = Scale(
            tonic_note=Note(input_str=key_list[key_ptr][1][0]),
            is_major=key_list[key_ptr][1][1] == "M",
        )
        roman_chord = JazzChord(scale=scale, name=chord)
        print(
            offset,
            key_list[key_ptr][1][0],
            key_list[key_ptr][1][1],
            roman_chord.numeral,
        )
        writer.writerow(
            (
                offset,
                key_list[key_ptr][1][0],
                key_list[key_ptr][1][1],
                roman_chord.numeral,
            )
        )
    export_file.close()


files = get_files()
for f in files[:1]:
    print(f)
    gt_key_file = open(DATA_PATH + DATASET_PATH_KEY + "/" + f)
    gt_chord_file = open(DATA_PATH + DATASET_PATH_CHORD + "/" + f)
    with gt_key_file as key_file:
        with gt_chord_file as chord_file:
            keys_dict = get_Schubert_key(key_file)
            chords_dict = get_Schubert_chord(chord_file)
            exporter(keys_dict, chords_dict, f)
    gt_key_file.close()
    gt_chord_file.close()
