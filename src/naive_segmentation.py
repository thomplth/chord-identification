# from ..ChordNoteTickStart.constant import MAJOR_SEMITONE_CUMULATIVE_PATTERN
from Music21Utils.music21_utility import *
from metric import *
import music21

# TODO: transfer the lyrics from the old file to the new file
# filename = "Nocturne_in_E_Major"
# filename = "Chopin_F._Nocturne_in_E_Major,_Op.26_No.2"
# stream = load_file("../Gymnopdie_n1_-_E._Satie.mxl")
stream = load_file("../Minuet_in_F_C.mxl")
# stream = load_file("../data/" + filename + ".mxl")

chordify_stream = chordify(stream)
measures_len = len(get_measures(chordify_stream))
print(measures_len)
time_signature = get_initial_time_signature(chordify_stream)
print(time_signature.numerator)


for element in chordify_stream.recurse().getElementsByClass("Measure"):
    element.show("text")
    chords = element.recurse().getElementsByClass("Chord")
    if len(chords) > 0:
        # notes[0].addLyric(str("x"))
        for chord in chords:
            mark = int(chord.offset) - chord.offset % time_signature.numerator == 0
            # mark = mark and int(note.offset) % time_signature.numerator
            if mark:
                chord.addLyric(str("x"))

    print("----")

# export_file(stream, "../result/Minuet_in_F_C_test")
# export_file(stream, "../result/anonymous_Twinkle_Twinkle_test")

export_file(chordify_stream, "../result/test2")
