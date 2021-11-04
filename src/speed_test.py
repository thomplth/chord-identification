from utility import note_input_convertor
import music21
import time

base_notes = ["C", "C#", "C-", "C##", "D", "D#", "D-", "D--"]
base_notes.extend(["E", "E#", "E-", "E--", "F", "F#", "F-", "F##"])
base_notes.extend(["G", "G#", "G-", "G--", "A", "A#", "A-", "A##"])
base_notes.extend(["B", "B#", "B-", "B--", "B##"])
m21_notes = [music21.note.Note(base + "5") for base in base_notes]
base_notes_len = len(base_notes)
intervals = ["P1", "A1", "d8", "M2", "A2", "m2", "d2", "M3", "A3", "m3", "d3"]
intervals.extend(["P4", "A4", "d4", "P5", "A5", "d5"])
intervals.extend(["M6", "A6", "m6", "d6", "M7", "A7", "m7", "d7"])
intervals_len = len(intervals)
# print(base_notes_len, intervals_len)
TRIAL = 100000

if __name__ == "__main__":

    def use_music21_interval_test():
        start_time1 = time.time()
        result = []
        for i in range(TRIAL):
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

        for i in range(TRIAL):
            # note = note_input_convertor(base_notes[i % base_notes_len])
            m21_note = m21_notes[i % base_notes_len]
            note = note_input_convertor(m21_note.name)
            interval = intervals[i % intervals_len]
            new_note = note.get_note_by_interval(interval)
            result.append(new_note.note_str(False))

        # Time calculation
        print(
            "--- Without using music21 library: Used %s seconds ---"
            % (time.time() - start_time)
        )
        return result

    result1 = use_music21_interval_test()
    result2 = no_music21_library_interval_test()
    for idx in range(TRIAL):
        if not (result1[idx] == result2[idx]):
            print("Error: ", result1[idx], result2[idx])