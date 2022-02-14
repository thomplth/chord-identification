if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from utility.constant import (
    HEPTATONIC_DICT as NOTE_DICT,
    MAJOR_SEMITONE_CUMULATIVE_PATTERN as SEMITONES_CP,
)


class Note:
    def __init__(self, alphabet, accidental):
        self.alphabet = alphabet
        self.accidental = accidental

    # Use string format to represent the note
    def __str__(self, isPrintedInDos=True):
        pass

    # It also includes prefect interval
    # distance is 1 - 7, meaning from prefect unison, P1, to major seventh, M7
    def get_note_by_major_interval(self, distance):
        new_alphabet = chr(
            (ord(self.alphabet) - ord("A") + distance - 1) % 7 + ord("A")
        )
        new_accidental = (
            SEMITONES_CP[distance - 1]
            - (NOTE_DICT[new_alphabet] - NOTE_DICT[self.alphabet]) % 12
            + self.accidental
        )
        return Note(new_alphabet, new_accidental)

    # Here is the general one
    # quality: M (major), m (minor), P (perfect), A (augmented), d (diminished)
    def get_note_by_interval(self, interval):

        quality = interval[0]
        distance = int(interval[1])
        if distance < 1 or distance > 8:
            print("Distance Error in get_note_by_interval.")
        if not quality in ["M", "m", "P", "A", "d"]:
            print("Quality Error in get_note_by_interval.")
        new_note = self.get_note_by_major_interval((distance - 1) % 7 + 1)

        if quality == "A":
            new_note.accidental += 1
        elif distance in [2, 3, 6, 7]:
            if quality == "m":
                new_note.accidental -= 1
            elif quality == "d":
                new_note.accidental -= 2
            elif not quality == "M":
                print("Wrong interval name!")
        else:
            if quality == "d":
                new_note.accidental -= 1
            elif not quality == "P":
                print("Wrong interval name!")
        return new_note

    # Given two notes with ordering, return the interval
    def get_interval(self, upper_note):
        distance = (ord(upper_note.alphabet) - ord(self.alphabet)) % 7 + 1
        accidental = (
            (NOTE_DICT[upper_note.alphabet] - NOTE_DICT[self.alphabet]) % 12
            + upper_note.accidental
            - self.accidental
            - SEMITONES_CP[distance - 1]
        )
        quality = "?"
        if accidental == 1:
            quality = "A"
        elif distance in [2, 3, 6, 7]:
            if accidental == -1:
                quality = "m"
            elif accidental == -2:
                quality = "d"
            elif accidental == 0:
                quality = "M"
        elif distance in [1, 4, 5]:
            if accidental == -1:
                quality = "d"
                if distance == 1:
                    distance = 8
            elif accidental == 0:
                quality = "P"

        return quality + str(distance)
