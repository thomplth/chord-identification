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
# only natural minor is listed
MINOR_SEMITONE_PATTERN = [2, 1, 2, 2, 1, 2]

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
MAJOR_CHORD_DICTIONARY["FrVI"] = ["m6", "M3", "M2", "M3"]
MAJOR_CHORD_DICTIONARY["ItVI"] = ["m6", "M3", "A4"]
MAJOR_CHORD_DICTIONARY["VI"] = ["M6", "m3", "M3"]
# MAJOR_CHORD_DICTIONARY["VI7"] = ["M6", "m3", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["VIIdim"] = ["M7", "m3", "m3"]
# MAJOR_CHORD_DICTIONARY["VIIdim5"] = ["M7", "m3", "m3", "M3"]  # Half-dim 7th
MAJOR_CHORD_DICTIONARY["VIIdim7"] = ["M7", "m3", "m3", "m3"]  # Dim 7th

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
MINOR_CHORD_DICTIONARY["FrVI"] = MAJOR_CHORD_DICTIONARY["FrVI"]
MINOR_CHORD_DICTIONARY["ItVI"] = MAJOR_CHORD_DICTIONARY["ItVI"]
MINOR_CHORD_DICTIONARY["VII"] = ["m7", "M3", "m3"]
MINOR_CHORD_DICTIONARY["VIIdim"] = MAJOR_CHORD_DICTIONARY["VIIdim"]
MINOR_CHORD_DICTIONARY["VIIdim7"] = MAJOR_CHORD_DICTIONARY["VIIdim7"]

# General one
# CHORD_DICTIONARY = MAJOR_CHORD_DICTIONARY.copy()
# for chord, pattern in MINOR_CHORD_DICTIONARY.items():
#     if chord not in CHORD_DICTIONARY:
#         CHORD_DICTIONARY[chord] = pattern

# Dictionary for note to chord
# CHORD_FINDER_DICTIONARY = {}
# for chord, pattern in CHORD_DICTIONARY.items():
#     chord_pattern = tuple(pattern[1:])
#     # print(chord, pattern[0], chord_pattern)
#     if chord_pattern in CHORD_FINDER_DICTIONARY:
#         CHORD_FINDER_DICTIONARY[chord_pattern].append(
#             {"chord": chord, "tonic_interval": pattern[0]}
#         )
#     else:
#         CHORD_FINDER_DICTIONARY[chord_pattern] = [
#             {"chord": chord, "tonic_interval": pattern[0]}
#         ]

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
# GerVI and FrVI special cases:
MAJOR_CHORD_FINDER_DICTIONARY["P5", "A2"] = [{"chord": "GerVI", "tonic_interval": "m6"}]
MAJOR_CHORD_FINDER_DICTIONARY["A4", "M3"] = [{"chord": "FrVI", "tonic_interval": "m6"}]

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
# GerVI and FrVI special cases:
MINOR_CHORD_FINDER_DICTIONARY["P5", "A2"] = [{"chord": "GerVI", "tonic_interval": "m6"}]
MINOR_CHORD_FINDER_DICTIONARY["A4", "M3"] = [{"chord": "FrVI", "tonic_interval": "m6"}]

# the threshold that determine if a segment can be given a chord label
NOTES_VARIATION_THRESHOLD = 4