from utility.constant import *
from preprocess.note import Note


def get_scale(tonic, is_major):
    scale = [tonic]
    # just follow how a scale is form
    scale_pattern = MAJOR_SEMITONE_PATTERN if is_major else MINOR_SEMITONE_PATTERN
    for semitone in scale_pattern:
        last_note = scale[-1]
        new_note = last_note.get_note_by_interval("M2")
        if semitone == 1:
            new_note.accidental -= 1
        scale.append(new_note)
    return scale


# The input is currently error free: No checking is needed
if __name__ == "__main__":
    print("Please input the scale you want. ")
    print("E.g. for F♯ major, type 'F#'. ")
    input_str = input("E.g. for B♭ minor, type 'b-'. \n")
    note = Note(input_str=input_str)
    print("Unison:", note.get_note_by_interval("P1").__str__())
    is_major = input_str[0].upper() == input_str[0]
    scale = get_scale(note, is_major)
    for note in scale:
        print(note.__str__(), end=" ")
    print()