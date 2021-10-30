from utility import note_input_convertor
import music21
import time

base_notes = ["C", "C#", "D-", "F", "G-", "A#", "B--", "B", "E-", "F##"]
m21_notes = [music21.note.Note(base + "5") for base in base_notes]
base_notes_len = len(base_notes)
intervals = ["P1", "M2", "m3", "d4", "P5", "m6", "d7"]
intervals_len = len(intervals)
TRIAL = 10000

if __name__ == "__main__":

    def use_music21_interval_test():
        start_time1 = time.time()
        for i in range(TRIAL):
            note = base_notes[i % base_notes_len]
            interval = intervals[i % intervals_len]
            new_note = music21.pitch.Pitch(note).transpose(interval)
            if i < 10:
                print(new_note.name)

        # Time calculation
        print(
            "--- With using music21 library: Used %s seconds ---"
            % (time.time() - start_time1)
        )

    def no_music21_library_interval_test():
        # Time calculation
        start_time = time.time()

        for i in range(TRIAL):
            # note = note_input_convertor(base_notes[i % base_notes_len])
            m21_note = m21_notes[i % base_notes_len]
            note = note_input_convertor(m21_note.name)
            interval = intervals[i % intervals_len]
            new_note = note.get_note_by_interval(interval)
            if i < 10:
                print(music21.note.Note(new_note.note_str(False)))

        # Time calculation
        print(
            "--- Without using music21 library: Used %s seconds ---"
            % (time.time() - start_time)
        )

    use_music21_interval_test()
    no_music21_library_interval_test()