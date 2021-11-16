import numpy as np
from collections import Counter


def select_key_profile(profile="Temperley"):
    if profile == "Krumhansl-Kessler":
        return np.array(
            [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
        ), np.array(
            [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
        )
    elif profile == "Temperley":
        return (
            np.array([5.0, 2.0, 3.5, 2.0, 4.5, 4.0, 2.0, 4.5, 2.0, 3.5, 1.5, 4.0]),
            np.array([5.0, 2.0, 3.5, 4.5, 2.0, 4.0, 2.0, 4.5, 3.5, 2.0, 1.5, 4.0]),
        )
    else:  # Longuet-Higgins/ Steedman a.k.a. flatten key profile
        return (
            np.array([1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0]),
            np.array([1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.5, 0.5]),
        )


# Key finding algo.
def find_key(measure_chromagram):
    major_profile, minor_profile = select_key_profile()
    # max_3_indices = np.argpartition(measure_chromagram, -3)[-3:]

    mean_chromagram = np.mean(measure_chromagram)

    def get_correlation_values(is_major, isFast=False):
        scale_profile = major_profile if is_major else minor_profile
        mean_scale = np.mean(scale_profile)
        value_scales = []

        coverage = range(12)  # []
        # if efficiency is a concern, we only do max of 9 instead of 12
        # if isFast:
        # choose C, E (Eb for minor), G
        # pitches_class = list(max_3_indices)
        # coverage = pitches_class + [(pitch + 7) % 12 for pitch in pitches_class]
        # if is_major:
        #     coverage = coverage + [(pitch + 4) % 12 for pitch in pitches_class]
        # else:
        #     coverage = coverage + [(pitch + 3) % 12 for pitch in pitches_class]
        # coverage = list(set(coverage))
        # else:
        #     coverage = range(12)

        for idx in coverage:
            rolled_chromagram = np.roll(measure_chromagram, -1 * idx)
            correlation_value_numerator = np.sum(
                (rolled_chromagram - mean_chromagram) * (scale_profile - mean_scale)
            )
            correlation_value_denominator = np.sqrt(
                np.sum((rolled_chromagram - mean_chromagram) ** 2)
                * np.sum((scale_profile - mean_scale) ** 2)
            )
            correlation_value = (
                correlation_value_numerator / correlation_value_denominator
            )
            value_scales.append((correlation_value, idx, is_major))
        return value_scales

    possible_key = max(
        get_correlation_values(True) + get_correlation_values(False), key=lambda i: i[0]
    )[1:]
    return possible_key


# determine the key of the measures in 3 layers
# measures_dictionary = return of key_segmentation
def determine_key(measures_dictionary):
    queue = []
    measures_possible_key = {}
    two_measures_chroma = np.zeros(12)
    four_measures_chroma = np.zeros(12)

    # identification of keys
    for idx, chroma in measures_dictionary.items():
        queue.append(idx)

        # Determine key within ONE measure
        key_1_measure = find_key(chroma)
        measures_possible_key[idx] = [key_1_measure]

        two_measures_chroma += chroma
        four_measures_chroma += chroma

        # Determine key within TWO measures
        if len(queue) >= 2:
            key_2_measure = find_key(two_measures_chroma)
            for i in queue:
                measures_possible_key[i].append(key_2_measure)
            # old_measure_idx = queue.pop(0)
            two_measures_chroma -= measures_dictionary[queue[0]]

        # Determine key within FOUR measures
        if len(queue) == 4:
            key_4_measure = find_key(four_measures_chroma)
            for i in queue:
                measures_possible_key[i].append(key_4_measure)
            old_measure_idx = queue.pop(0)
            four_measures_chroma -= measures_dictionary[old_measure_idx]

    # selection of key
    measures_key = {}
    for idx, keys in measures_possible_key.items():
        occurrence_count = Counter(keys)
        # Here assume if 2 keys having same count, choose key_1_measure -> key_2_measure -> key_4_measure
        measures_key[idx] = occurrence_count.most_common(1)[0][0]
    return measures_key
