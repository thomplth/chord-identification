if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from utility.entities import ChordSimilarityScore, Note_duration_dict
from preprocess.note import Note
from itertools import combinations


def determine_chord_tonality_by_tree(chroma, models):
    decision_tree, random_forest = models

    def generate_pitch_class_differences(chroma):
        indices_pairs = list(combinations(range(12), 2))
        chroma_diff = [0.0 for _ in range(len(indices_pairs))]
        for idx in range(len(indices_pairs)):
            a, b = indices_pairs[idx]
            chroma_diff[idx] = round(abs(chroma[a] - chroma[b]), 6)
        return chroma_diff

    pcd = generate_pitch_class_differences(chroma)

    def get_tonalities(one_hot_label):
        if one_hot_label[0]:  # augmented
            return ["Augmented"]
        elif one_hot_label[1]:  # augmented sixth
            return ["Italian sixth", "German sixth", "French sixth"]
        elif one_hot_label[2]:  # diminished
            return ["Diminished", "Diminished seventh", "Half-diminished seventh"]
        elif one_hot_label[3]:  # major
            return ["Major", "Major seventh", "Dominant seventh"]
        elif one_hot_label[4]:  # minor
            return ["Minor", "Minor seventh"]
        else:  # error
            return []

    # The floating pt number = True and False
    result = {}
    scale_modes = zip([True, False], [1.0, 0.0])
    for is_major, fp_num in scale_modes:
        pred_dt = decision_tree.predict([pcd + [fp_num]])[0]
        pred_rf = random_forest.predict([chroma + [fp_num]])[0]
        possible_tonalities = get_tonalities(pred_dt) + get_tonalities(pred_rf)
        result[is_major] = list(set(possible_tonalities))
    return result


def chord_filter_by_tonalities(
    possible_chords: list[ChordSimilarityScore], chord_tonalities_by_scale
):
    filtered_chords = []
    for possible_chord in possible_chords:
        chord_scale = possible_chord["chord"].scale
        chord_tonality = possible_chord["chord"].form
        if chord_tonality in chord_tonalities_by_scale[chord_scale.is_major]:
            filtered_chords.append(possible_chord)
    return filtered_chords
