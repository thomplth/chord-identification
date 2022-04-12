from utility.entities import OffsetPitchScaleCorrelationValues, OffsetNoteProfile
from utility.chord_constant import (
    MAJOR_CHORD_FREQUENCY_DICT,
    MINOR_CHORD_FREQUENCY_DICT,
)
from preprocess.chord import Chord
from preprocess.scale import Scale
from statistics import median


def find_scale_in_chord_segment(
    keys: OffsetPitchScaleCorrelationValues, chord_segment: OffsetNoteProfile
):
    # print(keys)
    # print(chord_segment)
    scale_score_dict = dict(keys[0]["corr_values"])

    offset = chord_segment["offset"]

    for key in keys:
        if offset < key["offset"]:
            break
        scale_score_dict = dict(key["corr_values"])

    return scale_score_dict


def calculate_choice_scores(key_dict, chord: Chord, base_score: float):
    roman = chord.numeral
    scale = chord.scale.get_pitch_scale()
    if not scale in key_dict:
        return {"chord": chord, "score": 0}
    chord_score = (
        MAJOR_CHORD_FREQUENCY_DICT[roman]
        if scale[1]  # is_major
        else MINOR_CHORD_FREQUENCY_DICT[roman]
    )
    chord_score = 1
    return {"chord": chord, "score": base_score * key_dict[scale] * chord_score}


def determine_chord(keys, chords):
    res = []
    for chord in chords:
        offset = chord["offset"]
        # KeyAndChordMode
        if not keys == None:
            scale_score_dict = find_scale_in_chord_segment(keys, chord)

            scores_chords = [
                calculate_choice_scores(
                    scale_score_dict,
                    possible_chord["chord"],
                    possible_chord["similarity_score"],
                )
                for possible_chord in chord["chords"]
            ]
            # TODO: debug
            # ignore if cannot find a chord with a key
            if len(scores_chords) > 0:
                scores_chords.sort(key=lambda i: i[0], reverse=True)
                chord_score, chosen_chord = scores_chords[0]
                res.append(
                    {"offset": offset, "chord": chosen_chord, "score": chord_score}
                )
        # KeyThenChordMode
        else:
            # ignore if cannot find a chord with a key
            if len(chord["chords"]) > 0:
                possible_chord = max(
                    chord["chords"], key=lambda item: item["similarity_score"]
                )
                key_score = median(
                    [
                        option["similarity_score"]
                        for option in chord["chords"]
                        if option["chord"].scale.is_equal(possible_chord["chord"].scale)
                    ]
                )
                # key_score = possible_chord[1]
                res.append(
                    {
                        "offset": offset,
                        "chord": possible_chord["chord"],
                        "score": key_score,
                    }
                )
    # print(res)
    return res
