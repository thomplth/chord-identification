from utility.constant import (
    MAJOR_CHORD_FREQUENCY_DICTIONARY,
    MINOR_CHORD_FREQUENCY_DICTIONARY,
)
from statistics import mean


def find_scale_in_chord_segment(keys, chord_segment):
    scale_score_dict = dict(keys[0]["corr_values"])

    offset = chord_segment[0]

    for key in keys:
        if offset < key["offset"]:
            break
        scale_score_dict = dict(key["corr_values"])

    return scale_score_dict


def calculate_choice_scores(key_dict, chord, base_score):
    roman = chord["chord"]
    scale = chord["scale"].get_pitch_scale()
    if not scale in key_dict:
        return (0, chord)
    chord_score = (
        MAJOR_CHORD_FREQUENCY_DICTIONARY[roman]
        if scale[1]
        else MINOR_CHORD_FREQUENCY_DICTIONARY[roman]
    )
    chord_score = 1
    return (base_score * key_dict[scale] * chord_score, chord)


def determine_chord(keys, chords):
    if not keys == None:
        res = []

        for chord in chords:
            offset = chord[0]
            scale_score_dict = find_scale_in_chord_segment(keys, chord)

            scores_chords = [
                calculate_choice_scores(
                    scale_score_dict, possible_chord[0], possible_chord[1]
                )
                for possible_chord in chord[1]
            ]
            # ignore if cannot find a chord with a key
            if len(scores_chords) > 0:
                scores_chords.sort(key=lambda i: i[0], reverse=True)
                chord_score, chosen_chord = scores_chords[0]
                res.append(
                    {"offset": offset, "chord": chosen_chord, "score": chord_score}
                )
    else:
        res = []
        for chord in chords:
            offset = chord[0]
            # ignore if cannot find a chord with a key
            if len(chord[1]) > 0:
                possible_chord = max(chord[1], key=lambda item: chord[1])
                key_score = mean(
                    [
                        score
                        for key, score in chord[1]
                        if key["scale"].is_equal(possible_chord[0]["scale"])
                    ]
                )
                # key_score = possible_chord[1]
                res.append(
                    {
                        "offset": offset,
                        "chord": possible_chord[0],
                        "score": key_score,
                    }
                )
        # print(res)

    return res
