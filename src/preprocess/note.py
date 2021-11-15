if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from utility.constant import (
    HEPTATONIC_DICTIONARY,
    SEMITONE_TO_INTERVAL_DICTIONARY,
    INTERVAL_TO_SEMITONE_DICTIONARY,
)


class Note:
    def __init__(self, alphabet, accidental):
        self.alphabet = alphabet
        self.accidental = accidental

    # Use string format to represent the note
    def note_str(self, isPrintedInDos=True):
        # If print in DOS, keep the representation as good as possible;
        # If used by music21, keep the alignment with music21
        sharp = "♯" if isPrintedInDos else "#"
        flat = "♭" if isPrintedInDos else "-"
        accidentals = ""
        if self.accidental > 0:
            accidentals = sharp * self.accidental
        elif self.accidental < 0:
            accidentals = flat * (-1 * self.accidental)
        return self.alphabet + accidentals

    # Give pitch class of a note
    def get_pitch_class(self):
        return (HEPTATONIC_DICTIONARY[self.alphabet] + self.accidental) % 12

    # quality: M (major), m (minor), P (perfect), A (augmented), d (diminished)
    def get_note_by_interval(self, interval):
        if interval in INTERVAL_TO_SEMITONE_DICTIONARY:
            alphabetical_distance = int(interval[1])
            semitone_difference = INTERVAL_TO_SEMITONE_DICTIONARY[interval]

            new_alphabet = chr(
                (ord(self.alphabet) - ord("A") + alphabetical_distance - 1) % 7
                + ord("A")
            )
            new_accidental = (
                self.get_pitch_class()
                + semitone_difference
                - HEPTATONIC_DICTIONARY[new_alphabet]
            )

            accidental_range = 4
            new_accidental = (new_accidental + accidental_range) % 12 - accidental_range

            return Note(new_alphabet, new_accidental)
        else:
            print("Error in get_note_by_interval.")
            return Note("?", 0)

    # Given two notes with ordering, return the interval
    def get_interval(self, upper_note):
        alphabetical_distance = (ord(upper_note.alphabet) - ord(self.alphabet)) % 7 + 1
        semitone_difference = (
            upper_note.get_pitch_class() - self.get_pitch_class()
        ) % 12
        intervals = SEMITONE_TO_INTERVAL_DICTIONARY[semitone_difference]

        # print(alphabetical_distance, semitone_difference, intervals)
        for interval in intervals:
            if int(interval[1]) == alphabetical_distance:
                return interval
        return "?0"
