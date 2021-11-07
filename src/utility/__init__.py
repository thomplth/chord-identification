from preprocess.note import Note

# Convert the note inputted in string to a Note object
def note_input_convertor(input_note_str):
    note_name = input_note_str[0].upper()
    note_accidental = input_note_str[1:]
    # Use # for sharp and - for flat (align with music21)
    return Note(note_name, note_accidental.count("#") - note_accidental.count("-"))


# Convert Music21.note.Note to note string
def note_name_simplifier(m21_notes, is_unique=True):
    m21_notes_names = [m21_note.name for m21_note in m21_notes]
    if is_unique:
        unique_notes_names = list(set(m21_notes_names))
        return unique_notes_names
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
