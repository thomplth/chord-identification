import time
from Music21Utils.music21_utility import *
from utility import note_input_convertor
from segmentation import *
from key_identification import determine_key
from note_to_chord import find_chords, print_chords_names


# Time calculation
start_time = time.time()

# stream = load_file("../Gymnopdie_n1_-_E._Satie.mxl")
# stream = load_file("../Minuet_in_F_C.mxl")
filename = "anonymous_Twinkle_Twinkle"
filename = "Chopin_F._Nocturne_in_E_Minor,_Op.72_No.1"
stream = load_file("../data/" + filename + ".mxl")

chordify_stream = chordify(stream)

time_signature = get_initial_time_signature(chordify_stream)
key_signature = get_initial_key_signature(chordify_stream)
scale_name = (
    key_signature.tonic.name.lower()
    if key_signature.type == "minor"
    else key_signature.tonic.name.upper()
)
print("Assume all measures are in ", scale_name)
measures_key = determine_key(key_segmentation(stream))
for k, v in measures_key.items():
    print(k, v)


if False:
    segments = uniform_segmentation(chordify_stream, time_signature)
    combined_segments = merge_chord_segment(segments)
    # print(combined_segments)
    for segment in combined_segments[:2]:
        notes = [note_input_convertor(note) for note in segment[1]]
        result = find_chords(notes)
        print(">>>", segment[0], segment[1], notes_variation(segment[1]))
        print_chords_names(notes, result, "")


# export_file(stream, "../result/Minuet_in_F_C_test")
# export_file(stream, "../result/anonymous_Twinkle_Twinkle_test")
# export_file(chordify_stream, "../result/test2")

# Time calculation
print("--- Used %s seconds ---" % (time.time() - start_time))