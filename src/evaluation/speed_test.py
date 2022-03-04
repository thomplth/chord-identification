if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from preprocess.note import Note
import music21

import time
from itertools import combinations

base_notes = ["C-", "C", "C#", "C##", "D--", "D-", "D", "D#"]
base_notes.extend(["E--", "E-", "E", "E#", "F-", "F", "F#", "F##"])
base_notes.extend(["G--", "G-", "G", "G#", "A-", "A", "A#", "A##"])
base_notes.extend(["B--", "B-", "B", "B#", "B##"])
m21_notes = [music21.note.Note(base + "5") for base in base_notes]
base_notes_len = len(base_notes)

intervals = ["P1", "A1", "d8", "M2", "A2", "m2", "d2", "M3", "A3", "m3", "d3"]
intervals.extend(["P4", "A4", "d4", "P5", "A5", "d5"])
intervals.extend(["M6", "A6", "m6", "d6", "M7", "A7", "m7", "d7"])
intervals_len = len(intervals)

if __name__ == "__main__":

    # TEST 1: Note generation by interval test
    trial_num = base_notes_len * intervals_len

    def use_music21_interval_test():
        start_time1 = time.time()
        result = []
        for i in range(trial_num):
            note = base_notes[i % base_notes_len]
            interval = intervals[i % intervals_len]
            new_note = music21.pitch.Pitch(note).transpose(interval)
            result.append(new_note.name)

        # Time calculation
        print(
            "--- With using music21 library: Used %s seconds ---"
            % (time.time() - start_time1)
        )
        return result

    def no_music21_library_interval_test():
        # Time calculation
        start_time = time.time()
        result = []

        for i in range(trial_num):
            m21_note = m21_notes[i % base_notes_len]
            note = Note(input_str=m21_note.name)
            interval = intervals[i % intervals_len]
            new_note = note.get_note_by_interval(interval)
            result.append(new_note.__str__())

        # Time calculation
        print(
            "--- Without using music21 library: Used %s seconds ---"
            % (time.time() - start_time)
        )
        return result

    result1 = use_music21_interval_test()
    result2 = no_music21_library_interval_test()
    for idx in range(trial_num):
        if not (result1[idx] == result2[idx]):
            print("Error: ", result1[idx], result2[idx])

    # Test 2: Interval calculation test
    trial_num = len(list(combinations(m21_notes, 2)))
    # print(trial_num)

    def use_music21_interval_test2():
        start_time1 = time.time()
        result = []
        for combo in list(combinations(m21_notes, 2)):
            ans = music21.interval.Interval(combo[0], combo[1])
            result.append(ans.name)

        # Time calculation
        print(
            "--- With using music21 library: Used %s seconds ---"
            % (time.time() - start_time1)
        )
        return result

    def no_music21_library_interval_test2():
        start_time = time.time()
        result = []
        for combo in list(combinations(m21_notes, 2)):
            notes = [Note(input_str=m21_note.name) for m21_note in combo]
            ans = notes[0].get_interval(notes[1])
            result.append(ans)

        # Time calculation
        print(
            "--- Without using music21 library: Used %s seconds ---"
            % (time.time() - start_time)
        )
        return result

    result1 = use_music21_interval_test2()
    result2 = no_music21_library_interval_test2()
    for idx in range(trial_num):
        if not (result1[idx] == result2[idx]):
            if len(result1[idx]) <= 2:  # Remove long quality supported by music21
                print("Error: ", idx, result1[idx], result2[idx])
