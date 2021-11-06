# from ..ChordNoteTickStart.constant import MAJOR_SEMITONE_CUMULATIVE_PATTERN
from Music21Utils.music21_utility import *
import music21
from utility import note_name_simplifier, note_input_convertor
from constant import NOTES_VARIATION_THRESHOLD
from metric import *

# top-down approach of chord segmentation
def uniform_segmentation(chordify_stream, time_signature):
    segments = []
    for measure in chordify_stream.recurse().getElementsByClass("Measure"):
        measure_offset = measure.offset
        chords = measure.recurse().getElementsByClass("Chord")
        if len(chords) > 0:
            # notes[0].addLyric(str("x"))
            for chord in chords:
                # mark if the chords are on beat
                mark = int(chord.offset) - chord.offset % time_signature.numerator == 0
                chord_offset = measure_offset + int(chord.offset)

                notes = list(chord.notes)
                # if the chord is not on beat, merge the chord with the previous on beat chord
                if not mark:
                    same_segment = segments.pop()
                    notes = same_segment[1] + notes

                segments.append((chord_offset, notes))
    # the return is the list of the tuple of (segment offset, [lists of note names (NOT Note object)])
    return [(segment[0], note_name_simplifier(segment[1])) for segment in segments]


# define note variation as the number of pitch class of a set of notes
def notes_variation(notes):
    return len(list(set(notes)))


# bottom-up approach of chord segmentation, segments = return of uniform_segmentation()
def merge_chord_segment(segments):
    res = [segments[0]]
    for idx in range(1, len(segments)):
        previous_segment = res.pop()
        current_segment = segments[idx]
        # combine the previous segment if the total variation of notes of two segments are fewer than the threshold
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
        # else don't combine
        else:
            res.append(previous_segment)
            res.append(current_segment)

    return res


# Steedman means whether the output vector is flatten
def chromagram(partial_stream, steedman=False):
    pitch_class = [0.0 for _ in range(12)]
    for element in list(flatten(partial_stream).elements):
        m21_notes = []
        # harmony.ChordSymbol is inherited from chord.Chord but it is just repeated the chord
        # so they should be ignored
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
            # adding pitch duration is the ordinary Krumhansl-Schmuckler approach
            pitch_class[note_class] += duration

    # flatten vector for Longuet-Higgins and Steedman's approach
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