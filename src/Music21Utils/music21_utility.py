from music21 import *

# get the name of the pieces of music
def get_music_title(whole_stream):
    return whole_stream.metadata.title


# Load the file in stream
def load_file(path):
    return converter.parse(path)


# TODO: output stream in Music XML format
def export_file(whole_stream, path):
    whole_stream.write("mxl", fp=path)


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

# Other useful:
# print(stream.parts[0].show("text"))
# stream2 = stream.flatten()
# stream.flatten().getElementsByClass(note.Note)
# for thisNote in stream.parts[0].getElementsByClass("Note"):
#     print(thisNote)
# stream.measures(0, 8).show()