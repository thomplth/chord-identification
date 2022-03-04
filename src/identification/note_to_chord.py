if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from utility.chord_constant import *
from utility import invert_interval
from utility.entities import Notes_frequencies, Pitch_scale, ChordSimilarityScore

from preprocess.note import Note
from preprocess.scale import Scale
from preprocess.chord import Chord
import sys
import time
from itertools import combinations

# Given the scale and the chord, output the notes of the chord
def pick_chord(scale: Scale, roman: str) -> list[Note]:
    base_note, is_major = scale.tonic, scale.is_major

    chord_intervals = MAJOR_CHORD_DICT[roman] if is_major else MINOR_CHORD_DICT[roman]
    chord_notes: list[Note] = []
    for interval in chord_intervals:
        base_note = base_note.get_note_by_interval(interval)
        chord_notes.append(base_note)
    return chord_notes


# For a list of notes with length n, output all intervals that between i and (i+1) mod n notes,
# i.e. the nth/1st notes interval is included
def get_adjacent_intervals(notes: list[Note]) -> list[str]:
    notes_num = len(notes)
    res: list[str] = []
    for i in range(notes_num):
        new_interval = notes[i % notes_num].get_interval(notes[(i + 1) % notes_num])
        res.append(new_interval)
    return res


def search_chord_dictionary(
    first_note: Note, target: list[str], pitch_scale: tuple[int, bool]
) -> list[Chord]:
    res: list[Chord] = []

    def search_one_dictionary(is_major: bool):
        dictionary = MAJOR_CHORD_FINDER_DICT if is_major else MINOR_CHORD_FINDER_DICT
        for k, v in dictionary.items():
            chord = list(k)
            isMatchedChord = chord == target
            if isMatchedChord:
                for option in v:
                    tonic_interval = invert_interval(option["tonic_interval"])
                    chord_scale = Scale(
                        tonic_note=first_note.get_note_by_interval(tonic_interval),
                        is_major=is_major,
                    )
                    # if chord_scale.is_equal(scale) or scale.tonic.alphabet == "?":
                    if pitch_scale == None or (
                        pitch_scale == chord_scale.get_pitch_scale()
                    ):
                        res.append(Chord(scale=chord_scale, numeral=option["chord"]))

    search_one_dictionary(True)
    search_one_dictionary(False)

    return res


# find chords
def find_chords_two_notes(
    notes: list[Note], notes_intervals: list[str], pitch_scale: tuple[int, bool]
) -> list[Chord]:
    # print(notes, notes_intervals)
    res: list[Chord] = []
    for idx in range(len(notes_intervals)):
        interval = notes_intervals[idx]
        if interval == "M3":
            res += search_chord_dictionary(notes[idx], ["M3", "m3"], pitch_scale)
        elif interval == "m3":
            res += search_chord_dictionary(notes[idx], ["m3", "M3"], pitch_scale)
            res += search_chord_dictionary(notes[idx], ["m3", "m3"], pitch_scale)
        # elif interval == "M2":
        #     res.append({"chord": "FreVI", "tonic": notes[idx], "is_major": True})
        #     res.append({"chord": "FreVI", "tonic": notes[idx], "is_major": False})
        # elif interval == "A2":
        #     tonic = notes[idx].get_note_by_interval("M6")
        #     res.append({"chord": "GerVI", "tonic": tonic, "is_major": True})
        #     res.append({"chord": "GerVI", "tonic": tonic, "is_major": False})
        # elif interval == "A4":
        #     res.append({"chord": "ItaVI", "tonic": notes[idx], "is_major": True})
        #     res.append({"chord": "ItaVI", "tonic": notes[idx], "is_major": False})
        elif interval == "d5":
            res += search_chord_dictionary(notes[idx], ["m3", "m3"], pitch_scale)
        elif interval == "P5":
            res += search_chord_dictionary(notes[idx], ["M3", "m3"], pitch_scale)
            res += search_chord_dictionary(notes[idx], ["m3", "M3"], pitch_scale)
        elif interval == "A6":
            tonic = notes[idx].get_note_by_interval("M3")
            # res.append({"chord": "ItaVI", "tonic": tonic, "is_major": True})
            # res.append({"chord": "ItaVI", "tonic": tonic, "is_major": False})
            # if scale.tonic.is_equal(tonic):
            if pitch_scale == None or pitch_scale[0] == tonic.get_pitch_class():
                res.append(
                    Chord(scale=Scale(tonic_note=tonic, is_major=True), numeral="ItaVI")
                )
                res.append(
                    Chord(
                        scale=Scale(tonic_note=tonic, is_major=False), numeral="ItaVI"
                    )
                )

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


def match_chords_patterns(
    notes_freq: Notes_frequencies, pitch_scale: Pitch_scale
) -> list[ChordSimilarityScore]:
    # base case: notes = 2
    notes_num = len(notes_freq)

    # get notes and similarity score
    notes: list[Note] = [note_freq[0] for note_freq in notes_freq]
    similarity_score: float = sum([note_freq[1] for note_freq in notes_freq])
    # Then generate the intervals
    notes_intervals: list[str] = get_adjacent_intervals(notes)

    found_chords = []
    if notes_num == 2:
        chords = find_chords_two_notes(notes, notes_intervals, pitch_scale)
        found_chords = [
            {"chord": chord, "similarity_score": similarity_score} for chord in chords
        ]
        return found_chords

    # If the notes satisfy the chord pattern , get the chord
    if notes_num == 3 or notes_num == 4:
        for idx in range(notes_num):
            rotated_notes = notes[-idx:] + notes[:-idx]
            rotated_intervals = notes_intervals[-idx:] + notes_intervals[:-idx]

            # the last interval is ignored as it is the difference between last and first notes
            chords = search_chord_dictionary(
                rotated_notes[0], rotated_intervals[0 : notes_num - 1], pitch_scale
            )
            found_chords.extend(
                [
                    {"chord": chord, "similarity_score": similarity_score}
                    for chord in chords
                ]
            )

    return found_chords


# Find chords in 'recursive' way
def find_chords(
    notes_freq: Notes_frequencies, pitch_scale: Pitch_scale = None
) -> list[ChordSimilarityScore]:

    # do sorting
    notes_freq.sort(key=lambda x: (x[0].alphabet, x[0].accidental))
    found_chords: list[ChordSimilarityScore] = []

    # drop a note if previous combinations have no result
    for note_num in range(len(notes_freq), 1, -1):
        # cannot have chord with more than 4 notes
        if note_num > 4:
            continue
        # for each combination, search if it satisfy the pattern of chords
        for combo in list(combinations(notes_freq, note_num)):
            found_chords.extend(match_chords_patterns(list(combo), pitch_scale))
        # if drop several notes to get result, stop searching
        # TODO: Determine if the break is needed
        # if len(res) > 0:
        #     break

    return found_chords


# print all right pattern
def print_chords_names(notes, possible_chords, target_scale):
    notes_str = [note.__str__() for note in notes]
    total_valid_chords = 0

    for ans in possible_chords:
        # chord_tonic = ans["tonic"].__str__()
        # print if there is no specify scale or match the scale
        if target_scale.tonic.alphabet == "?" or target_scale.is_equal(ans["scale"]):
            chord_notes = pick_chord(ans["scale"], ans["chord"])
            # If you get some strange notes, just DO NOT return that chord
            if chord_notes == None:
                continue
            chord_notes_str = [note.__str__() for note in chord_notes]
            print(ans["chord"] + " chord in " + ans["scale"].__str__(), end=" ")
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
    target_scale = None
    if not scale == "":
        target_tonic = Note(input_str=scale)
        target_scale = Scale(tonic_note=target_tonic, is_major=scale.isupper())

    # First convert to notes
    notes = [Note(input_str=note) for note in input_notes]

    # search for the right pattern
    # print(notes[0].__str__(), notes_intervals)
    possible_chords = find_chords(notes, target_scale)
    print_chords_names(notes, possible_chords, target_scale)

    # Time calculation
    print("--- Used %s seconds ---" % (time.time() - start_time))