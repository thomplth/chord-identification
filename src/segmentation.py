# from ..ChordNoteTickStart.constant import MAJOR_SEMITONE_CUMULATIVE_PATTERN
from Music21Utils.music21_utility import *
import music21
from utility import note_name_simplifier, note_input_convertor
from constant import NOTES_VARIATION_THRESHOLD
from metric import *


def uniform_segmentation(chordify_stream, time_signature):
    segments = []
    for measure in chordify_stream.recurse().getElementsByClass("Measure"):
        measure_offset = measure.offset
        chords = measure.recurse().getElementsByClass("Chord")
        if len(chords) > 0:
            # notes[0].addLyric(str("x"))
            for chord in chords:
                mark = int(chord.offset) - chord.offset % time_signature.numerator == 0
                chord_offset = measure_offset + int(chord.offset)

                notes = list(chord.notes)
                if not mark:
                    same_segment = segments.pop()
                    notes = same_segment[1] + notes

                segments.append((chord_offset, notes))

    return [(segment[0], note_name_simplifier(segment[1])) for segment in segments]


def notes_variation(notes):
    return len(list(set(notes)))


def merge_chord_segment(segments):
    res = [segments[0]]
    for idx in range(1, len(segments)):
        previous_segment = res.pop()
        current_segment = segments[idx]
        if (
            notes_variation(previous_segment[1] + current_segment[1])
            <= NOTES_VARIATION_THRESHOLD
        ):
            res.append(
                (
                    previous_segment[0],
                    list(set(previous_segment[1] + current_segment[1])),
                )
            )
        else:
            res.append(previous_segment)
            res.append(current_segment)

    return res


# Steedman means flatten the output vector
def chromagram(partial_stream, steedman=False):
    pitch_class = [0.0 for _ in range(12)]
    for element in list(flatten(partial_stream).elements):
        m21_notes = []
        # harmony.ChordSymbol is inherited from chord.Chord but it is just repeated the chord
        if isinstance(element, chord.Chord) and not isinstance(
            element, harmony.ChordSymbol
        ):
            m21_notes = list(element.notes)
        elif isinstance(element, note.Note):
            m21_notes = [element]
        else:
            continue

        for m21_note in m21_notes:
            name = m21_note.name
            duration = m21_note.duration.quarterLength
            note_class = note_input_convertor(name).get_pitch_class()
            pitch_class[note_class] += duration

    # flatten vector
    if steedman:
        return [(1.0 if pitch > 0 else 0.0) for pitch in pitch_class]

    return pitch_class


# for each measure return the chromagram of the measure
def key_segmentation(stream):
    result = []
    for measure in get_measures(stream):
        chroma = chromagram(measure)
        # TODO: map the same measure in different stream into the same vector
        result.append(chroma)
    return result