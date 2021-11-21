import numpy as np
from utility.constant import KEY_PROFILE_DICTIONARY
from collections import Counter


def select_key_profile(profile="Aarden-Essen"):
    return KEY_PROFILE_DICTIONARY[profile]


# Key finding algo.
def find_key(measure_chromagram, need_all=False):
    major_profile, minor_profile = select_key_profile()
    mean_chromagram = np.mean(measure_chromagram)

    def get_correlation_values(is_major):
        scale_profile = major_profile if is_major else minor_profile
        mean_scale = np.mean(scale_profile)
        value_scales = []

        coverage = range(12)

        for idx in coverage:
            rolled_chromagram = np.roll(measure_chromagram, -1 * idx)
            corr_value_numerator = np.sum(
                (rolled_chromagram - mean_chromagram) * (scale_profile - mean_scale)
            )
            corr_value_denominator = np.sqrt(
                np.sum((rolled_chromagram - mean_chromagram) ** 2)
                * np.sum((scale_profile - mean_scale) ** 2)
            )
            correlation_value = corr_value_numerator / corr_value_denominator
            value_scales.append((correlation_value, idx, is_major))
        return value_scales

    all_keys_corr_values = get_correlation_values(True) + get_correlation_values(False)
    if need_all:
        return all_keys_corr_values
    else:
        possible_key = max(all_keys_corr_values, key=lambda i: i[0])[1:]
        return possible_key


# determine the key by consider that measure only
# measures_dictionary = return of key_segmentation
def determine_key_solo(measures_dictionary):
    res = []
    for idx, segment in measures_dictionary.items():
        measure_offset = measures_dictionary[idx]["offset"]
        correlation_values = find_key(segment["chroma"], True)
        correlation_values.sort(key=lambda tup: tup[0], reverse=True)
        res.append({"offset": measure_offset, "corr_values": correlation_values})
    return res


# determine the key of the measures in 3 layers
# measures_dictionary = return of key_segmentation
def determine_key_by_adjacent(measures_dictionary):
    queue = []
    measures_possible_key = {}
    two_measures_chroma = np.zeros(12)
    four_measures_chroma = np.zeros(12)

    # identification of keys
    for idx, segment in measures_dictionary.items():
        chroma = segment["chroma"]
        queue.append(segment["chroma"])

        # Determine key within ONE measure
        key_1_measure = find_key(chroma)
        measures_possible_key[idx] = [key_1_measure]

        two_measures_chroma += chroma
        four_measures_chroma += chroma

        # Determine key within TWO measures
        if len(queue) >= 2:
            key_2_measure = find_key(two_measures_chroma)
            for i in range(idx, idx - 2, -1):
                measures_possible_key[i].append(key_2_measure)
            two_measures_chroma -= queue[0]

        # Determine key within FOUR measures
        if len(queue) == 4:
            key_4_measure = find_key(four_measures_chroma)
            for i in range(idx, idx - 4, -1):
                measures_possible_key[i].append(key_4_measure)
            old_measure_chroma = queue.pop(0)
            four_measures_chroma -= old_measure_chroma

    # selection of key
    measures_key = []
    for idx, keys in measures_possible_key.items():
        occurrence_frequency = Counter(keys)
        for k in occurrence_frequency.keys():
            occurrence_frequency[k] = occurrence_frequency[k] / len(keys)

        measure_offset = measures_dictionary[idx]["offset"]
        # Here assume if 2 keys having same count, choose key_1_measure -> key_2_measure -> key_4_measure
        # measures_key[measure_offset] = occurrence_count.most_common(1)[0][0] # give the common one
        measures_key.append(
            {"offset": measure_offset, "frequency": occurrence_frequency.items()}
        )
    # print(measures_key)
    return measures_key
