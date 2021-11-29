if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from music21.search.segment import scoreSimilarity
from utility.constant import *
from utility import note_input_convertor, invert_interval

# from preprocess.note import Note
from preprocess.scale import Scale
import sys
import time
from itertools import combinations

# Given the scale and the chord, output the notes of the chord
def pick_chord(scale, chord):
    tonic, is_major = scale.tonic, scale.is_major

    chord_intervals = (
        MAJOR_CHORD_DICTIONARY[chord] if is_major else MINOR_CHORD_DICTIONARY[chord]
    )
    base_note = tonic
    chord_notes = []
    for interval in chord_intervals:
        next_note = base_note.get_note_by_interval(interval)
        chord_notes.append(next_note)
        base_note = next_note
    return chord_notes


# For a list of notes with length n, output all intervals that between i and (i+1) mod n notes,
# i.e. the nth/1st notes interval is included
def get_adjacent_intervals(notes):
    notes_num = len(notes)
    res = []
    for i in range(notes_num):
        new_interval = notes[i % notes_num].get_interval(notes[(i + 1) % notes_num])
        res.append(new_interval)
    return res


def search_chord_dictionary(first_note, target, pitch_scale):
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
                    chord_scale = Scale(
                        tonic_note=first_note.get_note_by_interval(tonic_interval),
                        is_major=is_major,
                    )
                    # if chord_scale.is_equal(scale) or scale.tonic.alphabet == "?":
                    if pitch_scale == None or (
                        pitch_scale == chord_scale.get_pitch_scale()
                    ):
                        res.append(
                            {
                                "chord": option["chord"],
                                "scale": chord_scale
                                # "tonic": first_note.get_note_by_interval(tonic_interval),
                                # "is_major": is_major,
                            }
                        )

    search_one_dictionary(True)
    search_one_dictionary(False)

    return res


# find chords
def find_chords_two_notes(notes, notes_intervals, pitch_scale):
    # print(notes, notes_intervals)
    res = []
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
            if pitch_scale[0] == tonic.get_pitch_class():
                res.append({"chord": "ItaVI", "scale": Scale(tonic, True)})
                res.append({"chord": "ItaVI", "scale": Scale(tonic, False)})

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


def match_chords_patterns(notes_freq, pitch_scale):
    # base case: notes = 2
    notes_num = len(notes_freq)

    # get notes and similarity score
    notes = [note_freq[0] for note_freq in notes_freq]
    similarity_score = sum([note_freq[1] for note_freq in notes_freq])
    # Then generate the intervals
    notes_intervals = get_adjacent_intervals(notes)

    if notes_num == 2:
        chords = find_chords_two_notes(notes, notes_intervals, pitch_scale)
        return [(chord, similarity_score) for chord in chords]

    # If the notes satisfy the chord pattern , get the chord
    res = []
    if notes_num == 3 or notes_num == 4:
        for idx in range(notes_num):
            rotated_notes = notes[-idx:] + notes[:-idx]
            rotated_intervals = notes_intervals[-idx:] + notes_intervals[:-idx]

            # the last interval is ignored as it is the difference between last and first notes
            chords = search_chord_dictionary(
                rotated_notes[0], rotated_intervals[0 : notes_num - 1], pitch_scale
            )
            res.extend([(chord, similarity_score) for chord in chords])

    return res


# Find chords in 'recursive' way
def find_chords(notes_freq, pitch_scale=None):

    # do sorting
    notes_freq.sort(key=lambda x: (x[0].alphabet, x[0].accidental))
    res = []

    # drop a note if previous combinations have no result
    for note_num in range(len(notes_freq), 1, -1):
        # cannot have chord with more than 4 notes
        if note_num > 4:
            continue
        # for each combination, search if it satisfy the pattern of chords
        for combo in list(combinations(notes_freq, note_num)):
            res += match_chords_patterns(list(combo), pitch_scale)
        # if drop several notes to get result, stop searching
        # TODO: Determine if the break is needed
        # if len(res) > 0:
        #     break

    return res


# print all right pattern
def print_chords_names(notes, possible_chords, target_scale):
    notes_str = [note.note_str() for note in notes]
    total_valid_chords = 0

    for ans in possible_chords:
        # chord_tonic = ans["tonic"].note_str()
        # print if there is no specify scale or match the scale
        if target_scale.tonic.alphabet == "?" or target_scale.is_equal(ans["scale"]):
            chord_notes = pick_chord(ans["scale"], ans["chord"])
            # If you get some strange notes, just DO NOT return that chord
            if chord_notes == None:
                continue
            chord_notes_str = [note.note_str() for note in chord_notes]
            print(ans["chord"] + " chord in " + ans["scale"].scale_str(True), end=" ")
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
        target_tonic = note_input_convertor(scale)
        target_scale = Scale(tonic_note=target_tonic, is_major=scale.isupper())

    # First convert to notes
    notes = [note_input_convertor(note) for note in input_notes]

    # search for the right pattern
    # print(notes[0].note_str(), notes_intervals)
    possible_chords = find_chords(notes, target_scale)
    print_chords_names(notes, possible_chords, target_scale)

    # Time calculation
    print("--- Used %s seconds ---" % (time.time() - start_time))