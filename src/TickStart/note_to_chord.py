from constant import *
from utility import note_input_convertor, invert_interval
import sys


def get_intervals_between_notes(notes):
    notes_num = len(notes)
    res = []
    for i in range(notes_num):
        new_interval = notes[i % notes_num].get_interval(notes[(i + 1) % notes_num])
        res.append(new_interval)
    print(res)
    return res


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
    notes_interval = get_intervals_between_notes(notes)
    print(major)

    res = []
    for k, v in CHORD_FINDER_DICTIONARY.items():
        chord = list(k)
        # print(chord, v)
        for idx in range(len(notes_interval) - len(chord) + 1):
            if notes_interval[idx : idx + len(chord)] == chord:
                res.append(v)
    print(res)
    for pattern in res:
        for ans in pattern:
            # print(ans)
            major_interval = invert_interval(ans["tonic_interval"])
            # print(major_interval)
            major = notes[0].get_note_by_interval(
                major_interval[0], int(major_interval[1])
            )
            print(ans["chord"], "in", major.get_note_string(), "major")