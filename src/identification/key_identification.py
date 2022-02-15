import numpy as np
from utility import (
    PitchScaleCorrelationValue,
    Measure_OffsetChroma_dict,
    OffsetPitchScaleCorrelationValues,
)
from utility.constant import KEY_PROFILE_DICT
from collections import Counter


def select_key_profile(profile="Aarden-Essen"):
    return KEY_PROFILE_DICT[profile]


# Key finding algo.
def find_key(
    measure_chromagram: np.ndarray, need_all: bool = False
) -> list[PitchScaleCorrelationValue]:
    major_profile, minor_profile = select_key_profile()
    mean_chromagram: float = np.mean(measure_chromagram)

    def get_correlation_values(is_major: bool) -> list[PitchScaleCorrelationValue]:
        scale_profile = major_profile if is_major else minor_profile
        mean_scale = np.mean(scale_profile)
        value_scales: list[PitchScaleCorrelationValue] = []

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
            # corr_value is meaningless for negative number, so convert the range to [0,1]
            correlation_value = correlation_value / 2 + 0.5
            value_scales.append(
                {"pitch_scale": (idx, is_major), "corr_val": correlation_value}
            )
        return value_scales

    all_keys_corr_values = get_correlation_values(True) + get_correlation_values(False)
    if need_all:
        return all_keys_corr_values
    else:
        all_keys_corr_values.sort(key=lambda i: i["corr_val"], reverse=True)
        return [all_keys_corr_values[0]]


# determine the key by consider that measure only
# measures_dictionary = return of key_segmentation
# TODO: may have error
def determine_key_solo(
    measures_dictionary: Measure_OffsetChroma_dict,
) -> list[OffsetPitchScaleCorrelationValues]:
    res: list[OffsetPitchScaleCorrelationValues] = []
    for idx, segment in measures_dictionary.items():
        measure_offset = measures_dictionary[idx]["offset"]
        correlation_values: list[PitchScaleCorrelationValue] = find_key(
            segment["chroma"], True
        )
        correlation_values.sort(key=lambda tup: tup[0], reverse=True)
        res.append({"offset": measure_offset, "corr_values": correlation_values})
    return res


# determine the key of the measures in 3 layers
# measures_dictionary = return of key_segmentation
def determine_key_by_adjacent(
    measures_dictionary: Measure_OffsetChroma_dict,
) -> list[OffsetPitchScaleCorrelationValues]:
    queue: list[np.ndarray] = []
    measures_possible_key: dict[int, list[list[PitchScaleCorrelationValue]]] = {}
    two_measures_chroma = np.zeros(12)
    four_measures_chroma = np.zeros(12)

    # identification of keys
    for idx, segment in measures_dictionary.items():
        chroma: np.ndarray = segment["chroma"]
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
    measures_key: list[OffsetPitchScaleCorrelationValues] = []
    for idx, keys_scores in measures_possible_key.items():
        measure_offset = measures_dictionary[idx]["offset"]
        result_dict = {}

        flatten_keys_scores = [item for sublist in keys_scores for item in sublist]
        for key_score in flatten_keys_scores:
            if not key_score["pitch_scale"] in result_dict:
                result_dict[key_score["pitch_scale"]] = 0
            # choose the segment which has the highest corr values
            if result_dict[key_score["pitch_scale"]] < key_score["corr_val"]:
                result_dict[key_score["pitch_scale"]] = key_score["corr_val"]

        measures_key.append(
            {"offset": measure_offset, "corr_values": list(result_dict.items())}
        )
    return measures_key
