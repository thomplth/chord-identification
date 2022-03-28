"This files is currently useless."
import music21 as m21
from utility.m21_utility import get_notes_in_measures
import os


def get_files(diretory):
    all_scores = [f for f in os.listdir(diretory) if f.endswith(".krn")]
    return all_scores


def openFile(file_name: str):
    return m21.converter.parse(file_name)


# f = openFile("B063_00_01a_a.hrm")
if 1:
    directory = "..\data\TAVERN-Beethoven\B063"
    scores = get_files(directory)
    for s in scores[:1]:
        file_dir = directory + "\\" + s
        f = openFile(file_dir)
        f.show("text")
        # notes = get_notes_in_measures(f)
    # f.humdrum.spineParser.HarmSpine()
