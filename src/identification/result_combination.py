from utility.constant import (
    MAJOR_CHORD_FREQUENCY_DICTIONARY,
    MINOR_CHORD_FREQUENCY_DICTIONARY,
)


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
    return (base_score * key_dict[scale] * chord_score, chord)


def determine_chord(keys, chords):
    keys_change_num = len(keys)
    key_ptr = 0
    scale_score_dict = dict(keys[0]["corr_values"])
    res = []

    for chord in chords:
        offset = chord[0]
        while key_ptr < keys_change_num - 1 and offset >= keys[key_ptr + 1]["offset"]:
            key_ptr += 1
            scale_score_dict = dict(keys[key_ptr]["corr_values"])

        scores_chords = [
            calculate_choice_scores(
                scale_score_dict, possible_chord[0], possible_chord[1]
            )
            for possible_chord in chord[1]
        ]
        scores_chords.sort(key=lambda i: i[0], reverse=True)

        chord_score, chosen_chord = scores_chords[0]
        res.append({"offset": offset, "chord": chosen_chord, "score": chord_score})

    return res
