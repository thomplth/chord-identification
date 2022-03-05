from bidict import bidict

# chord form dictionary
CHORD_INTERVAL_FORM_BIDICT = bidict({("M3", "m3"): "Major"})
CHORD_INTERVAL_FORM_BIDICT[("m3", "M3")] = "Minor"
CHORD_INTERVAL_FORM_BIDICT[("m3", "m3")] = "Diminished"
CHORD_INTERVAL_FORM_BIDICT[("M3", "m3", "M3")] = "Major seventh"  # can omit
CHORD_INTERVAL_FORM_BIDICT[("m3", "M3", "m3")] = "Minor seventh"
CHORD_INTERVAL_FORM_BIDICT[("M3", "m3", "m3")] = "Dominant seventh"
CHORD_INTERVAL_FORM_BIDICT[("m3", "m3", "m3")] = "Diminished seventh"
CHORD_INTERVAL_FORM_BIDICT[("m3", "m3", "M3")] = "Half-diminished seventh"  # can omit
CHORD_INTERVAL_FORM_BIDICT[("M3", "m3", "A2")] = "German sixth"
CHORD_INTERVAL_FORM_BIDICT[("M3", "M2", "M3")] = "French sixth"
CHORD_INTERVAL_FORM_BIDICT[("M3", "A4")] = "Italian sixth"

# chord form abbr dictionary
CHORD_FORM_ABBR_BIDICT = bidict({"Major": ""})
CHORD_FORM_ABBR_BIDICT["Minor"] = "m"
CHORD_FORM_ABBR_BIDICT["Diminished"] = "dim"
CHORD_FORM_ABBR_BIDICT["Major seventh"] = "maj7"
CHORD_FORM_ABBR_BIDICT["Minor seventh"] = "m7"
CHORD_FORM_ABBR_BIDICT["Dominant seventh"] = "7"
CHORD_FORM_ABBR_BIDICT["Diminished seventh"] = "dim7"
CHORD_FORM_ABBR_BIDICT["Half-diminished seventh"] = "hdim7"
CHORD_FORM_ABBR_BIDICT["Italian sixth"] = "It"
CHORD_FORM_ABBR_BIDICT["German sixth"] = "Ger"
CHORD_FORM_ABBR_BIDICT["French sixth"] = "Fr"

# Key: chord name, value: array of intervals, where the first is the interval between the tonic and the first note,
# and the rest are the interval between the previous and the next note
def put_chord_dict(dictionary: dict, numeral: str, first_interval: str, form: str):
    if form not in CHORD_INTERVAL_FORM_BIDICT.inverse:
        return False
    else:
        dictionary[numeral] = [first_interval] + list(
            (CHORD_INTERVAL_FORM_BIDICT.inverse[form])
        )
        return True


MAJOR_CHORD_DICT = {}
put_chord_dict(MAJOR_CHORD_DICT, "I", "P1", "Major")
# put_chord_dict(MAJOR_CHORD_DICTIONARY, "I7", "P1", "Major seventh")
put_chord_dict(MAJOR_CHORD_DICT, "bII", "m2", "Major")
put_chord_dict(MAJOR_CHORD_DICT, "II", "M2", "Minor")
put_chord_dict(MAJOR_CHORD_DICT, "II7", "M2", "Minor seventh")
put_chord_dict(MAJOR_CHORD_DICT, "III", "M3", "Minor")
# put_chord_dict(MAJOR_CHORD_DICTIONARY, "III7", "M3", "Minor seventh")  # can delete
put_chord_dict(MAJOR_CHORD_DICT, "IV", "P4", "Major")
# put_chord_dict(MAJOR_CHORD_DICTIONARY, "IV7", "P4", "Major seventh")  # can delete
put_chord_dict(MAJOR_CHORD_DICT, "V", "P5", "Major")
put_chord_dict(MAJOR_CHORD_DICT, "V7", "P5", "Dominant seventh")
put_chord_dict(MAJOR_CHORD_DICT, "bVI", "m6", "Major")
put_chord_dict(MAJOR_CHORD_DICT, "GerVI", "m6", "German sixth")
put_chord_dict(MAJOR_CHORD_DICT, "FreVI", "m6", "French sixth")
put_chord_dict(MAJOR_CHORD_DICT, "ItaVI", "m6", "Italian sixth")
put_chord_dict(MAJOR_CHORD_DICT, "VI", "M6", "Minor")
# put_chord_dict(MAJOR_CHORD_DICTIONARY, "VI7", "M6", "Minor seventh")  # can delete
put_chord_dict(MAJOR_CHORD_DICT, "VIIdim", "M7", "Diminished")
# put_chord_dict(
#     MAJOR_CHORD_DICTIONARY, "DimVII5", "M7", "Half-diminished seventh"
# )  # Half-dim 7th, can delete
put_chord_dict(MAJOR_CHORD_DICT, "VIIdim7", "M7", "Diminished seventh")


MINOR_CHORD_DICT = {}
put_chord_dict(MINOR_CHORD_DICT, "I", "P1", "Minor")
MINOR_CHORD_DICT["I+"] = MAJOR_CHORD_DICT["I"]
MINOR_CHORD_DICT["bII"] = MAJOR_CHORD_DICT["bII"]
put_chord_dict(MINOR_CHORD_DICT, "IIdim", "M2", "Diminished")
put_chord_dict(MINOR_CHORD_DICT, "IIdim7", "M2", "Half-diminished seventh")
put_chord_dict(MINOR_CHORD_DICT, "III", "m3", "Major")
put_chord_dict(MINOR_CHORD_DICT, "IV", "P4", "Minor")
MINOR_CHORD_DICT["IV+"] = MAJOR_CHORD_DICT["IV"]
put_chord_dict(MINOR_CHORD_DICT, "V", "P5", "Minor")
MINOR_CHORD_DICT["V+"] = MAJOR_CHORD_DICT["V"]
MINOR_CHORD_DICT["V+7"] = MAJOR_CHORD_DICT["V7"]
MINOR_CHORD_DICT["VI"] = MAJOR_CHORD_DICT["bVI"]
MINOR_CHORD_DICT["GerVI"] = MAJOR_CHORD_DICT["GerVI"]
MINOR_CHORD_DICT["FreVI"] = MAJOR_CHORD_DICT["FreVI"]
MINOR_CHORD_DICT["ItaVI"] = MAJOR_CHORD_DICT["ItaVI"]
put_chord_dict(MINOR_CHORD_DICT, "VII", "m7", "Major")
MINOR_CHORD_DICT["VIIdim"] = MAJOR_CHORD_DICT["VIIdim"]
MINOR_CHORD_DICT["VIIdim7"] = MAJOR_CHORD_DICT["VIIdim7"]

# Dictionary for note to chord
MAJOR_CHORD_FINDER_DICT = {}
for chord, pattern in MAJOR_CHORD_DICT.items():
    chord_pattern = tuple(pattern[1:])
    # print(chord, pattern[0], chord_pattern)
    if chord_pattern in MAJOR_CHORD_FINDER_DICT:
        MAJOR_CHORD_FINDER_DICT[chord_pattern].append(
            {"chord": chord, "tonic_interval": pattern[0]}
        )
    else:
        MAJOR_CHORD_FINDER_DICT[chord_pattern] = [
            {"chord": chord, "tonic_interval": pattern[0]}
        ]
# GerVI and FreVI special cases:
MAJOR_CHORD_FINDER_DICT["P5", "A2"] = [{"chord": "GerVI", "tonic_interval": "m6"}]
MAJOR_CHORD_FINDER_DICT["A4", "M3"] = [{"chord": "FreVI", "tonic_interval": "m6"}]

MINOR_CHORD_FINDER_DICT = {}
for chord, pattern in MINOR_CHORD_DICT.items():
    chord_pattern = tuple(pattern[1:])
    # print(chord, pattern[0], chord_pattern)
    if chord_pattern in MINOR_CHORD_FINDER_DICT:
        MINOR_CHORD_FINDER_DICT[chord_pattern].append(
            {"chord": chord, "tonic_interval": pattern[0]}
        )
    else:
        MINOR_CHORD_FINDER_DICT[chord_pattern] = [
            {"chord": chord, "tonic_interval": pattern[0]}
        ]
# GerVI and FreVI special cases:
MINOR_CHORD_FINDER_DICT["P5", "A2"] = [{"chord": "GerVI", "tonic_interval": "m6"}]
MINOR_CHORD_FINDER_DICT["A4", "M3"] = [{"chord": "FreVI", "tonic_interval": "m6"}]


# chord frequency dictionary
PROBABILITY_DICT = {
    "often": 8.0 / 15,
    "common": 4.0 / 15,
    "seldom": 2.0 / 15,
    "rare": 1.0 / 15,
}
MAJOR_CHORD_FREQUENCY_DICT = {"I": PROBABILITY_DICT["often"]}
MAJOR_CHORD_FREQUENCY_DICT["I7"] = PROBABILITY_DICT["rare"]
MAJOR_CHORD_FREQUENCY_DICT["bII"] = PROBABILITY_DICT["common"]
MAJOR_CHORD_FREQUENCY_DICT["II"] = PROBABILITY_DICT["often"]
MAJOR_CHORD_FREQUENCY_DICT["II7"] = PROBABILITY_DICT["often"]
MAJOR_CHORD_FREQUENCY_DICT["III"] = PROBABILITY_DICT["seldom"]
MAJOR_CHORD_FREQUENCY_DICT["III7"] = PROBABILITY_DICT["rare"]
MAJOR_CHORD_FREQUENCY_DICT["IV"] = PROBABILITY_DICT["often"]
MAJOR_CHORD_FREQUENCY_DICT["IV7"] = PROBABILITY_DICT["seldom"]
MAJOR_CHORD_FREQUENCY_DICT["V"] = PROBABILITY_DICT["often"]
MAJOR_CHORD_FREQUENCY_DICT["V7"] = PROBABILITY_DICT["often"]
MAJOR_CHORD_FREQUENCY_DICT["bVI"] = PROBABILITY_DICT["common"]
MAJOR_CHORD_FREQUENCY_DICT["GerVI"] = PROBABILITY_DICT["common"]
MAJOR_CHORD_FREQUENCY_DICT["FreVI"] = PROBABILITY_DICT["common"]
MAJOR_CHORD_FREQUENCY_DICT["ItaVI"] = PROBABILITY_DICT["common"]
MAJOR_CHORD_FREQUENCY_DICT["VI"] = PROBABILITY_DICT["often"]
MAJOR_CHORD_FREQUENCY_DICT["VI7"] = PROBABILITY_DICT["seldom"]
MAJOR_CHORD_FREQUENCY_DICT["DimVII"] = PROBABILITY_DICT["often"]
MAJOR_CHORD_FREQUENCY_DICT["DimVII5"] = PROBABILITY_DICT["seldom"]
MAJOR_CHORD_FREQUENCY_DICT["DimVII7"] = PROBABILITY_DICT["common"]

MINOR_CHORD_FREQUENCY_DICT = {"I": PROBABILITY_DICT["often"]}
MINOR_CHORD_FREQUENCY_DICT["I+"] = PROBABILITY_DICT["seldom"]
MINOR_CHORD_FREQUENCY_DICT["bII"] = PROBABILITY_DICT["common"]
MINOR_CHORD_FREQUENCY_DICT["IIdim"] = PROBABILITY_DICT["often"]
MINOR_CHORD_FREQUENCY_DICT["IIdim7"] = PROBABILITY_DICT["often"]
MINOR_CHORD_FREQUENCY_DICT["III"] = PROBABILITY_DICT["common"]
MINOR_CHORD_FREQUENCY_DICT["IV"] = PROBABILITY_DICT["often"]
MINOR_CHORD_FREQUENCY_DICT["IV+"] = PROBABILITY_DICT["seldom"]
MINOR_CHORD_FREQUENCY_DICT["V"] = PROBABILITY_DICT["rare"]
MINOR_CHORD_FREQUENCY_DICT["V+"] = PROBABILITY_DICT["often"]
MINOR_CHORD_FREQUENCY_DICT["V+7"] = PROBABILITY_DICT["often"]
MINOR_CHORD_FREQUENCY_DICT["VI"] = PROBABILITY_DICT["common"]
MINOR_CHORD_FREQUENCY_DICT["GerVI"] = PROBABILITY_DICT["common"]
MINOR_CHORD_FREQUENCY_DICT["FreVI"] = PROBABILITY_DICT["common"]
MINOR_CHORD_FREQUENCY_DICT["ItaVI"] = PROBABILITY_DICT["common"]
MINOR_CHORD_FREQUENCY_DICT["VII"] = PROBABILITY_DICT["seldom"]
MINOR_CHORD_FREQUENCY_DICT["DimVII"] = PROBABILITY_DICT["often"]
MINOR_CHORD_FREQUENCY_DICT["DimVII7"] = PROBABILITY_DICT["common"]

partial_record = False
if partial_record:
    major_left = 0.307
    MAJOR_CHORD_FREQUENCY_DICT = {"I": 0.273}
    MAJOR_CHORD_FREQUENCY_DICT["I7"] = PROBABILITY_DICT["rare"] * major_left
    MAJOR_CHORD_FREQUENCY_DICT["bII"] = PROBABILITY_DICT["common"] * major_left
    MAJOR_CHORD_FREQUENCY_DICT["II"] = 0.051
    MAJOR_CHORD_FREQUENCY_DICT["II7"] = PROBABILITY_DICT["often"] * major_left
    MAJOR_CHORD_FREQUENCY_DICT["III"] = PROBABILITY_DICT["seldom"] * major_left
    MAJOR_CHORD_FREQUENCY_DICT["III7"] = PROBABILITY_DICT["rare"] * major_left
    MAJOR_CHORD_FREQUENCY_DICT["IV"] = 0.056
    MAJOR_CHORD_FREQUENCY_DICT["IV7"] = PROBABILITY_DICT["seldom"] * major_left
    MAJOR_CHORD_FREQUENCY_DICT["V"] = 0.096
    MAJOR_CHORD_FREQUENCY_DICT["V7"] = 0.171
    MAJOR_CHORD_FREQUENCY_DICT["bVI"] = PROBABILITY_DICT["common"] * major_left
    MAJOR_CHORD_FREQUENCY_DICT["GerVI"] = PROBABILITY_DICT["common"] * major_left
    MAJOR_CHORD_FREQUENCY_DICT["FreVI"] = PROBABILITY_DICT["common"] * major_left
    MAJOR_CHORD_FREQUENCY_DICT["ItaVI"] = PROBABILITY_DICT["common"] * major_left
    MAJOR_CHORD_FREQUENCY_DICT["VI"] = 0.028
    MAJOR_CHORD_FREQUENCY_DICT["VI7"] = PROBABILITY_DICT["seldom"] * major_left
    MAJOR_CHORD_FREQUENCY_DICT["DimVII"] = 0.018
    MAJOR_CHORD_FREQUENCY_DICT["DimVII5"] = PROBABILITY_DICT["seldom"] * major_left
    MAJOR_CHORD_FREQUENCY_DICT["DimVII7"] = PROBABILITY_DICT["common"] * major_left

    minor_left = 0.368
    MINOR_CHORD_FREQUENCY_DICT = {"I": 0.147}
    MINOR_CHORD_FREQUENCY_DICT["I+"] = 0.142
    MINOR_CHORD_FREQUENCY_DICT["bII"] = PROBABILITY_DICT["common"] * minor_left
    MINOR_CHORD_FREQUENCY_DICT["IIdim"] = PROBABILITY_DICT["often"] * minor_left
    MINOR_CHORD_FREQUENCY_DICT["IIdim7"] = PROBABILITY_DICT["often"] * minor_left
    MINOR_CHORD_FREQUENCY_DICT["III"] = PROBABILITY_DICT["common"] * minor_left
    MINOR_CHORD_FREQUENCY_DICT["IV"] = 0.032
    MINOR_CHORD_FREQUENCY_DICT["IV+"] = 0.023
    MINOR_CHORD_FREQUENCY_DICT["V"] = PROBABILITY_DICT["rare"] * minor_left
    MINOR_CHORD_FREQUENCY_DICT["V+"] = 0.104
    MINOR_CHORD_FREQUENCY_DICT["V+7"] = 0.154
    MINOR_CHORD_FREQUENCY_DICT["VI"] = 0.018
    MINOR_CHORD_FREQUENCY_DICT["GerVI"] = 0.006
    MINOR_CHORD_FREQUENCY_DICT["FreVI"] = PROBABILITY_DICT["common"] * minor_left
    MINOR_CHORD_FREQUENCY_DICT["ItaVI"] = PROBABILITY_DICT["common"] * minor_left
    MINOR_CHORD_FREQUENCY_DICT["VII"] = PROBABILITY_DICT["seldom"] * minor_left
    MINOR_CHORD_FREQUENCY_DICT["DimVII"] = PROBABILITY_DICT["often"] * minor_left
    MINOR_CHORD_FREQUENCY_DICT["DimVII7"] = 0.006