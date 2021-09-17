# Key: note name, value: distance (number of semitone) between C in ascending order
HEPTATONIC_DICTIONARY = {"C": 0}
HEPTATONIC_DICTIONARY["D"] = 2
HEPTATONIC_DICTIONARY["E"] = 4
HEPTATONIC_DICTIONARY["F"] = 5
HEPTATONIC_DICTIONARY["G"] = 7
HEPTATONIC_DICTIONARY["A"] = 9
HEPTATONIC_DICTIONARY["B"] = 11

MAJOR_SEMITONE_PATTERN = [2, 2, 1, 2, 2, 2]
MAJOR_SEMITONE_CUMULATIVE_PATTERN = [0, 2, 4, 5, 7, 9, 11]
# only natural minor is listed
MINOR_SEMITONE_PATTERN = [2, 1, 2, 2, 1, 2]

# Key: chord name, value: array of intervals, where the first is the interval between the tonic and the first note,
# and the rest are the interval between the previous and the next note
MAJOR_CHORD_DICTIONARY = {"I": ["P1", "M3", "m3"]}
MAJOR_CHORD_DICTIONARY["I7"] = ["P1", "M3", "m3", "M3"]
MAJOR_CHORD_DICTIONARY["bII"] = ["m2", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["ii"] = ["M2", "m3", "M3"]
MAJOR_CHORD_DICTIONARY["ii7"] = ["M2", "m3", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["iii"] = ["M3", "m3", "M3"]
MAJOR_CHORD_DICTIONARY["iii7"] = ["M3", "m3", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["IV"] = ["P4", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["IV7"] = ["P4", "M3", "m3", "M3"]
MAJOR_CHORD_DICTIONARY["V"] = ["P5", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["V7"] = ["P5", "M3", "m3", "m3"]
MAJOR_CHORD_DICTIONARY["bVI"] = ["m6", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["GerVI"] = ["m6", "M3", "m3", "A2"]
MAJOR_CHORD_DICTIONARY["FrVI"] = ["m6", "M3", "M2", "M3"]
MAJOR_CHORD_DICTIONARY["ItVI"] = ["m6", "M3", "A4"]
MAJOR_CHORD_DICTIONARY["vi"] = ["M6", "m3", "M3"]
MAJOR_CHORD_DICTIONARY["vi7"] = ["M6", "m3", "M3", "m3"]
MAJOR_CHORD_DICTIONARY["viidim"] = ["M7", "m3", "m3"]
MAJOR_CHORD_DICTIONARY["viidim5"] = ["M7", "m3", "m3", "M3"]  # Half-dim 7th
MAJOR_CHORD_DICTIONARY["viidim7"] = ["M7", "m3", "m3", "m3"]  # Dim 7th

MINOR_CHORD_DICTIONARY = {"i": ["P1", "m3", "M3"]}
MINOR_CHORD_DICTIONARY["I+"] = MAJOR_CHORD_DICTIONARY["I"]  # from I to I+
MINOR_CHORD_DICTIONARY["bII"] = MAJOR_CHORD_DICTIONARY["bII"]
MINOR_CHORD_DICTIONARY["iidim"] = ["M2", "m3", "m3"]
MINOR_CHORD_DICTIONARY["iidim5"] = ["M2", "m3", "m3", "M3"]  # Half-dim 7th
MINOR_CHORD_DICTIONARY["III"] = ["m3", "M3", "m3"]
MINOR_CHORD_DICTIONARY["iv"] = ["P4", "m3", "M3"]
MINOR_CHORD_DICTIONARY["IV"] = MAJOR_CHORD_DICTIONARY["IV"]
MINOR_CHORD_DICTIONARY["v"] = ["P5", "m3", "M3"]
MINOR_CHORD_DICTIONARY["V"] = MAJOR_CHORD_DICTIONARY["V"]
MINOR_CHORD_DICTIONARY["V7"] = MAJOR_CHORD_DICTIONARY["V7"]
MINOR_CHORD_DICTIONARY["VI"] = MAJOR_CHORD_DICTIONARY["bVI"]
MINOR_CHORD_DICTIONARY["GerVI"] = MAJOR_CHORD_DICTIONARY["GerVI"]
MINOR_CHORD_DICTIONARY["FrVI"] = MAJOR_CHORD_DICTIONARY["FrVI"]
MINOR_CHORD_DICTIONARY["ItVI"] = MAJOR_CHORD_DICTIONARY["ItVI"]
MINOR_CHORD_DICTIONARY["VII"] = ["m7", "M3", "m3"]
MINOR_CHORD_DICTIONARY["viidim"] = MAJOR_CHORD_DICTIONARY["viidim"]
MINOR_CHORD_DICTIONARY["viidim7"] = MAJOR_CHORD_DICTIONARY["viidim7"]

# General one
CHORD_DICTIONARY = MAJOR_CHORD_DICTIONARY.copy()
for chord, pattern in MINOR_CHORD_DICTIONARY.items():
    if chord not in CHORD_DICTIONARY:
        CHORD_DICTIONARY[chord] = pattern

# Dictionary for note to chord
CHORD_FINDER_DICTIONARY = {}
for chord, pattern in CHORD_DICTIONARY.items():
    chord_pattern = tuple(pattern[1:])
    # print(chord, pattern[0], chord_pattern)
    if chord_pattern in CHORD_FINDER_DICTIONARY:
        CHORD_FINDER_DICTIONARY[chord_pattern].append(
            {"chord": chord, "tonic_interval": pattern[0]}
        )
    else:
        CHORD_FINDER_DICTIONARY[chord_pattern] = [
            {"chord": chord, "tonic_interval": pattern[0]}
        ]