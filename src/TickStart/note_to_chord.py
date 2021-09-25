from constant import *
from utility import note_input_convertor, invert_interval
from chord_to_note import pick_chord
import sys
import time
from itertools import combinations

# For a list of notes with length n, output all intervals that between i and (i+1) mod n notes,
# i.e. the nth/1st notes interval is included
def get_adjacent_intervals(notes):
    notes_num = len(notes)
    res = []
    for i in range(notes_num):
        new_interval = notes[i % notes_num].get_interval(notes[(i + 1) % notes_num])
        res.append(new_interval)
    return res


def search_chord_dictionary(first_note, target):
    res = []

    def search_one_dictionary(is_major):
        dictionary = (
            MAJOR_CHORD_FINDER_DICTIONARY if is_major else MINOR_CHORD_FINDER_DICTIONARY
        )
        for k, v in dictionary.items():
            chord = list(k)
            isMatchedChord = chord == target
            if isMatchedChord:
                for option in v:
                    tonic_interval = invert_interval(option["tonic_interval"])
                    res.append(
                        {
                            "chord": option["chord"],
                            "tonic": first_note.get_note_by_interval(tonic_interval),
                            "is_major": is_major,
                        }
                    )

    search_one_dictionary(True)
    search_one_dictionary(False)
    return res


# find chords
def find_chords_two_notes(notes, notes_intervals):
    # print(notes, notes_intervals)
    res = []
    for idx in range(len(notes_intervals)):
        interval = notes_intervals[idx]
        if interval == "M3":
            res += search_chord_dictionary(notes[idx], ["M3", "m3"])
        elif interval == "m3":
            res += search_chord_dictionary(notes[idx], ["m3", "M3"])
            res += search_chord_dictionary(notes[idx], ["m3", "m3"])
        # elif interval == "M2":
        #     res.append({"chord": "FrVI", "tonic": notes[idx], "is_major": True})
        #     res.append({"chord": "FrVI", "tonic": notes[idx], "is_major": False})
        # elif interval == "A2":
        #     tonic = notes[idx].get_note_by_major_interval(6)
        #     res.append({"chord": "GerVI", "tonic": tonic, "is_major": True})
        #     res.append({"chord": "GerVI", "tonic": tonic, "is_major": False})
        # elif interval == "A4":
        #     res.append({"chord": "ItVI", "tonic": notes[idx], "is_major": True})
        #     res.append({"chord": "ItVI", "tonic": notes[idx], "is_major": False})
        elif interval == "d5":
            res += search_chord_dictionary(notes[idx], ["m3", "m3"])
        elif interval == "P5":
            res += search_chord_dictionary(notes[idx], ["M3", "m3"])
            res += search_chord_dictionary(notes[idx], ["m3", "M3"])
        elif interval == "A6":
            tonic = notes[idx].get_note_by_major_interval(3)
            res.append({"chord": "ItVI", "tonic": tonic, "is_major": True})
            res.append({"chord": "ItVI", "tonic": tonic, "is_major": False})
        # elif interval == "d7":
        #     res += search_chord_dictionary(notes[idx], ["m3", "m3", "m3"])
        # elif interval == "m7":
        #     res += search_chord_dictionary(notes[idx], ["M3", "m3", "m3"])
        #     res += search_chord_dictionary(notes[idx], ["m3", "M3", "m3"])
        #     res += search_chord_dictionary(notes[idx], ["m3", "m3", "M3"])
        # elif interval == "M7":
        #     res += search_chord_dictionary(notes[idx], ["M3", "m3", "M3"])
        # The rest 13 intervals have no combinations of intervals
    return res


def match_chords_patterns(notes, notes_intervals):
    # base case: notes = 2
    notes_num = len(notes)
    if notes_num == 2:
        return find_chords_two_notes(notes, notes_intervals)

    # If the notes satisfy the chord pattern , get the chord
    res = []
    if notes_num == 3 or notes_num == 4:
        for idx in range(notes_num):
            rotated_notes = notes[-idx:] + notes[:-idx]
            rotated_intervals = notes_intervals[-idx:] + notes_intervals[:-idx]

            # the last interval is ignored as it is the difference between last and first notes
            res += search_chord_dictionary(
                rotated_notes[0],
                rotated_intervals[0 : notes_num - 1],
            )

    return res


# Find chords in 'recursive' way
def find_chords(notes):
    # do sorting
    notes.sort(key=lambda x: (x.alphabet, x.accidental))
    res = []

    # drop a note if previous combinations have no result
    for note_num in range(len(notes), 1, -1):
        # cannot have chord with more than 4 notes
        if note_num > 4:
            continue
        # for each combination, search if it satisfy the pattern of chords
        for combo in list(combinations(notes, note_num)):
            # Then generate the intervals
            notes_intervals = get_adjacent_intervals(combo)
            res += match_chords_patterns(list(combo), notes_intervals)
        # if drop several notes to get result, stop searching
        if len(res) > 0:
            break

    return res


# print all right pattern
def print_chords_names(notes, possible_chords, scale):
    # Get the scale in note object
    if scale == "":
        target_tonic = ""
    else:
        target_tonic = note_input_convertor(scale).note_str()
    target_is_major = scale.isupper()

    notes_str = [note.note_str() for note in notes]
    total_valid_chords = 0

    for ans in possible_chords:
        chord_tonic = ans["tonic"].note_str()
        # print if there is no specify scale or match the scale
        if target_tonic == "" or (
            target_tonic == chord_tonic and target_is_major == ans["is_major"]
        ):
            chord_notes = pick_chord(ans["tonic"], ans["chord"], ans["is_major"])
            # If you get some strange notes, just DO NOT return that chord
            if chord_notes == None:
                continue
            chord_notes_str = [note.note_str() for note in chord_notes]
            print(ans["chord"], end=" chord in ")
            if ans["is_major"]:
                print(chord_tonic, "major; ", end="")
            else:
                print(chord_tonic.lower(), "minor; ", end="")
            print("Chord notes :", chord_notes_str, end="")
            missing_notes = list(set(chord_notes_str) - set(notes_str))
            if len(missing_notes) > 0:
                print("; Missing notes :", missing_notes, end="")
            print()
            total_valid_chords += 1
    print("--- Total %d chords ---" % (total_valid_chords))


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

    # First convert to notes
    notes = [note_input_convertor(note) for note in input_notes]

    # search for the right pattern
    # print(notes[0].note_str(), notes_intervals)
    possible_chords = find_chords(notes)
    print_chords_names(notes, possible_chords, scale)

    # Time calculation
    print("--- Used %s seconds ---" % (time.time() - start_time))