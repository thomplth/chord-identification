import numpy as np

MAJOR_SEMITONE_CUMULATIVE_PATTERN = [0, 2, 4, 5, 7, 9, 11]

# Key: note name, value: distance (number of semitone) between C in ascending order
HEPTATONIC_DICTIONARY = {"C": MAJOR_SEMITONE_CUMULATIVE_PATTERN[0]}
HEPTATONIC_DICTIONARY["D"] = MAJOR_SEMITONE_CUMULATIVE_PATTERN[1]
HEPTATONIC_DICTIONARY["E"] = MAJOR_SEMITONE_CUMULATIVE_PATTERN[2]
HEPTATONIC_DICTIONARY["F"] = MAJOR_SEMITONE_CUMULATIVE_PATTERN[3]
HEPTATONIC_DICTIONARY["G"] = MAJOR_SEMITONE_CUMULATIVE_PATTERN[4]
HEPTATONIC_DICTIONARY["A"] = MAJOR_SEMITONE_CUMULATIVE_PATTERN[5]
HEPTATONIC_DICTIONARY["B"] = MAJOR_SEMITONE_CUMULATIVE_PATTERN[6]

MAJOR_SEMITONE_PATTERN = [2, 2, 1, 2, 2, 2]
MINOR_SEMITONE_PATTERN = [2, 1, 2, 2, 1, 2]  # only natural minor is listed

# Dictionary to convert semitone to interval
SEMITONE_TO_INTERVAL_DICTIONARY = {0: ["P1", "d2", "A7"]}
SEMITONE_TO_INTERVAL_DICTIONARY[1] = ["m2", "A1"]
SEMITONE_TO_INTERVAL_DICTIONARY[2] = ["M2", "d3"]
SEMITONE_TO_INTERVAL_DICTIONARY[3] = ["m3", "A2"]
SEMITONE_TO_INTERVAL_DICTIONARY[4] = ["M3", "d4"]
SEMITONE_TO_INTERVAL_DICTIONARY[5] = ["P4", "A3"]
SEMITONE_TO_INTERVAL_DICTIONARY[6] = ["d5", "A4"]
SEMITONE_TO_INTERVAL_DICTIONARY[7] = ["P5", "d6"]
SEMITONE_TO_INTERVAL_DICTIONARY[8] = ["m6", "A5"]
SEMITONE_TO_INTERVAL_DICTIONARY[9] = ["M6", "d7"]
SEMITONE_TO_INTERVAL_DICTIONARY[10] = ["m7", "A6"]
SEMITONE_TO_INTERVAL_DICTIONARY[11] = ["M7", "d8"]

INTERVAL_TO_SEMITONE_DICTIONARY = {}
for semitone, intervals in SEMITONE_TO_INTERVAL_DICTIONARY.items():
    for interval in intervals:
        INTERVAL_TO_SEMITONE_DICTIONARY[interval] = semitone

# Key: chord name, value: array of intervals, where the first is the interval between the tonic and the first note,
# and the rest are the interval between the previous and the next note
MAJOR_CHORD_DICTIONARY = {"I": ["P1", "M3", "m3"]}
# MAJOR_CHORD_DICTIONARY["I7"] = ["P1", "M3", "m3", "M3"]  # can delete
MAJOR_CHORD_DICTIONARY["bII"] = ["m2", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["II"] = ["M2", "m3", "M3"]
MAJOR_CHORD_DICTIONARY["II7"] = ["M2", "m3", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["III"] = ["M3", "m3", "M3"]
# MAJOR_CHORD_DICTIONARY["iii7"] = ["M3", "m3", "M3", "m3"]  # can delete
MAJOR_CHORD_DICTIONARY["IV"] = ["P4", "M3", "m3"]
# MAJOR_CHORD_DICTIONARY["IV7"] = ["P4", "M3", "m3", "M3"]  # can delete
MAJOR_CHORD_DICTIONARY["V"] = ["P5", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["V7"] = ["P5", "M3", "m3", "m3"]
MAJOR_CHORD_DICTIONARY["bVI"] = ["m6", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["GerVI"] = ["m6", "M3", "m3", "A2"]
MAJOR_CHORD_DICTIONARY["FreVI"] = ["m6", "M3", "M2", "M3"]
MAJOR_CHORD_DICTIONARY["ItaVI"] = ["m6", "M3", "A4"]
MAJOR_CHORD_DICTIONARY["VI"] = ["M6", "m3", "M3"]
# MAJOR_CHORD_DICTIONARY["VI7"] = ["M6", "m3", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["DimVII"] = ["M7", "m3", "m3"]
# MAJOR_CHORD_DICTIONARY["DimVII5"] = ["M7", "m3", "m3", "M3"]  # Half-dim 7th
MAJOR_CHORD_DICTIONARY["DimVII7"] = ["M7", "m3", "m3", "m3"]  # Dim 7th

MINOR_CHORD_DICTIONARY = {"I": ["P1", "m3", "M3"]}
MINOR_CHORD_DICTIONARY["I+"] = MAJOR_CHORD_DICTIONARY["I"]
MINOR_CHORD_DICTIONARY["bII"] = MAJOR_CHORD_DICTIONARY["bII"]
MINOR_CHORD_DICTIONARY["IIdim"] = ["M2", "m3", "m3"]
MINOR_CHORD_DICTIONARY["IIdim7"] = ["M2", "m3", "m3", "M3"]  # Half-dim 7th
MINOR_CHORD_DICTIONARY["III"] = ["m3", "M3", "m3"]
MINOR_CHORD_DICTIONARY["IV"] = ["P4", "m3", "M3"]
MINOR_CHORD_DICTIONARY["IV+"] = MAJOR_CHORD_DICTIONARY["IV"]
MINOR_CHORD_DICTIONARY["V"] = ["P5", "m3", "M3"]
MINOR_CHORD_DICTIONARY["V+"] = MAJOR_CHORD_DICTIONARY["V"]
MINOR_CHORD_DICTIONARY["V+7"] = MAJOR_CHORD_DICTIONARY["V7"]
MINOR_CHORD_DICTIONARY["VI"] = MAJOR_CHORD_DICTIONARY["bVI"]
MINOR_CHORD_DICTIONARY["GerVI"] = MAJOR_CHORD_DICTIONARY["GerVI"]
MINOR_CHORD_DICTIONARY["FreVI"] = MAJOR_CHORD_DICTIONARY["FreVI"]
MINOR_CHORD_DICTIONARY["ItaVI"] = MAJOR_CHORD_DICTIONARY["ItaVI"]
MINOR_CHORD_DICTIONARY["VII"] = ["m7", "M3", "m3"]
MINOR_CHORD_DICTIONARY["DimVII"] = MAJOR_CHORD_DICTIONARY["DimVII"]
MINOR_CHORD_DICTIONARY["DimVII7"] = MAJOR_CHORD_DICTIONARY["DimVII7"]

# Dictionary for note to chord
MAJOR_CHORD_FINDER_DICTIONARY = {}
for chord, pattern in MAJOR_CHORD_DICTIONARY.items():
    chord_pattern = tuple(pattern[1:])
    # print(chord, pattern[0], chord_pattern)
    if chord_pattern in MAJOR_CHORD_FINDER_DICTIONARY:
        MAJOR_CHORD_FINDER_DICTIONARY[chord_pattern].append(
            {"chord": chord, "tonic_interval": pattern[0]}
        )
    else:
        MAJOR_CHORD_FINDER_DICTIONARY[chord_pattern] = [
            {"chord": chord, "tonic_interval": pattern[0]}
        ]
# GerVI and FreVI special cases:
MAJOR_CHORD_FINDER_DICTIONARY["P5", "A2"] = [{"chord": "GerVI", "tonic_interval": "m6"}]
MAJOR_CHORD_FINDER_DICTIONARY["A4", "M3"] = [{"chord": "FreVI", "tonic_interval": "m6"}]

MINOR_CHORD_FINDER_DICTIONARY = {}
for chord, pattern in MINOR_CHORD_DICTIONARY.items():
    chord_pattern = tuple(pattern[1:])
    # print(chord, pattern[0], chord_pattern)
    if chord_pattern in MINOR_CHORD_FINDER_DICTIONARY:
        MINOR_CHORD_FINDER_DICTIONARY[chord_pattern].append(
            {"chord": chord, "tonic_interval": pattern[0]}
        )
    else:
        MINOR_CHORD_FINDER_DICTIONARY[chord_pattern] = [
            {"chord": chord, "tonic_interval": pattern[0]}
        ]
# GerVI and FreVI special cases:
MINOR_CHORD_FINDER_DICTIONARY["P5", "A2"] = [{"chord": "GerVI", "tonic_interval": "m6"}]
MINOR_CHORD_FINDER_DICTIONARY["A4", "M3"] = [{"chord": "FreVI", "tonic_interval": "m6"}]

# chord frequency dictionary
PROBABILITY_DICTIONARY = {
    "often": 8.0 / 15,
    "common": 4.0 / 15,
    "seldom": 2.0 / 15,
    "rare": 1.0 / 15,
}
MAJOR_CHORD_FREQUENCY_DICTIONARY = {"I": PROBABILITY_DICTIONARY["often"]}
MAJOR_CHORD_FREQUENCY_DICTIONARY["I7"] = PROBABILITY_DICTIONARY["rare"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["bII"] = PROBABILITY_DICTIONARY["common"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["II"] = PROBABILITY_DICTIONARY["often"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["II7"] = PROBABILITY_DICTIONARY["often"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["III"] = PROBABILITY_DICTIONARY["seldom"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["III7"] = PROBABILITY_DICTIONARY["rare"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["IV"] = PROBABILITY_DICTIONARY["often"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["IV7"] = PROBABILITY_DICTIONARY["seldom"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["V"] = PROBABILITY_DICTIONARY["often"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["V7"] = PROBABILITY_DICTIONARY["often"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["bVI"] = PROBABILITY_DICTIONARY["common"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["GerVI"] = PROBABILITY_DICTIONARY["common"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["FreVI"] = PROBABILITY_DICTIONARY["common"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["ItaVI"] = PROBABILITY_DICTIONARY["common"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["VI"] = PROBABILITY_DICTIONARY["often"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["VI7"] = PROBABILITY_DICTIONARY["seldom"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["DimVII"] = PROBABILITY_DICTIONARY["often"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["DimVII5"] = PROBABILITY_DICTIONARY["seldom"]
MAJOR_CHORD_FREQUENCY_DICTIONARY["DimVII7"] = PROBABILITY_DICTIONARY["common"]

MINOR_CHORD_FREQUENCY_DICTIONARY = {"I": PROBABILITY_DICTIONARY["often"]}
MINOR_CHORD_FREQUENCY_DICTIONARY["I+"] = PROBABILITY_DICTIONARY["seldom"]
MINOR_CHORD_FREQUENCY_DICTIONARY["bII"] = PROBABILITY_DICTIONARY["common"]
MINOR_CHORD_FREQUENCY_DICTIONARY["IIdim"] = PROBABILITY_DICTIONARY["often"]
MINOR_CHORD_FREQUENCY_DICTIONARY["IIdim7"] = PROBABILITY_DICTIONARY["often"]
MINOR_CHORD_FREQUENCY_DICTIONARY["III"] = PROBABILITY_DICTIONARY["common"]
MINOR_CHORD_FREQUENCY_DICTIONARY["IV"] = PROBABILITY_DICTIONARY["often"]
MINOR_CHORD_FREQUENCY_DICTIONARY["IV+"] = PROBABILITY_DICTIONARY["seldom"]
MINOR_CHORD_FREQUENCY_DICTIONARY["V"] = PROBABILITY_DICTIONARY["rare"]
MINOR_CHORD_FREQUENCY_DICTIONARY["V+"] = PROBABILITY_DICTIONARY["often"]
MINOR_CHORD_FREQUENCY_DICTIONARY["V+7"] = PROBABILITY_DICTIONARY["often"]
MINOR_CHORD_FREQUENCY_DICTIONARY["VI"] = PROBABILITY_DICTIONARY["common"]
MINOR_CHORD_FREQUENCY_DICTIONARY["GerVI"] = PROBABILITY_DICTIONARY["common"]
MINOR_CHORD_FREQUENCY_DICTIONARY["FreVI"] = PROBABILITY_DICTIONARY["common"]
MINOR_CHORD_FREQUENCY_DICTIONARY["ItaVI"] = PROBABILITY_DICTIONARY["common"]
MINOR_CHORD_FREQUENCY_DICTIONARY["VII"] = PROBABILITY_DICTIONARY["seldom"]
MINOR_CHORD_FREQUENCY_DICTIONARY["DimVII"] = PROBABILITY_DICTIONARY["often"]
MINOR_CHORD_FREQUENCY_DICTIONARY["DimVII7"] = PROBABILITY_DICTIONARY["common"]

partial_record = True
if partial_record:
    major_left = 0.307
    MAJOR_CHORD_FREQUENCY_DICTIONARY = {"I": 0.273}
    MAJOR_CHORD_FREQUENCY_DICTIONARY["I7"] = PROBABILITY_DICTIONARY["rare"] * major_left
    MAJOR_CHORD_FREQUENCY_DICTIONARY["bII"] = (
        PROBABILITY_DICTIONARY["common"] * major_left
    )
    MAJOR_CHORD_FREQUENCY_DICTIONARY["II"] = 0.051
    MAJOR_CHORD_FREQUENCY_DICTIONARY["II7"] = (
        PROBABILITY_DICTIONARY["often"] * major_left
    )
    MAJOR_CHORD_FREQUENCY_DICTIONARY["III"] = (
        PROBABILITY_DICTIONARY["seldom"] * major_left
    )
    MAJOR_CHORD_FREQUENCY_DICTIONARY["III7"] = (
        PROBABILITY_DICTIONARY["rare"] * major_left
    )
    MAJOR_CHORD_FREQUENCY_DICTIONARY["IV"] = 0.056
    MAJOR_CHORD_FREQUENCY_DICTIONARY["IV7"] = (
        PROBABILITY_DICTIONARY["seldom"] * major_left
    )
    MAJOR_CHORD_FREQUENCY_DICTIONARY["V"] = 0.096
    MAJOR_CHORD_FREQUENCY_DICTIONARY["V7"] = 0.171
    MAJOR_CHORD_FREQUENCY_DICTIONARY["bVI"] = (
        PROBABILITY_DICTIONARY["common"] * major_left
    )
    MAJOR_CHORD_FREQUENCY_DICTIONARY["GerVI"] = (
        PROBABILITY_DICTIONARY["common"] * major_left
    )
    MAJOR_CHORD_FREQUENCY_DICTIONARY["FreVI"] = (
        PROBABILITY_DICTIONARY["common"] * major_left
    )
    MAJOR_CHORD_FREQUENCY_DICTIONARY["ItaVI"] = (
        PROBABILITY_DICTIONARY["common"] * major_left
    )
    MAJOR_CHORD_FREQUENCY_DICTIONARY["VI"] = 0.028
    MAJOR_CHORD_FREQUENCY_DICTIONARY["VI7"] = (
        PROBABILITY_DICTIONARY["seldom"] * major_left
    )
    MAJOR_CHORD_FREQUENCY_DICTIONARY["DimVII"] = 0.018
    MAJOR_CHORD_FREQUENCY_DICTIONARY["DimVII5"] = (
        PROBABILITY_DICTIONARY["seldom"] * major_left
    )
    MAJOR_CHORD_FREQUENCY_DICTIONARY["DimVII7"] = (
        PROBABILITY_DICTIONARY["common"] * major_left
    )

    minor_left = 0.368
    MINOR_CHORD_FREQUENCY_DICTIONARY = {"I": 0.147}
    MINOR_CHORD_FREQUENCY_DICTIONARY["I+"] = 0.142
    MINOR_CHORD_FREQUENCY_DICTIONARY["bII"] = (
        PROBABILITY_DICTIONARY["common"] * minor_left
    )
    MINOR_CHORD_FREQUENCY_DICTIONARY["IIdim"] = (
        PROBABILITY_DICTIONARY["often"] * minor_left
    )
    MINOR_CHORD_FREQUENCY_DICTIONARY["IIdim7"] = (
        PROBABILITY_DICTIONARY["often"] * minor_left
    )
    MINOR_CHORD_FREQUENCY_DICTIONARY["III"] = (
        PROBABILITY_DICTIONARY["common"] * minor_left
    )
    MINOR_CHORD_FREQUENCY_DICTIONARY["IV"] = 0.032
    MINOR_CHORD_FREQUENCY_DICTIONARY["IV+"] = 0.023
    MINOR_CHORD_FREQUENCY_DICTIONARY["V"] = PROBABILITY_DICTIONARY["rare"] * minor_left
    MINOR_CHORD_FREQUENCY_DICTIONARY["V+"] = 0.104
    MINOR_CHORD_FREQUENCY_DICTIONARY["V+7"] = 0.154
    MINOR_CHORD_FREQUENCY_DICTIONARY["VI"] = 0.018
    MINOR_CHORD_FREQUENCY_DICTIONARY["GerVI"] = 0.006
    MINOR_CHORD_FREQUENCY_DICTIONARY["FreVI"] = (
        PROBABILITY_DICTIONARY["common"] * minor_left
    )
    MINOR_CHORD_FREQUENCY_DICTIONARY["ItaVI"] = (
        PROBABILITY_DICTIONARY["common"] * minor_left
    )
    MINOR_CHORD_FREQUENCY_DICTIONARY["VII"] = (
        PROBABILITY_DICTIONARY["seldom"] * minor_left
    )
    MINOR_CHORD_FREQUENCY_DICTIONARY["DimVII"] = (
        PROBABILITY_DICTIONARY["often"] * minor_left
    )
    MINOR_CHORD_FREQUENCY_DICTIONARY["DimVII7"] = 0.006

# the threshold that determine if a segment can be given a chord label
NOTES_VARIATION_THRESHOLD = 3
NOTES_FREQUENCY_THRESHOLD = 0.2

# Key profile dictionary
KEY_PROFILE_DICTIONARY = {}
KEY_PROFILE_DICTIONARY["Krumhansl-Kessler"] = (
    np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]),
    np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]),
)
KEY_PROFILE_DICTIONARY["Temperley"] = (
    np.array([5.0, 2.0, 3.5, 2.0, 4.5, 4.0, 2.0, 4.5, 2.0, 3.5, 1.5, 4.0]),
    np.array([5.0, 2.0, 3.5, 4.5, 2.0, 4.0, 2.0, 4.5, 3.5, 2.0, 1.5, 4.0]),
)
KEY_PROFILE_DICTIONARY["Steedman"] = (
    np.array([1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0]),
    np.array([1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.5, 0.5]),
)
KEY_PROFILE_DICTIONARY["Aarden-Essen"] = (
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
