import csv
import os
from pydoc import doc
import numpy as np
from preprocess.note import Note
from preprocess.scale import Scale
from preprocess.chord import Chord, JazzChord
from utility import get_files
from identification.note_to_chord import find_chords
from itertools import combinations, product
from preprocess.piece import Piece
import re

DATA_PATH = "../data/ABC"
MAIN_ANNO_PATH = DATA_PATH + "/index_annotations.csv"
GT_PATH = "../data//ground_truth/ABC"
dataset = get_files(DATA_PATH, ".mxl")

main_file = open(MAIN_ANNO_PATH, "r", encoding="utf-8-sig")
reader = csv.DictReader(main_file)
# print(reader.fieldnames)
keys_to_extract = ["chord", "totbeat", "global_key", "is_major", "unified_chord"]
piece_code_header = ["op", "no", "mov"]


def ground_truth_handler():
    file_dict = {}
    for row in reader:
        piece_code = tuple(row[key] for key in piece_code_header)
        if not piece_code in file_dict:
            file_dict[piece_code] = []
        gt = {key: row[key] for key in keys_to_extract}
        file_dict[piece_code].append(gt)

    for code, gt in file_dict.items():
        gt = sorted(gt, key=lambda f: float(f["totbeat"]))
        file_dict[code] = gt

    return file_dict


def ground_truth_exporter(file_dict):
    for k, v in file_dict.items():
        path = os.path.join(GT_PATH, f"op{k[0]}_no{k[1]}_mov{k[2]}.csv")
        export_file = open(path, "w", newline="")
        writer = csv.writer(export_file)
        header = tuple(["offset", "tonic", "key", "numeral"])  # , "original_chord"
        writer.writerow(header)

        for segment in v:
            truth = tuple(
                [
                    segment["totbeat"],
                    segment["global_key"],
                    "M" if segment["is_major"] == "TRUE" else "m",
                    segment["unified_chord"],
                    # segment["chord"],
                ]
            )
            writer.writerow(truth)


file_dict = ground_truth_handler()
ground_truth_exporter(file_dict)
# for data in dataset:
#     name = re.search("op[0-9].*mov[0-9]", data)  # shd work
#     name = name.group(0)
#     piece_code = re.split("_", name)
#     op = int(piece_code[0][2:])
#     no = int(piece_code[1][2:])
#     mov = int(piece_code[2][3:])
#     print(op, no, mov)
