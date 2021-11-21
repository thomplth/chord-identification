if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))


from preprocess.note import Note


class Scale:
    def __init__(
        self, tonic_alphabet="?", tonic_accidental=0, is_major=True, tonic_note=None
    ):
        self.tonic = (
            Note(tonic_alphabet, tonic_accidental) if tonic_note == None else tonic_note
        )
        self.is_major = is_major

    # determine if two notes are equal
    def is_equal(self, other_scale):
        return (self.tonic.is_equal(other_scale.tonic)) and (
            self.is_major == other_scale.is_major
        )

    # Use string format to represent the note
    def scale_str(self, isPrintedInDos=False):
        scale_mode = "Major" if self.is_major else "Minor"
        tonic_str = self.tonic.note_str(isPrintedInDos)
        tonic_str = tonic_str.upper() if self.is_major else tonic_str.lower()
        result = tonic_str + " " + scale_mode
        return result

    # Give its relative scale of a scale
    def get_relative_scale(self):
        if self.is_major:
            relative_tonic = self.tonic.get_note_by_interval("M6")
        else:
            relative_tonic = self.tonic.get_note_by_interval("m3")

        return Scale(tonic_note=relative_tonic, is_major=not self.is_major)

    # sometime we are just interested in the pitch of the tonic
    def get_pitch_scale(self):
        return (self.tonic.get_pitch_class(), self.is_major)


if __name__ == "__main__":
    s = Scale("E", -1, True)
    print(s.scale_str())
    u = s.get_relative_scale()
    print(u.scale_str())
    t = Scale("C", 0, False)
    print(u.is_equal(t))
