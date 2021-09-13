from constant import *
from scale_generator import note_input_convertor
import sys


if __name__ == "__main__":
    input_notes = sys.argv[1:-1]
    major = sys.argv[-1]

    if major[0] == "-":
        major = major[1:]
    else:
        input_notes.append(major)
        major = ""

    input_notes.sort()

    notes = [note_input_convertor(note) for note in input_notes]
    notes_num = len(notes)
    for i in range(notes_num):
        print(notes[i % notes_num].get_interval(notes[(i + 1) % notes_num]))
    print(major)