import numpy as np
from collections import Counter

# TODO: Key finding algo.
def find_key(measure_chromagram):
    return "C"


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
        if len(queue) > 1:
            key_2_measure = find_key(two_measures_chroma)
            for i in queue[-2:]:
                measures_possible_key[i].append(key_2_measure)
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
