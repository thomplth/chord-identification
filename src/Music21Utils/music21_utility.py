from music21 import *
import time

# get the name of the pieces of music
def get_music_title(whole_stream):
    return whole_stream.metadata.title


# Load the file in stream
def load_file(path):
    return converter.parse(path)


# TODO: output stream in Music XML format
def export_file(whole_stream, path):
    whole_stream.write("musicxml", fp=path)


# reduce multiple parts to one part
def chordify(whole_stream):
    return whole_stream.chordify()
    # TODO: make the notes closer using closedPosition()


# get the measures (in list) in the stream
def get_measures(chordified_stream):
    measures = [
        measure for measure in chordified_stream.recurse().getElementsByClass("Measure")
    ]
    # print(measures)
    return measures


# get the key signature at the beginning
def get_initial_key_signature(chordified_stream):
    keys = [
        key.asKey()
        for key in chordified_stream.recurse().getElementsByClass(key.KeySignature)
    ]
    # print(keys)
    return keys[0]


# get the key signature at the beginning
def get_initial_time_signature(chordified_stream):
    times = [
        time
        for time in chordified_stream.recurse().getElementsByClass(meter.TimeSignature)
    ]
    # print(times)
    return times[0]


def analyze_key(stream):
    key = stream.analyze("key")
    return key
    # OR: return a tuple (Tonic, major/minor)
    # return (key.tonic, key.mode)


start_time = time.time()

# TODO: transfer the lyrics from the old file to the new file
filename = "Nocturne_in_E_Major"
# filename = "Chopin_F._Nocturne_in_E_Major,_Op.26_No.2"
# filename = "Brahms_J._Waltz_in_A-Flat_Major,_Op.35_No.15"
s1 = load_file("../../data/" + filename + ".mxl")
chordify_s1 = chordify(s1)

print(get_initial_key_signature(chordify_s1))

measures = get_measures(chordify_s1)
# for measure in measures[:4]:
#     for element in measure.recurse():
#         print(element)
#     print("--break--")

# print(s1.parts[0].lyrics())
# print(s2.parts[0].lyrics())
# print(get_key_signature(s1.parts[0]))
# print(get_key_signature(s2.parts[0]))
# print(get_key_signature(chordify(s1)))
# key = analyze_key(s1)

# Time calculation
print("--- Used %s seconds ---" % (time.time() - start_time))

# Other useful:
# print(stream.parts[0].show("text"))
# stream2 = stream.flatten()
# stream.flatten().getElementsByClass(note.Note)
# for thisNote in stream.parts[0].getElementsByClass("Note"):
#     print(thisNote)
# stream.measures(0, 8).show()