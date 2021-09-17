from constant import *
from utility import note_input_convertor

import sys


def chord_picker(tonic, chord, is_major):
    chord_intervals = (
        MAJOR_CHORD_DICTIONARY[chord] if is_major else MINOR_CHORD_DICTIONARY[chord]
    )
    if not is_major:
        pass
    base_note = tonic
    chord_notes = []
    for interval in chord_intervals:
        quality = interval[0]
        distance = int(interval[1])
        next_note = base_note.get_note_by_interval(quality, distance)
        chord_notes.append(next_note)
        base_note = next_note
    return chord_notes


def print_chord(tonic, chord, is_major):
    chord_notes = chord_picker(tonic, chord, is_major)
    print(chord, end=" : ")
    for note in chord_notes:
        print(note.get_note_string(), end=" ")
    print()


def print_all_chords(tonic, is_major):
    chord_dict = MAJOR_CHORD_DICTIONARY if is_major else MINOR_CHORD_DICTIONARY
    for chord, _ in chord_dict.items():
        print_chord(tonic, chord, is_major)


if __name__ == "__main__":
    input_major = sys.argv[1]
    tonic = note_input_convertor(input_major)
    is_major = input_major[0].upper() == input_major[0]
    input_chord = sys.argv[2]
    # print(tonic.get_note_string(), is_major, input_chord)

    if input_chord == "-a":
        print_all_chords(tonic, is_major)
    else:
        print_chord(tonic, input_chord, is_major)