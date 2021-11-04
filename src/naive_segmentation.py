# from ..ChordNoteTickStart.constant import MAJOR_SEMITONE_CUMULATIVE_PATTERN
from Music21Utils.music21_utility import *
from utility import note_name_simplifier
from constant import NOTES_VARIATION_THRESHOLD
from metric import *


def segmentation(chordify_stream, time_signature):
    segments = []
    for measure in chordify_stream.recurse().getElementsByClass("Measure"):
        measure_offset = measure.offset
        chords = measure.recurse().getElementsByClass("Chord")
        if len(chords) > 0:
            # notes[0].addLyric(str("x"))
            for chord in chords:
                # uniform segmentation
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


def merge_segment(segments):
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
