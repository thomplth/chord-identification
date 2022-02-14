if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from utility.constant import (
    HEPTATONIC_DICT,
    SEMITONE_INTERVAL_DICT,
    INTERVAL_SEMITONE_DICT,
)


class Note:
    def __init__(self, alphabet: str = "C", accidental: int = 0):
        self.alphabet = "C"
        if alphabet in ["A", "B", "C", "D", "E", "F", "G"]:
            self.alphabet = alphabet
        self.accidental = 0
        if accidental in range(-2, 3):
            self.accidental = accidental

    # determine if two notes are equal
    def is_equal(self, other_note) -> bool:
        """
        :other_note: Note object
        """
        return (self.alphabet == other_note.alphabet) and (
            self.accidental == other_note.accidental
        )

    # Use string format to represent the note
    def __str__(self) -> str:
        # If print in DOS, keep the representation as good as possible;
        # If used by music21, keep the alignment with music21
        sharp = "#"  # "♯"
        flat = "-"  # "♭"
        accidentals = ""
        if self.accidental > 0:
            accidentals = sharp * self.accidental
        elif self.accidental < 0:
            accidentals = flat * (-1 * self.accidental)
        return self.alphabet + accidentals

    # Give pitch class of a note
    def get_pitch_class(self) -> int:
        """
        :return type: int range [1:11]
        """
        return (HEPTATONIC_DICT[self.alphabet] + self.accidental) % 12

    # quality: M (major), m (minor), P (perfect), A (augmented), d (diminished)
    def get_note_by_interval(self, interval):
        """
        :interval: char[2], where char[0] = quality, char[1] = int range [1:7]
        """
        if interval in INTERVAL_SEMITONE_DICT:
            alphabetical_distance = int(interval[1])
            semitone_difference = INTERVAL_SEMITONE_DICT[interval]

            new_alphabet = chr(
                (ord(self.alphabet) - ord("A") + alphabetical_distance - 1) % 7
                + ord("A")
            )
            new_accidental = (
                self.get_pitch_class()
                + semitone_difference
                - HEPTATONIC_DICT[new_alphabet]
            )

            accidental_range = 4
            new_accidental = (new_accidental + accidental_range) % 12 - accidental_range

            return Note(new_alphabet, new_accidental)
        else:
            print("Error in get_note_by_interval.")
            return Note("?", 0)

    # Given two notes with ordering, return the interval
    def get_interval(self, upper_note) -> str:
        """
        :upper_note: Note object
        """
        alphabetical_distance = (ord(upper_note.alphabet) - ord(self.alphabet)) % 7 + 1
        semitone_difference = (
            upper_note.get_pitch_class() - self.get_pitch_class()
        ) % 12
        intervals = SEMITONE_INTERVAL_DICT[semitone_difference]

        # print(alphabetical_distance, semitone_difference, intervals)
        for interval in intervals:
            if int(interval[1]) == alphabetical_distance:
                return interval
        return "?0"
