from constant import *
from utility import note_input_convertor, invert_interval
import sys
import time

# For a list of notes with length n, output all intervals that between i and (i+1) mod n notes, i.e. the nth/1st notes interval is included
def get_adjacent_intervals(notes):
    notes_num = len(notes)
    res = []
    for i in range(notes_num):
        new_interval = notes[i % notes_num].get_interval(notes[(i + 1) % notes_num])
        res.append(new_interval)
    return res


# find chords
def find_chords(notes_intervals):
    res = []
    for k, v in CHORD_FINDER_DICTIONARY.items():
        chord = list(k)
        # print(chord, v)
        for idx in range(len(notes_intervals) - len(chord) + 1):
            if notes_intervals[idx : idx + len(chord)] == chord:
                res += v
    return res


# print all right pattern
def print_chords_names(possible_chords):
    for ans in possible_chords:
        # print(ans)
        major_interval = invert_interval(ans["tonic_interval"])
        # print(major_interval)
        chord_scale = notes[0].get_note_by_interval(
            major_interval[0], int(major_interval[1])
        )

        scale_str = ""
        is_major = True
        if ans["chord"] in MAJOR_CHORD_DICTIONARY:
            scale_str = chord_scale.note_str()
        else:
            scale_str = chord_scale.get_note_by_interval("M", 6).note_str().lower()
            is_major = False
        # TODO: error when scale = "E-" (scale is not convert to Note object)
        if scale_str == scale or scale == "":
            print(ans["chord"], "in", scale_str, "major" if is_major else "minor")


if __name__ == "__main__":
    # Time calculation
    start_time = time.time()

    # Get input notes and given scale, if any
    input_notes = sys.argv[1:-1]
    scale = sys.argv[-1]

    if scale[0] == "-":
        scale = scale[1:]
    else:
        input_notes.append(scale)
        scale = ""

    # First do sorting
    input_notes.sort()

    notes = [note_input_convertor(note) for note in input_notes]
    notes_intervals = get_adjacent_intervals(notes)

    # search for the right pattern
    possible_chords = find_chords(notes_intervals)
    # print(possible_chords)
    print_chords_names(possible_chords)

    print("--- Used %s seconds ---" % (time.time() - start_time))