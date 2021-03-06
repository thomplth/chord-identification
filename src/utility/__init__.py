from utility.constant import *
import os

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


def get_files(directory, suffix, filename=None):
    all_scores = [f for f in os.listdir(directory) if f.endswith(suffix)]
    if filename in all_scores:
        return [filename]
    return all_scores