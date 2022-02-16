if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from utility.m21_utility import *
from utility import note_input_convertor
from utility.entities import (
    Note_duration_dict,
    Measure_OffsetChroma_dict,
    OffsetNoteProfile,
)
from utility.constant import NOTES_VARIATION_THRESHOLD, NOTES_FREQUENCY_THRESHOLD
import numpy as np


# normalization of note dictionary
def normalize_note_dictionary(notes_dict: Note_duration_dict) -> Note_duration_dict:
    total = sum(notes_dict.values())
    normalized_dict: Note_duration_dict = notes_dict.copy()
    for note in normalized_dict.keys():
        normalized_dict[note] = normalized_dict[note] / total
    return normalized_dict


# sum up two note dictionary
def sum_note_dictionary(
    notes_dictionary_1: Note_duration_dict, notes_dictionary_2: Note_duration_dict
) -> Note_duration_dict:
    new_notes_dict: Note_duration_dict = notes_dictionary_1.copy()
    for key, value in notes_dictionary_2.items():
        if not key in new_notes_dict:
            new_notes_dict[key] = 0
        new_notes_dict[key] = value
    return new_notes_dict


# top-down approach of chord segmentation
def uniform_segmentation(chordify_stream, time_signature) -> list[OffsetNoteProfile]:
    offsets_notes_dictionary: dict[float, dict[str, float]] = {}

    for measure_offset, notes in chordify_stream.items():
        # duration calculation
        for m21_note in notes:
            name: str = m21_note.name
            note_offset: float = int(m21_note.offset) + measure_offset
            duration: float = m21_note.duration.quarterLength

            if duration > 0:
                if not (note_offset in offsets_notes_dictionary):
                    offsets_notes_dictionary[note_offset] = {}
                if not (name in offsets_notes_dictionary[note_offset]):
                    offsets_notes_dictionary[note_offset][name] = 0
                offsets_notes_dictionary[note_offset][name] += duration
                # no normalization

    offsets_notes_list: list[OffsetNoteProfile] = [
        {"note_profile": notes_dict, "offset": offset}
        for offset, notes_dict in offsets_notes_dictionary.items()
    ]

    return offsets_notes_list


def is_excess_notes_variation(notes_dictionary: Note_duration_dict) -> bool:
    # First normalization the notes dictionary
    normalized_notes_dict: Note_duration_dict = normalize_note_dictionary(
        notes_dictionary
    )
    notes = list(normalized_notes_dict.items())
    # Then sort acc. to the ranking
    notes.sort(key=lambda tup: tup[1], reverse=True)

    # The variation does not excess if:
    return not (
        (
            # too few notes, OR
            len(notes) <= NOTES_VARIATION_THRESHOLD
            # the notes distribution is satisfied
            or (
                notes[NOTES_VARIATION_THRESHOLD - 1][1] >= NOTES_FREQUENCY_THRESHOLD
                and notes[NOTES_VARIATION_THRESHOLD][1] < NOTES_FREQUENCY_THRESHOLD
            )
        )
    )


# bottom-up approach of chord segmentation, segments = return of uniform_segmentation()
def merge_chord_segment(segments: list[OffsetNoteProfile]):
    res: list[OffsetNoteProfile] = [segments[0]]
    for idx in range(1, len(segments)):
        previous_segment = res.pop()
        current_segment = segments[idx]

        # print("###", previous_segment, current_segment)
        # combine the previous segment if the total variation of notes of two segments are fewer than the threshold
        merged_segment = sum_note_dictionary(
            previous_segment["note_profile"], current_segment["note_profile"]
        )
        if not is_excess_notes_variation(merged_segment):
            res.append(
                {"note_profile": merged_segment, "offset": previous_segment["offset"]}
            )
        # else don't combine
        else:
            res.extend([previous_segment, current_segment])
    # normalize all segments at last
    for ele in res:
        ele["note_profile"] = normalize_note_dictionary(ele["note_profile"])
    return res


# Steedman means whether the output vector is flatten
def create_chroma(partial_stream, steedman=False) -> list[float]:
    pitch_class: list[float] = [0.0 for _ in range(12)]
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
            name: str = m21_note.name
            duration: float = m21_note.duration.quarterLength
            note_class = note_input_convertor(name).get_pitch_class()
            # adding pitch duration is the ordinary Krumhansl-Schmuckler approach
            pitch_class[note_class] += duration

    # flatten vector for Longuet-Higgins and Steedman's approach
    if steedman:
        return [(1.0 if pitch > 0 else 0.0) for pitch in pitch_class]

    return pitch_class


# for each measure return the chromagram of the measure
def key_segmentation(stream) -> Measure_OffsetChroma_dict:
    result: Measure_OffsetChroma_dict = {}
    for measure in get_measures(stream):
        idx = measure.number
        np_chroma = np.array(create_chroma(measure))

        # map the same measure in different stream into the same vector
        if idx in result:
            result[idx]["chroma"] += np_chroma
        else:
            result[idx] = {"chroma": np_chroma, "offset": measure.offset}

    return result