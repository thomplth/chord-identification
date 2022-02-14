import numpy as np

MAJOR_SEMITONE_CUMULATIVE_PATTERN: list[int] = [0, 2, 4, 5, 7, 9, 11]

# Key: note name, value: distance (number of semitone) between C in ascending order
HEPTATONIC_DICT: dict[str, int] = {"C": MAJOR_SEMITONE_CUMULATIVE_PATTERN[0]}
HEPTATONIC_DICT["D"] = MAJOR_SEMITONE_CUMULATIVE_PATTERN[1]
HEPTATONIC_DICT["E"] = MAJOR_SEMITONE_CUMULATIVE_PATTERN[2]
HEPTATONIC_DICT["F"] = MAJOR_SEMITONE_CUMULATIVE_PATTERN[3]
HEPTATONIC_DICT["G"] = MAJOR_SEMITONE_CUMULATIVE_PATTERN[4]
HEPTATONIC_DICT["A"] = MAJOR_SEMITONE_CUMULATIVE_PATTERN[5]
HEPTATONIC_DICT["B"] = MAJOR_SEMITONE_CUMULATIVE_PATTERN[6]

MAJOR_SEMITONE_PATTERN: list[int] = [2, 2, 1, 2, 2, 2]
MINOR_SEMITONE_PATTERN: list[int] = [2, 1, 2, 2, 1, 2]  # only natural minor is listed

# Dictionary to convert semitone to interval
SEMITONE_INTERVAL_DICT: dict[int, list[str]] = {0: ["P1", "d2", "A7"]}
SEMITONE_INTERVAL_DICT[1] = ["m2", "A1"]
SEMITONE_INTERVAL_DICT[2] = ["M2", "d3"]
SEMITONE_INTERVAL_DICT[3] = ["m3", "A2"]
SEMITONE_INTERVAL_DICT[4] = ["M3", "d4"]
SEMITONE_INTERVAL_DICT[5] = ["P4", "A3"]
SEMITONE_INTERVAL_DICT[6] = ["d5", "A4"]
SEMITONE_INTERVAL_DICT[7] = ["P5", "d6"]
SEMITONE_INTERVAL_DICT[8] = ["m6", "A5"]
SEMITONE_INTERVAL_DICT[9] = ["M6", "d7"]
SEMITONE_INTERVAL_DICT[10] = ["m7", "A6"]
SEMITONE_INTERVAL_DICT[11] = ["M7", "d8"]

INTERVAL_SEMITONE_DICT: dict[str, int] = {}
for semitone, intervals in SEMITONE_INTERVAL_DICT.items():
    for interval in intervals:
        INTERVAL_SEMITONE_DICT[interval] = semitone


# the threshold that determine if a segment can be given a chord label
NOTES_VARIATION_THRESHOLD = 4
NOTES_FREQUENCY_THRESHOLD = 0.2

# Key profile dictionary
KEY_PROFILE_DICT = {}
KEY_PROFILE_DICT["Krumhansl-Kessler"] = (
    np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]),
    np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]),
)
KEY_PROFILE_DICT["Temperley"] = (
    np.array([5.0, 2.0, 3.5, 2.0, 4.5, 4.0, 2.0, 4.5, 2.0, 3.5, 1.5, 4.0]),
    np.array([5.0, 2.0, 3.5, 4.5, 2.0, 4.0, 2.0, 4.5, 3.5, 2.0, 1.5, 4.0]),
)
KEY_PROFILE_DICT["Steedman"] = (
    np.array([1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0]),
    np.array([1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.5, 0.5]),
)
KEY_PROFILE_DICT["Aarden-Essen"] = (
    np.array(
        [
            17.7661,
            0.145624,
            14.9265,
            0.160186,
            19.8049,
            11.3587,
            0.291248,
            22.062,
            0.145624,
            8.15494,
            0.232998,
            4.95122,
        ]
    ),
    np.array(
        [
            18.2648,
            0.737619,
            14.0499,
            16.8599,
            0.702494,
            14.4362,
            0.702494,
            18.6161,
            4.56621,
            1.93186,
            7.37619,
            1.75623,
        ]
    ),
)
