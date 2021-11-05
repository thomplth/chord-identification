# from ..ChordNoteTickStart.constant import MAJOR_SEMITONE_CUMULATIVE_PATTERN
from Music21Utils.music21_utility import *
from utility import note_name_simplifier, note_input_convertor
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


def chromagram(chordify_partial_stream):
    pitch_class = [0 for i in range(12)]
    for measure in chordify_partial_stream.recurse().getElementsByClass("Measure"):
        chords = measure.recurse().getElementsByClass("Chord")
        if len(chords) > 0:
            for chord in chords:
                notes = list(chord.notes)
                notes_names = note_name_simplifier(notes, False)
                for name in notes_names:
                    note_class = note_input_convertor(name).get_pitch_class()
                    pitch_class[note_class] += 1
        # print(measure, pitch_class)

    return pitch_class