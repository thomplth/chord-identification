from Note import Note
from constant import *


def note_input_convertor(input_note_str):
    note_name = input_note_str[0].upper()
    note_accidental = input_note_str[1:]
    return Note(note_name, note_accidental.count("+") - note_accidental.count("-"))


def get_scale(tonic, is_major):
    scale = [tonic]
    # just follow how a scale is form
    scale_pattern = MAJOR_SEMITONE_PATTERN if is_major else MINOR_SEMITONE_PATTERN
    for semitone in scale_pattern:
        last_note = scale[-1]
        new_note = last_note.get_note_by_major_interval(2)
        if semitone == 1:
            new_note = new_note.modify_accidental(-1)
        scale.append(new_note)
    return scale


# The input is currently error free: No checking is needed
if __name__ == "__main__":
    print("Please input the scale you want. ")
    print("E.g. for F♯ major, type 'F+'. ")
    input_str = input("E.g. for B♭ minor, type 'b-'. ")
    note = note_input_convertor(input_str)
    print("Unison:", note.get_note_by_interval("P", 1).get_note_string())
    is_major = input_str[0].upper() == input_str[0]
    scale = get_scale(note, is_major)
    for note in scale:
        print(note.get_note_string(), end=" ")