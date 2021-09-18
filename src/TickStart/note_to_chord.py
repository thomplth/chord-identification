from constant import *
from utility import note_input_convertor, invert_interval
from chord_to_note import pick_chord, print_chord
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


def search_chord_dictionary(first_note, target):
    res = []

    def search_in_one_dictionary(is_major):
        dictionary = (
            MAJOR_CHORD_FINDER_DICTIONARY if is_major else MINOR_CHORD_FINDER_DICTIONARY
        )
        for k, v in dictionary.items():
            chord = list(k)
            if chord[0 : len(target)] == target:
                for option in v:
                    tonic_interval = invert_interval(option["tonic_interval"])
                    res.append(
                        {
                            "chord": option["chord"],
                            "scale": first_note.get_note_by_interval(
                                tonic_interval[0],
                                int(tonic_interval[1]),
                            ),
                            "is_major": is_major,
                        }
                    )

    search_in_one_dictionary(True)
    search_in_one_dictionary(False)
    return res


# find chords
def find_chords_two_notes(notes, notes_intervals):
    # print(notes, notes_intervals)
    res = []
    for idx in range(len(notes_intervals)):
        interval = notes_intervals[idx]
        if interval == "M3":
            res += search_chord_dictionary(notes[idx], [interval])
        elif interval == "m3":
            res += search_chord_dictionary(notes[idx], [interval])
        elif interval == "M2":
            res.append({"chord": "FrVI", "scale": notes[idx], "is_major": True})
            res.append({"chord": "FrVI", "scale": notes[idx], "is_major": False})
        elif interval == "A2":
            res.append({"chord": "GerVI", "scale": notes[idx], "is_major": True})
            res.append({"chord": "GerVI", "scale": notes[idx], "is_major": False})
        elif interval == "A4":
            res.append({"chord": "GerVI", "scale": notes[idx], "is_major": True})
            res.append({"chord": "GerVI", "scale": notes[idx], "is_major": False})
            res.append({"chord": "FrVI", "scale": notes[idx], "is_major": True})
            res.append({"chord": "FrVI", "scale": notes[idx], "is_major": False})
            res.append({"chord": "ItVI", "scale": notes[idx], "is_major": True})
            res.append({"chord": "ItVI", "scale": notes[idx], "is_major": False})
        elif interval == "d5":
            res += search_chord_dictionary(notes[idx], ["m3", "m3"])
        elif interval == "P5":
            res += search_chord_dictionary(notes[idx], ["M3", "m3"])
            res += search_chord_dictionary(notes[idx], ["m3", "M3"])
        elif interval == "A6":
            tonic = notes[idx].get_note_by_major_interval(3)
            res.append({"chord": "GerVI", "scale": tonic, "is_major": True})
            res.append({"chord": "GerVI", "scale": tonic, "is_major": False})
            res.append({"chord": "FrVI", "scale": tonic, "is_major": True})
            res.append({"chord": "FrVI", "scale": tonic, "is_major": False})
            res.append({"chord": "ItVI", "scale": tonic, "is_major": True})
            res.append({"chord": "ItVI", "scale": tonic, "is_major": False})
        elif interval == "d7":
            res += search_chord_dictionary(notes[idx], ["m3", "m3", "m3"])
        elif interval == "m7":
            res += search_chord_dictionary(notes[idx], ["M3", "m3", "m3"])
            res += search_chord_dictionary(notes[idx], ["m3", "M3", "m3"])
            res += search_chord_dictionary(notes[idx], ["m3", "m3", "M3"])
        elif interval == "M7":
            res += search_chord_dictionary(notes[idx], ["M3", "m3", "M3"])
        # The rest 13 intervals have no combinations of intervals
    return res


# def find_chords(notes_intervals):
#     res = []
#     print(len(MAJOR_CHORD_FINDER_DICTIONARY))
#     for k, v in MAJOR_CHORD_FINDER_DICTIONARY.items():
#         print(k, v)
#         chord = list(k)
#         # print("a:", chord, notes_intervals)
#         for idx in range(len(notes_intervals) - len(chord) + 1):
#             # print("b:", notes_intervals[idx : idx + len(chord)])
#             if notes_intervals[idx : idx + len(chord)] == chord:
#                 res += v
#                 # print("c:", res)
#     print(len(MINOR_CHORD_FINDER_DICTIONARY))
#     for k, v in MINOR_CHORD_FINDER_DICTIONARY.items():
#         print(k, v)
#         chord = list(k)
#         # print(chord, v)
#         for idx in range(len(notes_intervals) - len(chord) + 1):
#             if notes_intervals[idx : idx + len(chord)] == chord:
#                 res += v
#     return res


# print all right pattern
def print_chords_names(notes, possible_chords):
    notes_str = [note.note_str() for note in notes]
    for ans in possible_chords:
        chord_notes = pick_chord(ans["scale"], ans["chord"], ans["is_major"])
        chord_notes_str = [note.note_str() for note in chord_notes]
        print(ans["chord"], end=" chord in ")
        if ans["is_major"]:
            print(ans["scale"].note_str(), "major.")
        else:
            print(ans["scale"].note_str().lower(), "minor.")
        missing_notes = list(set(chord_notes_str) - set(notes_str))
        print("Missing notes:", missing_notes)

        # print(ans)
        # major_interval = invert_interval(ans["tonic_interval"])
        # print(major_interval)
        # chord_scale = notes[0].get_note_by_interval(
        #     major_interval[0], int(major_interval[1])
        # )

        # scale_str = ""
        # is_major = True
        # if ans["chord"] in MAJOR_CHORD_DICTIONARY:
        #     scale_str = chord_scale.note_str()
        # else:
        #     scale_str = chord_scale.get_note_by_interval("M", 6).note_str().lower()
        #     is_major = False
        # if scale_str == scale or scale == "":
        #     print(ans["chord"], "in", scale_str, "major" if is_major else "minor")


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
    print(notes[0].note_str(), notes_intervals)
    possible_chords = find_chords_two_notes(notes[0:2], notes_intervals[0:2])
    # possible_chords = find_chords(notes_intervals)
    # print(possible_chords)
    print_chords_names(notes[0:2], possible_chords)

    print("--- Used %s seconds ---" % (time.time() - start_time))