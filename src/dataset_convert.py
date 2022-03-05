import configparser
import csv
import os
from preprocess.note import Note
from preprocess.scale import Scale
from preprocess.chord import Chord, JazzChord

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
        convert_dict["maj"] = ""
        convert_dict["min"] = "m"
        convert_dict["dim"] = "dim"
        convert_dict["aug"] = "aug"
        convert_dict["sus4"] = ""
        convert_dict["maj6"] = ""
        convert_dict["7"] = "7"
        convert_dict["9"] = "7"
        convert_dict["maj7"] = "maj7"
        convert_dict["min7"] = "m7"
        convert_dict["dim7"] = "dim7"
        convert_dict["hdim7"] = "hdim7"
        convert_dict["It"] = "It"
        convert_dict["Ger"] = "Ger"
        convert_dict["Fr"] = "Fr"

        tmp_form = dataset_form.split("(", 1)
        abbr_form = tmp_form[0]
        notes_specified = tmp_form[1][:-1] if len(tmp_form) > 1 else ""
        if len(tmp_form) > 1:
            if abbr_form == "":
                notes = notes_specified.split(",")
            #     check_notes = ["b3", "3", "b5", "5", "bb7", "b7", "7"]
            #     is_in_notes = [n in notes for n in check_notes]
            #     if is_in_notes[1] and is_in_notes[3] and is_in_notes[6]:
            #         abbr_form = "maj7"
            #     elif is_in_notes[0] and is_in_notes[3] and is_in_notes[5]:
            #         abbr_form = "min7"
            #     elif is_in_notes[1] and is_in_notes[3] and is_in_notes[5]:
            #         abbr_form = "7"
            #     elif is_in_notes[0] and is_in_notes[2] and is_in_notes[4]:
            #         abbr_form = "dim7"
            #     elif is_in_notes[0] and is_in_notes[2] and is_in_notes[5]:
            #         abbr_form = "hdim7"
            #     elif is_in_notes[1] and is_in_notes[2] and is_in_notes[5]:
            #         abbr_form = "Fr"
            #     elif is_in_notes[1] and is_in_notes[2] and "b9" in notes:
            #         abbr_form = "Fr"
            #     elif is_in_notes[1] and is_in_notes[3] and "#6" in notes:
            #         abbr_form = "Ger"
            #     elif is_in_notes[1] and "#6" in notes:
            #         abbr_form = "It"

            #     if abbr_form == "":
            #         if is_in_notes[1] and is_in_notes[3]:
            #             abbr_form = "maj"
            #         elif is_in_notes[0] and is_in_notes[3]:
            #             abbr_form = "m"
            #         elif is_in_notes[0] and is_in_notes[2]:
            #             abbr_form = "dim"
            #         elif is_in_notes[1] and "#5" in notes:
            #             abbr_form = "aug"
            #         elif is_in_notes[2] and is_in_notes[5]:
            #             abbr_form = "hdim7"
            # if abbr_form == "":
            #     print(row[0], notes)

        standard_abbr = convert_dict[abbr_form]
        return standard_abbr

    csv_reader = csv.reader(csv_file, delimiter=";")
    result = {}
    next(csv_reader)  # no need the header
    for row in csv_reader:
        shorthand = row[2].split("/", 1)
        inversion_note = shorthand[1] if len(shorthand) > 1 else ""
        jazz_chord = shorthand[0].split(":", 1)
        chord_form = convert_form_Suchubert(
            jazz_chord[1] if len(jazz_chord) > 1 else ""
        )
        result[float(row[0])] = (jazz_chord[0], chord_form, inversion_note)
    return result


def exporter(keys_dict, chords_dict, piece_name):
    path = os.path.join(GT_PATH, piece_name)
    export_file = open(path, "w", newline="")
    writer = csv.writer(export_file)
    writer.writerow(("offset", "tonic", "key", "numeral"))

    key_list = sorted(keys_dict.items(), key=lambda x: x[0])
    chord_list = sorted(chords_dict.items(), key=lambda x: x[0])
    key_ptr = 0
    error_counter = 0

    for offset, chord in chord_list:
        if key_ptr < len(key_list) - 1 and key_list[key_ptr + 1][0] <= offset:
            key_ptr += 1
        tonic, form, inversion_note = chord
        scale = Scale(
            tonic_note=Note(input_str=key_list[key_ptr][1][0]),
            is_major=key_list[key_ptr][1][1] == "M",
        )
        roman_chord = JazzChord(scale=scale, name=tonic + form)

        # if the chord is seventh and it cannot be recognized,
        # remove the seventh note
        if roman_chord.numeral == "?":
            tmp_form = ""
            if form == "7" or form == "maj7":
                tmp_form = ""
            elif form == "m7":
                tmp_form = "m"
            elif form == "dim7" or form == "hdim7":
                tmp_form = "dim"
            roman_chord = JazzChord(scale=scale, name=tonic + tmp_form)

        # If still has problem, then it maybe common-tone chords
        if roman_chord.numeral == "?":
            if (
                scale.tonic.get_note_by_interval("M2").is_equal(Note(input_str=tonic))
                and form == "7"
            ):
                roman_chord = Chord(scale=scale, numeral="#IVdim")

        if roman_chord.numeral == "?":
            print(">>>", offset, key_list[key_ptr][1], tonic, chord)
            error_counter += 1
        writer.writerow(
            (
                offset,
                key_list[key_ptr][1][0],
                key_list[key_ptr][1][1],
                roman_chord.numeral,
            )
        )
    export_file.close()
    print("*********************")
    return (len(chord_list), error_counter)


files = get_files()
total_num, total_err = 0, 0
for f in files:
    print("Now handling:", f)
    gt_key_file = open(DATA_PATH + DATASET_PATH_KEY + "/" + f)
    gt_chord_file = open(DATA_PATH + DATASET_PATH_CHORD + "/" + f)
    with gt_key_file as key_file:
        with gt_chord_file as chord_file:
            keys_dict = get_Schubert_key(key_file)
            chords_dict = get_Schubert_chord(chord_file)
            num, err = exporter(keys_dict, chords_dict, f)
            total_num += num
            total_err += err

    gt_key_file.close()
    gt_chord_file.close()

print("Total chords:", total_num)
print(
    "Error:",
    total_err,
    "and the Convert Rate:",
    (total_num - total_err) / total_num,
)
