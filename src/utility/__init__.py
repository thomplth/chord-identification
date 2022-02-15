from preprocess.note import Note
from utility.constant import *

# Convert the note inputted in string to a Note object
def note_input_convertor(input___str__):
    note_name = input___str__[0].upper()
    note_accidental = input___str__[1:]
    # Use # for sharp and - for flat (align with music21)
    # also use "b" for flat. Suppose it is invalid to exist "-" and "b" for flat as the same time
    return Note(
        note_name,
        note_accidental.count("#")
        - note_accidental.count("-")
        - note_accidental.count("b"),
    )


# Convert Music21.note.Note to note string
def note_name_simplifier(m21_notes, is_unique=True):
    m21_notes_names = [m21_note.name for m21_note in m21_notes]
    if is_unique:
        return list(set(m21_notes_names))
    else:
        return m21_notes_names


# Convert Music21.note.Note to Custom Note object
def note_object_simplifier(m21_notes):
    unique_notes_names = note_name_simplifier(m21_notes)
    return [note_input_convertor(note) for note in unique_notes_names]


# Get the invert interval from an interval
def invert_interval(interval):
    quality = interval[0]
    distance = interval[1]
    if distance == "1":
        return interval
    new_quality = quality
    if quality == "M":
        new_quality = "m"
    elif quality == "m":
        new_quality = "M"
    elif quality == "A":
        new_quality = "d"
    elif quality == "d":
        new_quality = "A"
    new_distance = str((9 - int(distance)))
    return new_quality + new_distance


from typing import TypedDict
import numpy as np

# note dict: note name -> duration
Note_duration_dict = dict[str, float]


class OffsetChroma(TypedDict):
    chroma: np.ndarray
    offset: float


class OffsetNoteProfile(TypedDict):
    note_profile: Note_duration_dict
    offset: float


Measure_OffsetChroma_dict = dict[int, OffsetChroma]

Pitch_scale = tuple[int, bool]


class PitchScaleCorrelationValue(TypedDict):
    pitch_scale: Pitch_scale
    corr_val: float


class OffsetPitchScaleCorrelationValues(TypedDict):
    offset: float
    corr_values: list[PitchScaleCorrelationValue]
