

def cSeg_accuracy_hard(piece, prediction):
    target = piece.get_cSeg_target()
    aligned = 0
    segments = min(len(prediction), len(target))
    for i in range(segments):
        if prediction[i] == target[i][1]:
            aligned += 1

def cSeg_accuracy(piece, prediction):
    pass

def kSeg_accuracy(piece, prediction):
    pass


if __name__ == '__main__':
    pass
    # print(chord_segmentation_accuracy())

"""
>>> music21.music21.converter.subConverters.ConverterMusicXML
def parseFile(self, fp: Union[str, pathlib.Path], number=None):
    # Open from a file path; check to see if there is a pickled
    # version available and up to date; if so, open that, otherwise
    # open source.
    
    # return fp to load, if pickle needs to be written, fp pickle
    # this should be able to work on a .mxl file, as all we are doing
    # here is seeing which is more recent
    from music21 import converter
    from music21.musicxml import xmlToM21

    c = xmlToM21.MusicXMLImporter()

    # here, we can see if this is a mxl or similar archive
    arch = converter.ArchiveManager(fp)
    if arch.isArchive():
        archData = arch.getData()
        c.xmlText = archData
        c.parseXMLText()
    else:  # its a file path or a raw musicxml string
        c.readFile(fp)

    # movement titles can be stored in more than one place in musicxml
    # manually insert file name as a movementName title if no titles are defined
    if c.stream.metadata.movementName is None:
        junk, fn = os.path.split(fp)
        c.stream.metadata.movementName = fn  # this should become a Path
    self.stream = c.stream
    
<<<<<<< HEAD
'''
=======
"""
>>>>>>> fc634d2767129441883fea4e33534c24dc5fca46
