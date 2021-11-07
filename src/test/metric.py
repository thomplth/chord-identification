from preprocess.piece import Piece


def chord_seg_accuracy_hard(piece, prediction):
    """
    Naive scoring method for chord segmentation.
    Only checks portion of correct slicing.

    :rtype: score in 0-1 range
    """

    target = piece.get_chord_seg_target()
    aligned = 0
    segments = min(len(prediction), len(target))
    for i in range(segments):
        if prediction[i] == target[i][1]:
            aligned += 1

    return round(aligned / len(target), 4)


def chord_seg_accuracy(piece, prediction):
    pass


def key_seg_accuracy(piece, prediction):
    pass


if __name__ == "__main__":
    p = Piece('Twinkle-Twinkle')
    print(chord_seg_accuracy_hard(p, [0.0, 4.0, 6.0, 8.0, 10.0, 11.0]))

""" reference for
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
    
"""
