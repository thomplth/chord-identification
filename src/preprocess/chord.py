if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from preprocess.note import Note
from preprocess.scale import Scale
from preprocess.chord_to_note import pick_chord
from utility import note_input_convertor
from utility.chord_constant import (
    CHORD_INTERVAL_FORM_BIDICT,
    CHORD_FORM_ABBR_BIDICT,
    MAJOR_CHORD_FINDER_DICT,
    MINOR_CHORD_FINDER_DICT,
)

# All chords in Chord class are in Roman numeral analysis
class Chord:
    def __init__(self, scale: Scale = None, numeral: str = "?"):
        self.scale: Scale = Scale() if scale is None else scale
        self.numeral: str = numeral
        dictionary = self.scale.get_chord_dictionary()

        self.form: str = "Undefined"
        self.root: Note = None
        if numeral in dictionary:
            self.form = CHORD_INTERVAL_FORM_BIDICT[tuple(dictionary[numeral][1:])]
            interval = dictionary[numeral][0]
            self.root = self.scale.tonic.get_note_by_interval(interval)

    # get the jazz representation of a chord
    def get_jazz_representation(self) -> str:
        if self.form == "Undefined":
            return "Undefined"
        return self.root.note_str() + " " + self.form

    # determine if two chords are equal
    # support neglect seventh note (on_triad) and Jazz chord comparison (on_jazz)
    # When on_triad and on_jazz = true, only on_jazz works
    def is_equal(
        self, other_chord, on_triad: bool = False, on_jazz: bool = False
    ) -> bool:

        if self.form == "Undefined" or other_chord.form == "Undefined":
            print("Cannot compare as there is an undefined chord.")
            return False

        if on_jazz:
            return (
                self.get_jazz_representation() == other_chord.get_jazz_representation()
            )

        # not on_jazz must have same scale
        flag: bool = self.scale.is_equal(other_chord.scale)
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
    def chord_str(self, isPrintedInDos: bool = False) -> str:
        scale_str = self.scale.scale_str(isPrintedInDos)
        result = self.numeral + " chord in " + scale_str
        return result


import re


def SplitJazzChordProperties(jazz_chord: str) -> list[str]:
    return re.findall("[A-G][#b-]?|.*[m|o]7?|7|.*\+6", jazz_chord)
    # Explain: Return an array with max length of 2, where
    # 1. root note, which can contain sharp or flat
    # 2. chord form, which can return 'm', 'm7', 'dim', 'dim7', 'o7', '+6' and '7'
    #    if a chord is major in form then the length of the array is 1.


# A child class is made for initialize the Jazz chord easily
class JazzChord(Chord):
    def __init__(self, scale: Scale = None, name: str = ""):
        chord_props = SplitJazzChordProperties(name)
        root: str = ""
        abbr_form: str = ""
        if len(chord_props) > 0:
            root = chord_props[0]
            if len(chord_props) > 1:
                abbr_form = chord_props[1]

        root_note = note_input_convertor(root)
        tonic_interval = scale.tonic.get_interval(root_note)

        if abbr_form not in CHORD_FORM_ABBR_BIDICT.inverse:
            super().__init__()
            return None
        form = CHORD_FORM_ABBR_BIDICT.inverse[abbr_form]
        chord_interval = CHORD_INTERVAL_FORM_BIDICT.inverse[form]

        chord_dictionary = (
            MAJOR_CHORD_FINDER_DICT
            if scale.is_major
            else MINOR_CHORD_FINDER_DICT
        )
        possible_chord = []
        if chord_interval in chord_dictionary:
            possible_chord = chord_dictionary[chord_interval]

        numeral: str = "?"
        for c in possible_chord:
            if c["tonic_interval"] == tonic_interval:
                numeral = c["chord"]
                break

        super().__init__(scale, numeral)
        # self.root = root_note  # record only
        # self.form = form  # record only


if __name__ == "__main__":
    c = Scale("D", 0, True)
    g = Scale("G", 0, True)
    x = Chord(c, numeral="I")
    y = Chord(g, numeral="V7")
    # j = JazzChord(g, "C", "")
    # print(x.is_equal(y))
    # print(x.is_equal(y, True))
    # print(x.is_equal(y, True, True))
    # print(x.is_equal(y, False, True))
    # print(j.get_jazz_representation())
