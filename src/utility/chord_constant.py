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
CHORD_FORM_ABBR_BIDICT["Diminished seventh"] = "o7"
CHORD_FORM_ABBR_BIDICT["Half-diminished seventh"] = "%7"
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


MAJOR_CHORD_DICTIONARY = {}
put_chord_dict(MAJOR_CHORD_DICTIONARY, "I", "P1", "Major")
# put_chord_dict(MAJOR_CHORD_DICTIONARY, "I7", "P1", "Major seventh")
put_chord_dict(MAJOR_CHORD_DICTIONARY, "bII", "m2", "Major")
put_chord_dict(MAJOR_CHORD_DICTIONARY, "II", "M2", "Minor")
put_chord_dict(MAJOR_CHORD_DICTIONARY, "II7", "M2", "Minor seventh")
put_chord_dict(MAJOR_CHORD_DICTIONARY, "III", "M3", "Minor")
# put_chord_dict(MAJOR_CHORD_DICTIONARY, "III7", "M3", "Minor seventh")  # can delete
put_chord_dict(MAJOR_CHORD_DICTIONARY, "IV", "P4", "Major")
# put_chord_dict(MAJOR_CHORD_DICTIONARY, "IV7", "P4", "Major seventh")  # can delete
put_chord_dict(MAJOR_CHORD_DICTIONARY, "V", "P5", "Major")
put_chord_dict(MAJOR_CHORD_DICTIONARY, "V7", "P5", "Dominant seventh")
put_chord_dict(MAJOR_CHORD_DICTIONARY, "bVI", "m6", "Major")
put_chord_dict(MAJOR_CHORD_DICTIONARY, "GerVI", "m6", "German sixth")
put_chord_dict(MAJOR_CHORD_DICTIONARY, "FreVI", "m6", "French sixth")
put_chord_dict(MAJOR_CHORD_DICTIONARY, "ItaVI", "m6", "Italian sixth")
put_chord_dict(MAJOR_CHORD_DICTIONARY, "VI", "M6", "Minor")
# put_chord_dict(MAJOR_CHORD_DICTIONARY, "VI7", "M6", "Minor seventh")  # can delete
put_chord_dict(MAJOR_CHORD_DICTIONARY, "VIIdim", "M7", "Diminished")
# put_chord_dict(
#     MAJOR_CHORD_DICTIONARY, "DimVII5", "M7", "Half-diminished seventh"
# )  # Half-dim 7th, can delete
put_chord_dict(MAJOR_CHORD_DICTIONARY, "VIIdim7", "M7", "Diminished seventh")


MINOR_CHORD_DICTIONARY = {}
put_chord_dict(MINOR_CHORD_DICTIONARY, "I", "P1", "Minor")
MINOR_CHORD_DICTIONARY["I+"] = MAJOR_CHORD_DICTIONARY["I"]
MINOR_CHORD_DICTIONARY["bII"] = MAJOR_CHORD_DICTIONARY["bII"]
put_chord_dict(MINOR_CHORD_DICTIONARY, "IIdim", "M2", "Diminished")
put_chord_dict(MINOR_CHORD_DICTIONARY, "IIdim7", "M2", "Half-diminished seventh")
put_chord_dict(MINOR_CHORD_DICTIONARY, "III", "m3", "Major")
put_chord_dict(MINOR_CHORD_DICTIONARY, "IV", "P4", "Minor")
MINOR_CHORD_DICTIONARY["IV+"] = MAJOR_CHORD_DICTIONARY["IV"]
put_chord_dict(MINOR_CHORD_DICTIONARY, "V", "P5", "Minor")
MINOR_CHORD_DICTIONARY["V+"] = MAJOR_CHORD_DICTIONARY["V"]
MINOR_CHORD_DICTIONARY["V+7"] = MAJOR_CHORD_DICTIONARY["V7"]
MINOR_CHORD_DICTIONARY["VI"] = MAJOR_CHORD_DICTIONARY["bVI"]
MINOR_CHORD_DICTIONARY["GerVI"] = MAJOR_CHORD_DICTIONARY["GerVI"]
MINOR_CHORD_DICTIONARY["FreVI"] = MAJOR_CHORD_DICTIONARY["FreVI"]
MINOR_CHORD_DICTIONARY["ItaVI"] = MAJOR_CHORD_DICTIONARY["ItaVI"]
put_chord_dict(MINOR_CHORD_DICTIONARY, "VII", "m7", "Major")
MINOR_CHORD_DICTIONARY["VIIdim"] = MAJOR_CHORD_DICTIONARY["VIIdim"]
MINOR_CHORD_DICTIONARY["VIIdim7"] = MAJOR_CHORD_DICTIONARY["VIIdim7"]

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

partial_record = False
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