from Note import Note

# Convert the note inputted in string to a Note object
def note_input_convertor(input_note_str):
    note_name = input_note_str[0].upper()
    note_accidental = input_note_str[1:]
    # Use # for sharp and - for flat (align with music21)
    return Note(note_name, note_accidental.count("#") - note_accidental.count("-"))


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
