if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from utility.m21_utility import *
from utility.entities import (
    Note_duration_dict,
    Measure_OffsetChroma_dict,
    OffsetNoteProfile,
)
from utility.constant import NOTES_VARIATION_THRESHOLD, NOTES_FREQUENCY_THRESHOLD
from preprocess.note import Note
from segmentation.ml_models_classification import (
    determine_valid_combined_segment_by_tree,
)
import numpy as np
from math import log2


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
# def uniform_segmentation(chordify_stream) -> list[OffsetNoteProfile]:
#     offsets_notes_dictionary: dict[float, dict[str, float]] = {}

#     for measure_offset, notes in chordify_stream.items():
#         # duration calculation
#         for m21_note in notes:
#             name: str = m21_note.name
#             note_offset: float = int(m21_note.offset) + measure_offset
#             duration: float = m21_note.duration.quarterLength

#             if duration > 0:
#                 if not (note_offset in offsets_notes_dictionary):
#                     offsets_notes_dictionary[note_offset] = {}
#                 if not (name in offsets_notes_dictionary[note_offset]):
#                     offsets_notes_dictionary[note_offset][name] = 0
#                 offsets_notes_dictionary[note_offset][name] += duration
#                 # no normalization

#     offsets_notes_list: list[OffsetNoteProfile] = [
#         {"note_profile": notes_dict, "offset": offset}
#         for offset, notes_dict in offsets_notes_dictionary.items()
#     ]


def generate_note_profiles_in_segments(notes_in_segments: dict):
    offsets_notes_dictionary: dict[float, dict[str, float]] = {}
    for offset, m21_notes in notes_in_segments.items():
        for m21_note in m21_notes:
            name: str = m21_note.name
            duration: float = m21_note.duration.quarterLength

            if duration > 0:
                if not (offset in offsets_notes_dictionary):
                    offsets_notes_dictionary[offset] = {}
                if not (name in offsets_notes_dictionary[offset]):
                    offsets_notes_dictionary[offset][name] = 0
                offsets_notes_dictionary[offset][name] += duration
                # no normalization

    offsets_notes_list: list[OffsetNoteProfile] = [
        {"note_profile": notes_dict, "offset": offset}
        for offset, notes_dict in offsets_notes_dictionary.items()
    ]

    return offsets_notes_list


def get_notes_in_segments(stream, segment_unit=1.0):
    measures = get_measures(stream)
    res = {}
    for measure in measures:
        for element in list(measure.elements):
            m21_notes = []
            # harmony.ChordSymbol is inherited from chord.Chord but it is just repeated the chord
            # so they should be ignored
            if isinstance(element, chord.Chord) and not (
                isinstance(element, harmony.ChordSymbol)
            ):
                m21_notes_temp = list(element.notes)
                # the offset of notes in chord is relative to chord
                for n in m21_notes_temp:
                    n.offset += element.offset
                m21_notes.extend(m21_notes_temp)
            elif isinstance(element, note.Note):
                m21_notes.append(element)
            else:
                continue

            offset = m21_notes[0].offset
            index = measure.offset + floor(offset / segment_unit) * segment_unit
            if index in res:
                res[index].extend(m21_notes)
            else:
                res[index] = m21_notes
    return res


def is_valid_note_profile(notes_dictionary: Note_duration_dict) -> bool:
    # First normalization the notes dictionary
    normalized_notes_dict: Note_duration_dict = normalize_note_dictionary(
        notes_dictionary
    )
    notes = list(normalized_notes_dict.items())
    # Then sort acc. to the ranking
    notes.sort(key=lambda tup: tup[1], reverse=True)

    # In Phase I: The variation does not excess if:
    # return not (
    #     (
    #         # too few notes, OR
    #         len(notes) <= NOTES_VARIATION_THRESHOLD
    #         # the notes distribution is satisfied
    #         or (
    #             notes[NOTES_VARIATION_THRESHOLD - 1][1] >= NOTES_FREQUENCY_THRESHOLD
    #             and notes[NOTES_VARIATION_THRESHOLD][1] < NOTES_FREQUENCY_THRESHOLD
    #         )
    #     )
    # )

    # In Phase II: The variation does not excess if
    # the notes distribution is satisfied: check the normalized value of the pitch class in rank \theta{nv}
    return (
        len(notes) < NOTES_VARIATION_THRESHOLD
        or notes[NOTES_VARIATION_THRESHOLD - 1][1] <= NOTES_FREQUENCY_THRESHOLD
    )


# bottom-up approach of chord segmentation, segments = return of uniform_segmentation()
def merge_chord_segment(segments: list[OffsetNoteProfile], models):
    res: list[OffsetNoteProfile] = [segments[0]]
    for idx in range(1, len(segments)):
        previous_segment = res.pop()
        current_segment = segments[idx]

        # print("###", previous_segment, current_segment)
        # combine the previous segment if the total variation of notes of two segments are fewer than the threshold
        merged_segment = sum_note_dictionary(
            previous_segment["note_profile"], current_segment["note_profile"]
        )
        is_valid: bool = is_valid_note_profile(merged_segment)
        if models is not None:
            is_valid = determine_valid_combined_segment_by_tree(
                note_profile=merged_segment,
                rule_based_result=is_valid,
                models = models
            )
        if is_valid_note_profile(merged_segment):
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
            note_class = Note(input_str=name).get_pitch_class()
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


def get_segment_unit(stream) -> float:
    min_length = float("inf")
    for measure in get_measures(stream):
        for element in list(flatten(measure).elements):
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
                duration: float = m21_note.duration.quarterLength
                if duration > 0 and duration < min_length:
                    if log2(duration).is_integer():
                        min_length = duration
    # print(f"min_length: {min_length}")
    return min_length