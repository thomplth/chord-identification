import csv
import os
import numpy as np
from preprocess.note import Note
from preprocess.scale import Scale
from preprocess.chord import Chord, JazzChord
from utility import get_files
from identification.note_to_chord import find_chords


DATA_PATH = "../data"
DATASET_PATH_KEY = "/Schubert_Winterreise_Dataset/localkey-ann"
DATASET_PATH_CHORD = "/Schubert_Winterreise_Dataset/chord"
GT_PATH = DATA_PATH + "/ground_truth"  # "/ground_truth_Schubert"
CHROMA_PATH = DATA_PATH + "/chroma/KYDataset2"  # "/chroma/Schubert2"
TRAINING_DATA_PATH = (
    DATA_PATH + "/SegmentedChroma/KYDataset"
)  # "/SegmentedChroma/Schubert"


def get_Schubert_key(csv_file):
    csv_reader = csv.reader(csv_file, delimiter=";")
    result = {}
    next(csv_reader)  # no need the header
    for row in csv_reader:
        tmp = row[2].split(":")
        scale = (tmp[0], "M" if tmp[1] == "maj" else "m")
        result[float(row[0])] = scale
    return result


def get_chord_info(chord_str):
    def convert_Suchubert(root_str, dataset_form):
        form_dict = {
            "": "",
            "maj": "",
            "min": "m",
            "dim": "dim",
            "aug": "aug",
            "sus4": "",
            "maj6": "",
            "maj7": "maj7",
            "min7": "m7",
            "dim7": "dim7",
            "hdim7": "hdim7",
            "7": "7",
            "9": "7",
        }

        # Actually this can be coded in non-hardcoded way
        interval_dict = {
            "b3": "m3",
            "*3": "M3",  # although mediant is missing, we consider it for chord finding
            "3": "M3",
            "4": "P4",
            "5": "P5",
            "b5": "d5",
            "#5": "A5",
            "6": "M6",
            "#6": "A6",
            "7": "M7",
            "b7": "m7",
            "bb7": "d7",
            "9": "M2",
            "b9": "m2",
        }

        tmp_form = dataset_form.split("(", 1)
        abbr_form = tmp_form[0]
        notes_specified = tmp_form[1][:-1] if len(tmp_form) > 1 else ""
        if len(tmp_form) > 1:
            if abbr_form == "":
                abbr_form = "?"
                notes_str = notes_specified.split(",")
                intervals_str = [interval_dict[n] for n in notes_str]
        if abbr_form in form_dict:
            return form_dict[abbr_form]
        else:
            root = Note(input_str=root_str)
            notes = [root] + [root.get_note_by_interval(i) for i in intervals_str]
            return notes

    shorthand = chord_str.split("/", 1)
    inversion_note_str = shorthand[1] if len(shorthand) > 1 else ""
    jazz_chord = shorthand[0].split(":", 1)
    chord_form = convert_Suchubert(
        jazz_chord[0], jazz_chord[1] if len(jazz_chord) > 1 else ""
    )
    return (jazz_chord[0], chord_form, inversion_note_str)


def get_Schubert_chord(csv_file):

    csv_reader = csv.reader(csv_file, delimiter=";")
    result = {}
    next(csv_reader)  # no need the header
    for row in csv_reader:
        offset = float(row[0])
        root_str, chord_form, inversion_note_str = get_chord_info(row[2])
        # form convertion fail, but notes are caught
        if type(chord_form) == list:
            result[offset] = ("", chord_form, inversion_note_str)
        # form convertion success
        elif type(chord_form) == str:
            _, chord_form_details, _ = get_chord_info(
                row[3]
            )  # in case the chord cannot find
            result[offset] = (
                root_str,
                chord_form,
                inversion_note_str,
                chord_form_details,
            )
    return result


def get_ground_truth(csv_file):
    csv_reader = csv.reader(csv_file, delimiter=",")
    gt_dict = {}
    next(csv_reader)  # no need the header

    # Input lists of chords first
    for row in csv_reader:
        offset, tonic, scale_type, roman_num = row[:4]
        if roman_num == "?":
            continue  # ignore cases that are unknown (cleaner the data)
        tonic_note = Note(input_str=tonic)
        scale = Scale(is_major=scale_type == "M", tonic_note=tonic_note)
        chord = Chord(scale=scale, numeral=roman_num)
        try:
            offset_num = float(offset)
        except:
            # The offset is in fraction
            frac = offset.split("/")
            offset_num = round(float(frac[0]) / float(frac[1]), 6)
        gt_dict[offset_num] = chord

    # Remove duplication
    chord_list = sorted(gt_dict.items(), key=lambda x: x[0])
    dedup_chord_list = [chord_list[0]]
    for idx in range(1, len(chord_list) - 1):
        if not dedup_chord_list[-1][1].is_equal(chord_list[idx][1]):
            dedup_chord_list.append(chord_list[idx])

    return dedup_chord_list


def get_chroma(csv_file):
    csv_reader = csv.reader(csv_file, delimiter=",")
    chroma_dict = {}
    next(csv_reader)  # no need the header

    # Input lists of chroma
    for row in csv_reader:
        offset = float(row[0])
        chroma = np.array([float(val) for val in row[1:]])
        chroma_dict[offset] = chroma

    return sorted(chroma_dict.items(), key=lambda x: x[0])


def ground_truth_exporter(keys_dict, chords_dict, piece_name):
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
        root, form, inversion_note = chord[:3]
        scale = Scale(
            tonic_note=Note(input_str=key_list[key_ptr][1][0]),
            is_major=key_list[key_ptr][1][1] == "M",
        )
        if type(form) == str:
            roman_chord = JazzChord(scale=scale, name=root + form)

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
                roman_chord = JazzChord(scale=scale, name=root + tmp_form)

            if roman_chord.numeral == "?":
                if (
                    scale.tonic.get_note_by_interval("M2").is_equal(
                        Note(input_str=root)
                    )
                    and form == "7"
                    and scale.is_major
                ):
                    roman_chord = Chord(scale=scale, numeral="#IVdim")

            # # If still has problem, then use chord identification to help
            if roman_chord.numeral == "?":
                root = ""
                form = chord[3]
            else:
                writer.writerow(
                    (
                        offset,
                        key_list[key_ptr][1][0],
                        key_list[key_ptr][1][1],
                        roman_chord.numeral,
                    )
                )

        # do the chord identification here
        if type(form) == list:
            notes_freq = [
                (
                    n,
                    0.5 + 0.5 / len(form)
                    if n.__str__() == inversion_note
                    else 0.5 / len(form),
                )
                for n in form
            ]
            chords = find_chords(notes_freq, scale.get_pitch_scale())
            possible_chords_dict = dict(
                [(c["chord"].numeral, c["similarity_score"]) for c in chords]
            )
            chord_candidates = [
                chord
                for chord, value in possible_chords_dict.items()
                if value == max(possible_chords_dict.values())
            ]

            normalize_interval = scale.tonic.get_interval(Note("C", 0))
            basic_interval = scale.tonic.get_interval(form[0])

            if len(chord_candidates) == 0:
                chosen_chord = "?"
                error_counter += 1
                print(scale.__str__(), normalize_interval, "basic", basic_interval)
                # print(
                #     ">>> Null: ",
                #     offset,
                #     "   In C, the notes are:",
                #     [
                #         n.get_note_by_interval(normalize_interval).__str__()
                #         for n in form
                #     ],
                # )
            else:
                chosen_chord = chord_candidates[0]
                if len(chord_candidates) > 1:
                    # expect case 1: if dominant seventh chord & VIIDim7 comes tgt, dominant seventh is the one
                    if "V7" in chord_candidates and "VIIdim7" in chord_candidates:
                        chosen_chord = "V7"
                    elif "V+7" in chord_candidates and "VIIdim7" in chord_candidates:
                        chosen_chord = "V+7"
                    # expect case 2: minor v.s. major traid
                    elif "I" in chord_candidates and "I+" in chord_candidates:
                        chosen_chord = "I"
                    elif "IV" in chord_candidates and "IV+" in chord_candidates:
                        chosen_chord = "IV"
                    elif "V" in chord_candidates and "V+" in chord_candidates:
                        chosen_chord = "V+"
                    # expect case 3: aug v.s. major traid
                    elif "I" in chord_candidates and "Iaug" in chord_candidates:
                        chosen_chord = "I"
                    elif "IV" in chord_candidates and "IVaug" in chord_candidates:
                        chosen_chord = "IV"
                    elif "V" in chord_candidates and "Vaug" in chord_candidates:
                        chosen_chord = "V"
                    # expect case 4: FreVI v.s. GerVI
                    elif "FreVI" in chord_candidates and "GerVI" in chord_candidates:
                        chosen_chord = "GerVI"
                    else:
                        chosen_chord = "/".join(chord_candidates) + "?"
                        error_counter += 1
                        normalize_interval = scale.tonic.get_interval(Note("C", 0))
                        print(
                            scale.__str__(),
                            normalize_interval,
                            "basic",
                            basic_interval,
                        )
                        print(
                            ">>> Many: ",
                            offset,
                            chosen_chord,
                            "   In C, the notes are:",
                            [
                                n.get_note_by_interval(normalize_interval).__str__()
                                for n in form
                            ],
                        )
            writer.writerow(
                (
                    offset,
                    key_list[key_ptr][1][0],
                    key_list[key_ptr][1][1],
                    chosen_chord,
                )
            )

    export_file.close()
    return (len(chord_list), error_counter)


def ground_truth_handler():
    files = get_files(DATA_PATH + DATASET_PATH_KEY, ".csv")
    total_num, total_err = 0, 0
    for f in files:
        print("Now handling:", f)
        gt_key_file = open(DATA_PATH + DATASET_PATH_KEY + "/" + f)
        gt_chord_file = open(DATA_PATH + DATASET_PATH_CHORD + "/" + f)
        with gt_key_file as key_file:
            with gt_chord_file as chord_file:
                keys_dict = get_Schubert_key(key_file)
                chords_dict = get_Schubert_chord(chord_file)
                continue  # Remove this carefully
                num, err = ground_truth_exporter(keys_dict, chords_dict, f)
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


def ground_truth_segment_merger(file_str):
    gt_file = open(GT_PATH + "/" + file_str)
    chord_list = get_ground_truth(gt_file)
    chords_len = len(chord_list)

    chroma_file = open(CHROMA_PATH + "/" + file_str)
    chroma_list = get_chroma(chroma_file)
    chromas_len = len(chroma_list)

    segmented_chroma_dict = {}
    # Handle the case that cannot cover by first chord
    chromas_in_zeroth = [
        chroma for chroma in chroma_list if chroma[0] < chord_list[0][0]
    ]
    if chromas_in_zeroth:
        segmented_chroma_dict[chromas_in_zeroth[0][0]] = {
            "chord": None,
            "chroma": np.sum([c[1] for c in chromas_in_zeroth], axis=0),
        }

    # Handle the rest
    chord_ptr = 0
    chroma_ptr = len(chromas_in_zeroth)
    while (chord_ptr < chords_len) and (chroma_ptr < chromas_len):
        chord_offset = chord_list[chord_ptr][0]
        if chord_offset not in segmented_chroma_dict:
            segmented_chroma_dict[chord_offset] = {
                "chord": chord_list[chord_ptr][1],
                "chroma": np.zeros(13),
            }

        chroma_offset = chroma_list[chroma_ptr][0]
        # print(chord_offset, chroma_offset)
        if (
            chroma_offset > chord_offset
            and chord_ptr < chords_len - 1
            and chroma_offset >= chord_list[chord_ptr + 1][0]
        ):
            chord_ptr += 1
        else:
            segmented_chroma_dict[chord_offset]["chroma"] += chroma_list[chroma_ptr][1]
            chroma_ptr += 1
    chroma_file.close()
    gt_file.close()

    return segmented_chroma_dict


def ground_truth_segmented_exporter(segmented_chroma_dict, file_str):
    path = os.path.join(TRAINING_DATA_PATH, file_str)
    export_file = open(path, "w", newline="")
    writer = csv.writer(export_file)

    header = tuple(
        map(
            str,
            "offset c c# d d# e f f# g g# a a# b total tonic is_major numeral chord_tonality".split(
                " "
            ),
        )
    )
    writer.writerow(header)

    for offset, segment in segmented_chroma_dict.items():
        chroma = segment["chroma"]
        chroma_sum = segment["chroma"][-1]
        normalized_chroma = [0.0 for _ in range(13)]
        if chroma_sum > 0:
            normalized_chroma = [round((val / chroma_sum), 6) for val in chroma]

        chord = segment["chord"]
        chord_tuple = (None, None, None, None)
        if chord:
            chord_tuple = (
                chord.scale.tonic.__str__(),
                chord.scale.is_major,
                chord.numeral,
                chord.form,
            )

        result = tuple([offset]) + tuple(normalized_chroma) + chord_tuple
        writer.writerow(result)


def main():
    gt_files = get_files(GT_PATH, ".csv")
    for f in gt_files:  # TODO: Label error @ 9
        print("Now handling:", f)
        try:
            segmented_chroma_dict = ground_truth_segment_merger(f)
            ground_truth_segmented_exporter(segmented_chroma_dict, f)
        except Exception as e:
            print(e)


main()
# import re


def tavern_handler():
    path = "../data/TAVERN-Beethoven"
    folders = [f for f in os.listdir(path) if f != "combine"]
    for folder in folders[:1]:
        piece_fragments = [f for f in os.listdir(path + "/" + folder)]
        f = open(path + "/combine/" + folder + ".krn", "w")

        frag = piece_fragments[0]
        krn = open(path + "/" + folder + "/" + frag)
        lines = krn.readlines()
        idx = [i for i in range(len(lines)) if lines[i].startswith("=")][0]
        header = lines[:idx]
        idx = [i for i in range(len(header)) if lines[i].startswith("*")][0]
        f.writelines(header[:idx])
        for line in header[idx:]:
            parts = line.split("\t")
            new_line = "{func}\t{notes1}\t{notes2}\t{chord}\n".format(
                func=parts[0],
                notes1=parts[2],
                notes2=parts[3].removesuffix("\n"),
                chord=parts[1],
            )
            f.write(new_line)

        for frag in piece_fragments:
            krn = open(path + "/" + folder + "/" + frag)
            lines = krn.readlines()
            idx = [i for i in range(len(lines)) if lines[i].startswith("=")][0]
            target_lines = lines[idx:-1]
            for l in target_lines:
                new_line = l
                if not l.startswith("="):
                    parts = l.split("\t")
                    new_line = "{func}\t{notes1}\t{notes2}\t{chord}\n".format(
                        func=parts[0],
                        notes1=parts[2],
                        notes2=parts[3].removesuffix("\n"),
                        chord=parts[1],
                    )
                    # print(parts, new_line)
                f.write(new_line)
        f.write("*-\t*-\t*-\t*-\n")
        f.close()
        # TODO: You have to edit the title manually


# from music21 import converter

# f = converter.parse("../data/TAVERN-Beethoven/combine/B063.krn")
# f.show()