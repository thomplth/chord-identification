if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

# from ..ChordNoteTickStart.constant import MAJOR_SEMITONE_CUMULATIVE_PATTERN
from utility.m21_utility import *
import music21
from utility import note_name_simplifier, note_input_convertor
from utility.constant import NOTES_VARIATION_THRESHOLD, NOTES_FREQUENCY_THRESHOLD
import numpy as np

# top-down approach of chord segmentation
def uniform_segmentation(chordify_stream, time_signature):
    def old():
        segments = []
        for measure in chordify_stream.recurse().getElementsByClass("Measure"):
            measure_offset = measure.offset
            chords = measure.recurse().getElementsByClass("Chord")
            if len(chords) > 0:
                # notes[0].addLyric(str("x"))
                for chord in chords:
                    # mark if the chords are on beat
                    mark = (
                        int(chord.offset) - chord.offset % time_signature.numerator == 0
                    )
                    chord_offset = measure_offset + int(chord.offset)

                    notes = list(chord.notes)
                    # if the chord is not on beat, merge the chord with the previous on beat chord
                    if not mark:
                        same_segment = segments.pop()
                        notes = same_segment[1] + notes

                    segments.append((chord_offset, notes))
        # the return is the list of the tuple of (segment offset, [lists of note names (NOT Note object)])
        return [(segment[0], note_name_simplifier(segment[1])) for segment in segments]

    def new():
        res = []
        for measure_offset, notes in chordify_stream.items():
            offsets_notes_dictionary = {}
            # duration calculation
            for m21_note in notes:
                name = m21_note.name
                note_offset = int(m21_note.offset) + measure_offset
                duration = m21_note.duration.quarterLength
                if duration > 0:
                    if not (note_offset in offsets_notes_dictionary):
                        offsets_notes_dictionary[note_offset] = {}
                    if not (name in offsets_notes_dictionary[note_offset]):
                        offsets_notes_dictionary[note_offset][name] = 0
                    offsets_notes_dictionary[note_offset][name] += duration

            # normalization
            for offset in offsets_notes_dictionary.keys():
                total = sum(offsets_notes_dictionary[offset].values())
                for note in offsets_notes_dictionary[offset].keys():
                    offsets_notes_dictionary[offset][note] = (
                        offsets_notes_dictionary[offset][note] / total
                    )

            res.extend(list(offsets_notes_dictionary.items()))
        res.sort(key=lambda tup: tup[0])
        return res

    return new()


# define note variation as the number of pitch class of a set of notes
def notes_variation(notes_names):
    return len(list(set(notes_names)))


def is_excess_notes_variation(notes_dictionary):
    notes = list(notes_dictionary.items())
    notes.sort(key=lambda tup: tup[1], reverse=True)
    return not (
        (
            len(notes) <= NOTES_VARIATION_THRESHOLD
            or (
                notes[NOTES_VARIATION_THRESHOLD - 1][1] >= NOTES_FREQUENCY_THRESHOLD
                and notes[NOTES_VARIATION_THRESHOLD][1] < NOTES_FREQUENCY_THRESHOLD
            )
        )
    )


def notes_dictionary_sum(notes_dictionary_1, notes_dictionary_2):
    new_notes_dict = notes_dictionary_1.copy()
    for key, value in notes_dictionary_2.items():
        if not key in new_notes_dict:
            new_notes_dict[key] = 0
        new_notes_dict[key] = value
    total = sum(new_notes_dict.values())
    for note in new_notes_dict.keys():
        new_notes_dict[note] = new_notes_dict[note] / total
    return new_notes_dict


# bottom-up approach of chord segmentation, segments = return of uniform_segmentation()
def merge_chord_segment(segments):
    res = [segments[0]]
    for idx in range(1, len(segments)):
        previous_segment = res.pop()
        current_segment = segments[idx]

        def old():
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

        def new():
            # print("###", previous_segment, current_segment)
            # combine the previous segment if the total variation of notes of two segments are fewer than the threshold
            merged_segment = notes_dictionary_sum(
                previous_segment[1], current_segment[1]
            )
            if not is_excess_notes_variation(merged_segment):
                res.append((previous_segment[0], merged_segment))
            # else don't combine
            else:
                res.append(previous_segment)
                res.append(current_segment)

        new()
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
    result = {}
    for measure in get_measures(stream):
        idx = measure.number
        np_chroma = np.array(chromagram(measure))

        # map the same measure in different stream into the same vector
        if idx in result:
            result[idx]["chroma"] += np_chroma
        else:
            result[idx] = {"chroma": np_chroma, "offset": measure.offset}

    return result