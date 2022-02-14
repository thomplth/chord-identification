if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))


from preprocess.note import Note
from utility.chord_constant import MAJOR_CHORD_DICT, MINOR_CHORD_DICT


class Scale:
    def __init__(
        self,
        tonic_alphabet: str = "?",
        tonic_accidental: int = 0,
        is_major: bool = True,
        tonic_note: Note = None,
    ):
        self.tonic = (
            Note(tonic_alphabet, tonic_accidental) if tonic_note is None else tonic_note
        )
        self.is_major = is_major

    def __str__(self):
        scale_mode = "Major" if self.is_major else "Minor"
        tonic_str = self.tonic.__str__()
        tonic_str = tonic_str.upper() if self.is_major else tonic_str.lower()
        result = tonic_str + " " + scale_mode
        return result

    # determine if two scales are equal
    def is_equal(self, other_scale):
        """
        :other_scale: Scale object
        """
        return (self.tonic.is_equal(other_scale.tonic)) and (
            self.is_major == other_scale.is_major
        )

    # # Give its relative scale of a scale
    def get_relative_scale(self):
        transpose_interval = "M6" if self.is_major else "m3"
        relative_tonic = self.tonic.get_note_by_interval(transpose_interval)
        return Scale(tonic_note=relative_tonic, is_major=not self.is_major)

    # sometime we are just interested in the pitch of the tonic
    def get_pitch_scale(self):
        return (self.tonic.get_pitch_class(), self.is_major)

    # get chords dictionary for the scale
    def get_chord_dictionary(self):
        return MAJOR_CHORD_DICT if self.is_major else MINOR_CHORD_DICT


if __name__ == "__main__":
    s = Scale("E", -1, True)
    print(s.__str__())
    u = s.get_relative_scale()
    print(u.__str__())
    t = Scale("C", 0, False)
    print(u.is_equal(t))
