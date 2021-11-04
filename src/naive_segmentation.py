# from ..ChordNoteTickStart.constant import MAJOR_SEMITONE_CUMULATIVE_PATTERN
from Music21Utils.music21_utility import *
from utility import note_input_convertor, note_object_simplifier
from metric import *
import music21
import time


def segmentation(chordify_stream):
    segments = []
    print("------")
    for measure in chordify_stream.recurse().getElementsByClass("Measure"):
        measure_offset = measure.offset
        chords = measure.recurse().getElementsByClass("Chord")
        if len(chords) > 0:
            # notes[0].addLyric(str("x"))
            for chord in chords:
                # uniform segmentation
                mark = int(chord.offset) - chord.offset % time_signature.numerator == 0
                chord_offset = measure_offset + int(chord.offset)

                notes = list(chord.notes)
                if not mark:
                    same_segment = segments.pop()
                    notes = same_segment[1] + notes

                segments.append((chord_offset, notes))

    return [(segment[0], note_object_simplifier(segment[1])) for segment in segments]


if __name__ == "__main__":
    # Time calculation
    start_time = time.time()

    # TODO: transfer the lyrics from the old file to the new file
    # filename = "Nocturne_in_E_Major"
    # filename = "Chopin_F._Nocturne_in_E_Major,_Op.26_No.2"
    # stream = load_file("../Gymnopdie_n1_-_E._Satie.mxl")
    stream = load_file("../Minuet_in_F_C.mxl")
    # stream = load_file("../data/" + filename + ".mxl")

    chordify_stream = chordify(stream)
    measures_len = len(get_measures(chordify_stream))
    # print(measures_len)
    time_signature = get_initial_time_signature(chordify_stream)
    # print(time_signature.numerator)

    segments = segmentation(chordify_stream)
    for ele in segments:
        print(ele[0], [note.note_str() for note in ele[1]])

    # export_file(stream, "../result/Minuet_in_F_C_test")
    # export_file(stream, "../result/anonymous_Twinkle_Twinkle_test")

    # export_file(chordify_stream, "../result/test2")

    # Time calculation
    print("--- Used %s seconds ---" % (time.time() - start_time))