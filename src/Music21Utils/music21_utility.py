from music21 import *
import time

# get the name of the pieces of music
def get_music_title(whole_stream):
    return whole_stream.metadata.title


# get the number of measures in the stream
def get_measure_num(part):
    return len(part.getElementsByClass("Measure"))


# TODO: get the key signature at the beginning
def get_key_signature(part):
    print(part)
    print(part.flat)
    return part.flat.getElementsByClass("KeySignature")


# Load the file in stream
def load_file(path):
    return converter.parse(path)


# reduce multiple parts to one part
def chordify(whole_stream):
    return whole_stream.chordify()
    # TODO: make the notes closer using closedPosition()


# TODO: output stream in Music XML format
def export_file(whole_stream, path):
    whole_stream.write("musicxml", fp=path)


def analyze_key(stream):
    key = stream.analyze("key")
    return key
    # OR: return a tuple (Tonic, major/minor)
    # return (key.tonic, key.mode)


start_time = time.time()
# TODO: transfer the lyrics from the old file to the new file
s1 = load_file("../../data/Nocturne_in_E_Major.mxl")
# s2 = load_file("../../data/Chopin_F._Nocturne_in_E_Major,_Op.26_No.2.mxl")
s1 = load_file("../../data/Brahms_J._Waltz_in_A-Flat_Major,_Op.35_No.15.mxl")
# print(s1.parts[0].lyrics())
# print(s2.parts[0].lyrics())
print(get_key_signature(s1.parts[0]))
# print(get_key_signature(s2.parts[0]))
# print(get_key_signature(chordify(s2)))
key = analyze_key(s1)

# Time calculation
print("--- Used %s seconds ---" % (time.time() - start_time))

# Other useful:
# print(stream.parts[0].show("text"))
# stream2 = stream.flatten()
# stream.flatten().getElementsByClass(note.Note)
# for thisNote in stream.parts[0].getElementsByClass("Note"):
#     print(thisNote)
# stream.measures(0, 8).show()