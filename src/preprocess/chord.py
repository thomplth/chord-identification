if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from preprocess.scale import Scale
from preprocess.chord_to_note import pick_chord
from utility.constant import (
    CHORD_FORM_NAME_DICTIONARY,
    CHORD_FORM_INTERVAL_DICTIONARY,
    MAJOR_CHORD_FINDER_DICTIONARY,
    MINOR_CHORD_FINDER_DICTIONARY,
)
from utility import note_input_convertor

# All chords in Chord class are in Roman numeral analysis
class Chord:
    def __init__(self, scale: Scale = None, numeral: str = "?"):
        self.scale: Scale = Scale() if scale is None else scale
        self.numeral: str = numeral
        dictionary = self.scale.get_chord_dictionary()
        self.form: str = "?"
        if numeral in dictionary:
            self.form = CHORD_FORM_NAME_DICTIONARY[tuple(dictionary[numeral][1:])]

    # get the jazz representation of a chord
    def get_jazz_representation(self):
        if self.form == "?":
            return "Undefined"
        dictionary = self.scale.get_chord_dictionary()
        interval = dictionary[self.numeral][0]
        root = self.scale.tonic.get_note_by_interval(interval)
        return root.note_str() + " " + self.form

    # def result_roman_to_jazz(roman, scale_str):
    #     # V+,d Minor
    #     scale_text = scale_str.split()
    #     tonic_str = scale_text[0]
    #     isMajor = scale_text[1] == "Major"

    #     lexicon = MAJOR_CHORD_DICTIONARY if isMajor else MINOR_CHORD_DICTIONARY
    #     root_interval = lexicon[roman][0]
    #     chord_form = CHORD_FORM_NAME_DICTIONARY[tuple(lexicon[roman][1:])]
    #     tonic = note_input_convertor(tonic_str).get_note_by_interval(root_interval)
    #     return tonic.note_str(False) + " " + chord_form
    #     # A Major

    # determine if two chords are equal
    # support neglect seventh note and Jazz chord comparison
    def is_equal(self, other_chord, on_triad: bool = False, on_jazz: bool = False):
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
    def chord_str(self, isPrintedInDos: bool = False):
        scale_str = self.scale.scale_str(isPrintedInDos)
        result = self.numeral + " chord in " + scale_str
        return result


# A child class is made for initialize the Jazz chord easily
class JazzChord(Chord):
    def __init__(self, scale: Scale = None, root: str = "", abbr_form: str = ""):
        root_note = note_input_convertor(root)
        tonic_interval = scale.tonic.get_interval(root_note)

        def translate_form(abbr: str):
            result: str = "?"
            if abbr == "":
                result = "Major"
            elif abbr == "m":
                result = "Minor"
            elif abbr == "dim":
                result = "Diminished"
            elif abbr == "maj7":
                result = "Major seventh"
            elif abbr == "m7":
                result = "Minor seventh"
            elif abbr == "7":
                result = "Dominant seventh"
            elif abbr == "o7":
                result = "Diminished seventh"
            elif abbr == "It":
                result = "Italian sixth"
            elif abbr == "Ger":
                result = "German sixth"
            elif abbr == "Fr":
                result = "French sixth"
            return result

        form = translate_form(abbr_form)
        chord_interval = CHORD_FORM_INTERVAL_DICTIONARY[form]

        chord_dictionary = (
            MAJOR_CHORD_FINDER_DICTIONARY
            if scale.is_major
            else MINOR_CHORD_FINDER_DICTIONARY
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
