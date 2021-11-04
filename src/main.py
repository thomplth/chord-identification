import time
from Music21Utils.music21_utility import *
from utility import note_input_convertor
from naive_segmentation import *
from note_to_chord import find_chords, print_chords_names


# Time calculation
start_time = time.time()

# TODO: transfer the lyrics from the old file to the new file
# filename = "Nocturne_in_E_Major"
# filename = "Chopin_F._Nocturne_in_E_Major,_Op.26_No.2"
stream = load_file("../Gymnopdie_n1_-_E._Satie.mxl")
# stream = load_file("../Minuet_in_F_C.mxl")
# stream = load_file("../data/" + filename + ".mxl")

chordify_stream = chordify(stream)
time_signature = get_initial_time_signature(chordify_stream)
# print(time_signature.numerator)
key_signature = get_initial_key_signature(chordify_stream)
scale_name = (
    key_signature.tonic.name.lower()
    if key_signature.type == "minor"
    else key_signature.tonic.name.upper()
)
print(scale_name)

segments = segmentation(chordify_stream, time_signature)
combined_segments = merge_segment(segments)
for segment in combined_segments:
    # print(segment[0], [note for note in segment[1]], notes_variation(segment[1]))
    notes = [note_input_convertor(note) for note in segment[1]]
    result = find_chords(notes)
    print(">>>", segment[0])
    print_chords_names(notes, result, scale_name)

# export_file(stream, "../result/Minuet_in_F_C_test")
# export_file(stream, "../result/anonymous_Twinkle_Twinkle_test")
# export_file(chordify_stream, "../result/test2")

# Time calculation
print("--- Used %s seconds ---" % (time.time() - start_time))