from music21 import *

s = converter.parse("Nocturne_in_Eb_Major.mxl")
# s.show()
s = s.transpose("M3")
s.show()
# key = s.getScale("major")
# print(key)