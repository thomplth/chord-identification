from constant import *
from utility import note_input_convertor, invert_interval
from chord_to_note import pick_chord
import sys
import time

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
            if chord[0 : len(target)] == target:
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
            res += search_chord_dictionary(notes[idx], [interval])
        elif interval == "m3":
            res += search_chord_dictionary(notes[idx], [interval])
        elif interval == "M2":
            res.append({"chord": "FrVI", "tonic": notes[idx], "is_major": True})
            res.append({"chord": "FrVI", "tonic": notes[idx], "is_major": False})
        elif interval == "A2":
            tonic = notes[idx].get_note_by_major_interval(6)
            res.append({"chord": "GerVI", "tonic": tonic, "is_major": True})
            res.append({"chord": "GerVI", "tonic": tonic, "is_major": False})
        elif interval == "A4":
            res.append({"chord": "GerVI", "tonic": notes[idx], "is_major": True})
            res.append({"chord": "GerVI", "tonic": notes[idx], "is_major": False})
            res.append({"chord": "FrVI", "tonic": notes[idx], "is_major": True})
            res.append({"chord": "FrVI", "tonic": notes[idx], "is_major": False})
            res.append({"chord": "ItVI", "tonic": notes[idx], "is_major": True})
            res.append({"chord": "ItVI", "tonic": notes[idx], "is_major": False})
        elif interval == "d5":
            res += search_chord_dictionary(notes[idx], ["m3", "m3"])
        elif interval == "P5":
            res += search_chord_dictionary(notes[idx], ["M3", "m3"])
            res += search_chord_dictionary(notes[idx], ["m3", "M3"])
        elif interval == "A6":
            tonic = notes[idx].get_note_by_major_interval(3)
            res.append({"chord": "GerVI", "tonic": tonic, "is_major": True})
            res.append({"chord": "GerVI", "tonic": tonic, "is_major": False})
            res.append({"chord": "FrVI", "tonic": tonic, "is_major": True})
            res.append({"chord": "FrVI", "tonic": tonic, "is_major": False})
            res.append({"chord": "ItVI", "tonic": tonic, "is_major": True})
            res.append({"chord": "ItVI", "tonic": tonic, "is_major": False})
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


# Find chords in recursive way
# TODO: enhances efficiency
def find_chords(notes, notes_intervals, can_drop_notes=True):
    # base case: notes = 2
    notes_num = len(notes)
    if notes_num == 2:
        return find_chords_two_notes(notes, notes_intervals)

    # If the notes satisfy the chord pattern by adding 0+ notes, stop
    res = []
    if notes_num == 3 or notes_num == 4:
        for idx in range(notes_num):
            r = idx % notes_num
            rotated_notes = notes[-r:] + notes[:-r]
            rotated_intervals = notes_intervals[-r:] + notes_intervals[:-r]

            res += search_chord_dictionary(
                rotated_notes[0], rotated_intervals[0 : notes_num - 1]
            )

    if len(res) > 0:
        return res

    # Else drop a note and search whether the rest notes can give a chord
    if can_drop_notes:

        def find_chords_in_subsets(notes, notes_num, can_drop):
            result = []
            for idx in range(notes_num):
                new_notes = notes.copy()
                new_notes.pop(idx)
                new_notes_intervals = get_adjacent_intervals(new_notes)
                result += find_chords(new_notes, new_notes_intervals, can_drop)
            return result

        # First disallow drop any notes for the subset of notes
        res += find_chords_in_subsets(notes, notes_num, False)
        # If none of the subset of notes can find a chord, allow them to drop one more note
        # If res has >= 1 chord, then recursion is avoided to enhance efficiency
        if len(res) == 0:
            res += find_chords_in_subsets(notes, notes_num, True)
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
    for ans in possible_chords:
        chord_tonic = ans["tonic"].note_str()
        # print if there is no specify scale or match the scale
        if target_tonic == "" or (
            target_tonic == chord_tonic and target_is_major == ans["is_major"]
        ):
            chord_notes = pick_chord(ans["tonic"], ans["chord"], ans["is_major"])
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
    # and do sorting
    notes.sort(key=lambda x: (x.alphabet, x.accidental))
    # Then generate the intervals
    notes_intervals = get_adjacent_intervals(notes)

    # search for the right pattern
    # print(notes[0].note_str(), notes_intervals)
    possible_chords = find_chords(notes, notes_intervals)
    print_chords_names(notes, possible_chords, scale)

    # Time calculation
    print("--- Used %s seconds ---" % (time.time() - start_time))