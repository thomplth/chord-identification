from utility.m21_utility import *

# This file is just for retrieved the data for corrupted mxl files
# which does nothing on the chord identification system

filename = "Nocturne_in_E_Major"
old_stream = load_file("../data/" + filename + ".mxl")
# filename = "Chopin_F._Nocturne_in_E_Major,_Op.26_No.2"
# new_stream = load_file("../data/" + filename + ".mxl")
# print(len(get_measures(chordify(old_stream))))

target = old_stream.recurse().measures(70, 82)
target.show()
# for measure in target.recurse().getElementsByClass("Measure"):
#     print(measure)
#     chords = measure.recurse().getElementsByClass("Chord")
#     if len(chords) > 0:
#         for c in chords:
#             if len(c.lyrics) > 0:
#                 print(c.lyrics, c.offset)
#     notes = measure.recurse().getElementsByClass("Note")
#     if len(notes) > 0:
#         for c in notes:
#             if len(c.lyrics) > 0:
#                 print(c.lyrics, c.offset)
#     print("---")
