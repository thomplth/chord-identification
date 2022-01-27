if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from preprocess.scale import Scale
from chord_to_note import pick_chord
from utility.constant import (
    MAJOR_CHORD_DICTIONARY,
    MINOR_CHORD_DICTIONARY,
    CHORD_FORM_DICTIONARY,
)
from utility import note_input_convertor

# All chords in Chord class are in Roman numeral analysis
class Chord:
    def __init__(self, scale: Scale = None, numeral: str = ""):
        self.scale: Scale = Scale() if scale is None else scale
        self.numeral: str = numeral
        dictionary = (
            MAJOR_CHORD_DICTIONARY if self.scale.is_major else MINOR_CHORD_DICTIONARY
        )
        self.form: str = "?"
        if numeral in dictionary:
            self.form = CHORD_FORM_DICTIONARY[tuple(dictionary[numeral][1:])]

    # get the jazz representation of a chord
    def get_jazz_representation(self):
        dictionary = (
            MAJOR_CHORD_DICTIONARY if self.scale.is_major else MINOR_CHORD_DICTIONARY
        )
        interval = dictionary[self.numeral][0]
        root = self.scale.tonic.get_note_by_interval(interval)
        return root.note_str() + " " + self.form

    # determine if two chords are equal
    # support neglect seventh note and Jazz chord comparison
    def is_equal(self, other_chord, on_triad=False, on_jazz=False):
        flag: bool = True

        if on_jazz:
            flag = (
                self.get_jazz_representation() == other_chord.get_jazz_representation()
            )
        else:
            # not on jazz must have same scale
            flag = self.scale.is_equal(other_chord.scale)
            if not flag:
                return flag
            flag = self.numeral == other_chord.numeral

        if on_triad and not flag:

            def get_first_three_notes_str(chord):
                notes = pick_chord(
                    chord.scale.tonic, chord.numeral, chord.scale.is_major
                )
                return tuple([note.note_str() for note in notes[:3]])

            self_notes = get_first_three_notes_str(self)
            other_notes = get_first_three_notes_str(other_chord)
            return self_notes == other_notes
        else:
            return flag

    # Use string format to represent the chord
    def chord_str(self, isPrintedInDos=False):
        scale_str = self.scale.scale_str(isPrintedInDos)
        result = self.numeral + " chord in " + scale_str
        return result


# A child class is made for initialize the Jazz chord easily
class JazzChord(Chord):
    def __init__(self, scale: Scale = None, root: str = "", form: str = ""):
        root_note = note_input_convertor(root)
        print(scale.tonic.get_interval(root_note))
        # TODO: Complete the rest.
        numeral: str = "I"
        super().__init__(scale, numeral)


if __name__ == "__main__":
    c = Scale("D", 0, True)
    g = Scale("G", 0, True)
    x = Chord(c, numeral="I")
    y = Chord(g, numeral="V7")
    j = JazzChord(g, "C", "")
    # print(x.is_equal(y))
    # print(x.is_equal(y, True))
    # print(x.is_equal(y, True, True))
    # print(x.is_equal(y, False, True))
    print(j.get_jazz_representation())
