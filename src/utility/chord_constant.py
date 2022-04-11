from bidict import bidict

# chord form dictionary
CHORD_INTERVAL_FORM_BIDICT = bidict({("M3", "m3"): "Major"})
CHORD_INTERVAL_FORM_BIDICT[("m3", "M3")] = "Minor"
CHORD_INTERVAL_FORM_BIDICT[("m3", "m3")] = "Diminished"
CHORD_INTERVAL_FORM_BIDICT[("M3", "M3")] = "Augmented"
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
CHORD_FORM_ABBR_BIDICT["Augmented"] = "aug"
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
put_chord_dict(MAJOR_CHORD_DICT, "Iaug", "P1", "Augmented")
put_chord_dict(MAJOR_CHORD_DICT, "bII", "m2", "Major")
put_chord_dict(MAJOR_CHORD_DICT, "II", "M2", "Minor")
put_chord_dict(MAJOR_CHORD_DICT, "II7", "M2", "Minor seventh")
put_chord_dict(MAJOR_CHORD_DICT, "#IIdim7", "A2", "Diminished seventh")
put_chord_dict(MAJOR_CHORD_DICT, "III", "M3", "Minor")
put_chord_dict(MAJOR_CHORD_DICT, "IV", "P4", "Major")
put_chord_dict(MAJOR_CHORD_DICT, "IVaug", "P4", "Augmented")
put_chord_dict(MAJOR_CHORD_DICT, "#IVdim", "A4", "Diminished")
put_chord_dict(MAJOR_CHORD_DICT, "V", "P5", "Major")
put_chord_dict(MAJOR_CHORD_DICT, "V7", "P5", "Dominant seventh")
put_chord_dict(MAJOR_CHORD_DICT, "Vaug", "P5", "Augmented")
put_chord_dict(MAJOR_CHORD_DICT, "bVI", "m6", "Major")
put_chord_dict(MAJOR_CHORD_DICT, "VI", "M6", "Minor")
put_chord_dict(MAJOR_CHORD_DICT, "GerVI", "m6", "German sixth")
put_chord_dict(MAJOR_CHORD_DICT, "FreVI", "m6", "French sixth")
put_chord_dict(MAJOR_CHORD_DICT, "ItaVI", "m6", "Italian sixth")
put_chord_dict(MAJOR_CHORD_DICT, "VIIdim", "M7", "Diminished")
put_chord_dict(MAJOR_CHORD_DICT, "VIIdim7", "M7", "Diminished seventh")
put_chord_dict(
    MAJOR_CHORD_DICT, "VIIhdim7", "M7", "Half-diminished seventh"
)  # Half-dim 7th


MINOR_CHORD_DICT = {}
put_chord_dict(MINOR_CHORD_DICT, "I", "P1", "Minor")
MINOR_CHORD_DICT["I+"] = MAJOR_CHORD_DICT["I"]
MINOR_CHORD_DICT["bII"] = MAJOR_CHORD_DICT["bII"]
put_chord_dict(MINOR_CHORD_DICT, "IIdim", "M2", "Diminished")
put_chord_dict(MINOR_CHORD_DICT, "IIhdim7", "M2", "Half-diminished seventh")
MINOR_CHORD_DICT["#IIdim7"] = MAJOR_CHORD_DICT["#IIdim7"]
put_chord_dict(MINOR_CHORD_DICT, "III", "m3", "Major")
put_chord_dict(MINOR_CHORD_DICT, "IV", "P4", "Minor")
MINOR_CHORD_DICT["IV+"] = MAJOR_CHORD_DICT["IV"]
MINOR_CHORD_DICT["#IVdim"] = MAJOR_CHORD_DICT["#IVdim"]
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
MINOR_CHORD_DICT["VIIhdim7"] = MAJOR_CHORD_DICT["VIIhdim7"]

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
MAJOR_CHORD_FREQUENCY_DICT = {"I": 0.287110789}
MAJOR_CHORD_FREQUENCY_DICT["Iaug"] = 0.002111996
MAJOR_CHORD_FREQUENCY_DICT["bII"] = 0.003620565
MAJOR_CHORD_FREQUENCY_DICT["II"] = 0.058532464
MAJOR_CHORD_FREQUENCY_DICT["II7"] = 0.008749698
MAJOR_CHORD_FREQUENCY_DICT["#IIdim7"] = 0.000844798
MAJOR_CHORD_FREQUENCY_DICT["III"] = 0.006335988
MAJOR_CHORD_FREQUENCY_DICT["IV"] = 0.068006276
MAJOR_CHORD_FREQUENCY_DICT["IVaug"] = 0.00066377
MAJOR_CHORD_FREQUENCY_DICT["#IVdim"] = 0.00066377
MAJOR_CHORD_FREQUENCY_DICT["V"] = 0.18277818
MAJOR_CHORD_FREQUENCY_DICT["V7"] = 0.291877866
MAJOR_CHORD_FREQUENCY_DICT["Vaug"] = 0.001568911
MAJOR_CHORD_FREQUENCY_DICT["bVI"] = 0.001146512
MAJOR_CHORD_FREQUENCY_DICT["VI"] = 0.035059136
MAJOR_CHORD_FREQUENCY_DICT["GerVI"] = 0.003318851
MAJOR_CHORD_FREQUENCY_DICT["FreVI"] = 0.000301714
MAJOR_CHORD_FREQUENCY_DICT["ItaVI"] = 0.001629254
MAJOR_CHORD_FREQUENCY_DICT["VIIdim"] = 0.029507603
MAJOR_CHORD_FREQUENCY_DICT["VIIdim7"] = 0.012068549
MAJOR_CHORD_FREQUENCY_DICT["VIIhdim7"] = 0.004103307

MINOR_CHORD_FREQUENCY_DICT = {"I": 0.182064849}
MINOR_CHORD_FREQUENCY_DICT["I+"] = 0.154524488
MINOR_CHORD_FREQUENCY_DICT["bII"] = 0.008411342
MINOR_CHORD_FREQUENCY_DICT["IIdim"] = 0.009632343
MINOR_CHORD_FREQUENCY_DICT["IIdim7"] = 0.007461674
MINOR_CHORD_FREQUENCY_DICT["#IIdim7"] = 0.000271334
MINOR_CHORD_FREQUENCY_DICT["III"] = 0.008818342
MINOR_CHORD_FREQUENCY_DICT["IV"] = 0.041514042
MINOR_CHORD_FREQUENCY_DICT["IV+"] = 0.034459368
MINOR_CHORD_FREQUENCY_DICT["#IVdim"] = 0.000135667
MINOR_CHORD_FREQUENCY_DICT["V"] = 0.006919007
MINOR_CHORD_FREQUENCY_DICT["V+"] = 0.188034188
MINOR_CHORD_FREQUENCY_DICT["V+7"] = 0.242300909
MINOR_CHORD_FREQUENCY_DICT["VI"] = 0.026455026
MINOR_CHORD_FREQUENCY_DICT["GerVI"] = 0.007868675
MINOR_CHORD_FREQUENCY_DICT["FreVI"] = 0.001085334
MINOR_CHORD_FREQUENCY_DICT["ItaVI"] = 0.002849003
MINOR_CHORD_FREQUENCY_DICT["VII"] = 0.003120336
MINOR_CHORD_FREQUENCY_DICT["VIIdim"] = 0.021842355
MINOR_CHORD_FREQUENCY_DICT["VIIdim7"] = 0.051553385
MINOR_CHORD_FREQUENCY_DICT["VIIhdim7"] = 0.000678334
