if __name__ == "__main__":
    import os, sys
    sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utility.constant import (
    HEPTATONIC_DICTIONARY as NOTE_DICT,
    MAJOR_SEMITONE_CUMULATIVE_PATTERN as SEMITONES_CP,
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
        return (NOTE_DICT[self.alphabet] + self.accidental) % 12

    # TODO: Can omit it
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
        def new_method():
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
                    - NOTE_DICT[new_alphabet]
                )

                accidental_range = 4
                new_accidental = (
                    new_accidental + accidental_range
                ) % 12 - accidental_range

                return Note(new_alphabet, new_accidental)
            else:
                print("Error in get_note_by_interval.")
                return Note("?", 0)

        # TODO: OLD METHOD. Can omit it
        def old_method():
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

        return new_method()

    # Given two notes with ordering, return the interval
    def get_interval(self, upper_note):
        def old_method():
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

        # TODO: Is new METHOD faster?
        def new_method():
            alphabetical_distance = (
                ord(upper_note.alphabet) - ord(self.alphabet)
            ) % 7 + 1
            semitone_difference = (
                upper_note.get_pitch_class() - self.get_pitch_class()
            ) % 12
            intervals = SEMITONE_TO_INTERVAL_DICTIONARY[semitone_difference]

            # print(alphabetical_distance, semitone_difference, intervals)
            for interval in intervals:
                if int(interval[1]) == alphabetical_distance:
                    return interval
            return "?0"

        return new_method()
