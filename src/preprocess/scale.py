if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))


from note import Note


class Scale:
    def __init__(
        self, tonic_alphabet="C", tonic_accidental="0", isMajor=True, tonic_note=None
    ):
        self.tonic = (
            Note(tonic_alphabet, tonic_accidental) if tonic_note == None else tonic_note
        )
        self.isMajor = isMajor

    # Use string format to represent the note
    def scale_str(self, isPrintedInDos=True):
        scale_mode = "Major" if self.isMajor else "Minor"
        result = self.tonic.note_str(isPrintedInDos) + " " + scale_mode
        return result

    # Give its relative scale of a scale
    def get_relative_scale(self):
        if self.isMajor:
            relative_tonic = self.tonic.get_note_by_interval("M6")
        else:
            relative_tonic = self.tonic.get_note_by_interval("m3")

        return Scale(tonic_note=relative_tonic, isMajor=not self.isMajor)


# if __name__ == "__main__":
#     s = Scale("E", -1, True)
#     print(s.scale_str())
#     print(s.get_relative_scale().scale_str())
