if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from utility.chord_constant import MAJOR_CHORD_DICT, MINOR_CHORD_DICT
from preprocess.note import Note
import time

import sys

# Given the scale and the chord, output the notes of the chord
def pick_chord(tonic, chord, is_major):
    chord_intervals = MAJOR_CHORD_DICT[chord] if is_major else MINOR_CHORD_DICT[chord]
    base_note = tonic
    chord_notes = []
    for interval in chord_intervals:
        next_note = base_note.get_note_by_interval(interval)
        # If you get some strange notes, just DO NOT return that chord
        # if next_note.accidental > 2 or next_note.accidental < -2:
        #     return None
        chord_notes.append(next_note)
        base_note = next_note
    return chord_notes


def print_chord(tonic, chord, is_major):
    chord_notes = pick_chord(tonic, chord, is_major)
    if chord_notes != None:
        print(chord, end=" : ")
        chord_notes_str = [note.__str__() for note in chord_notes]
        print(chord_notes_str)
    else:
        print(
            chord,
            ": unable to print the chord because of there are notes with more than 2 accidentals.",
        )


def print_all_chords(tonic, is_major):
    chord_dict = MAJOR_CHORD_DICT if is_major else MINOR_CHORD_DICT
    for chord, _ in chord_dict.items():
        print_chord(tonic, chord, is_major)


if __name__ == "__main__":
    start_time = time.time()
    input_major = sys.argv[1]
    tonic = Note(input_str=input_major)
    is_major = input_major[0].upper() == input_major[0]
    input_chord = sys.argv[2]
    # print(tonic.__str__(), is_major, input_chord)

    if input_chord == "-a":
        print_all_chords(tonic, is_major)
    else:
        print_chord(tonic, input_chord, is_major)

    # Time calculation
    print(
        "--- Without using music21 library: Used %s seconds ---"
        % (time.time() - start_time)
    )