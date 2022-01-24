from music21 import converter, stream, harmony
import configparser
import os

CONFIG = configparser.ConfigParser()
configpath = os.path.dirname(os.path.dirname(__file__))
CONFIG.read(os.path.join(configpath, "config.ini"))

try:
    DATA_PATH = CONFIG["locations"]["data_path"]
    RESULT_PATH = CONFIG["locations"]["result_path"]
except KeyError:
    print(f"failed to read config.ini (or wrong key specified)")
    raise SystemExit


class Piece:
    """Container of a music21.stream object with custom data extration methods and enhanced abstraction.
    """

    def __init__(self, filename):
        """
        :param filename: filename of the music piece
        :type filename: str
        """
        self.name = os.path.basename(filename)
        self.score = converter.parse(os.path.join(DATA_PATH, self.name+'.mxl'))
        self.length = self.score.duration.quarterLength

        self.chordified = self.score.chordify()
        self.flattened = self.score.flatten()

    def __iter__(self):
        """
        :return: Iterator of current stream object
        :rtype: StreamIterator
        """
        return stream.iterator.StreamIterator(self.score)

    def __get_elements_in_measures(self, measures, type):
        res = []
        for measure in measures:
            for el in measure.getElementsByClass(type):
                res.append(el)
        return res

    def get_key_signatures(self, custom_stream=None):
        """Search key signatures for all parts of the score.

        :rtype: list of keySignature objects
        """
        target_stream = self.score if not custom_stream else custom_stream
        return list(target_stream.recurse().getElementsByClass("KeySignature"))

    def get_elements_by_offset(self, filter=None):
        """Obtain all/specified elements in flatterned stream, ordered by offset

        :param filter: filter type based on m21 classes, defaults to None
        :type filter: str/m21 class, optional
        :return: dictionary of offsets and lists of m21 objects in {<offset>: [<element>]}
        :rtype: dict
        """
        o_iter = stream.iterator.OffsetIterator(self.flattened)
        if filter:
            o_iter = o_iter.getElementsByClass(filter)
        return {x[0].offset: x for x in o_iter}

    def get_measures(self, custom_stream=None):
        """Obtain all measures of the score. Default to origin stream.

        :param custom_stream: specify stream (compactible with chordified stream), defaults to None
        :type custom_stream: music21.stream.Score, optional
        :return: (default) list of lists of measures
                 (custom) list of measures
        :rtype: list
        """
        if not custom_stream:
            parts_iter = self.score.getElementsByClass("PartStaff")
            return [list(part.getElementsByClass('Measure')) for part in parts_iter]
        else:
            return list(custom_stream.recurse().getElementsByClass('Measure'))

    def get_notes(self, custom_stream=None):
        """Obtain all notes of the score.

        :param custom_stream: specify stream, defaults to None
        :type custom_stream: music21.stream.Score, optional
        :return: (default) list of lists of notes
                 (custom) list of notes
        :rtype: list
        """
        if not custom_stream:
            parts = self.get_measures()
            return [self.__get_elements_in_measures(measures, 'Note') for measures in parts]
        else:
            return list(custom_stream.recurse().getElementsByClass('Note'))

    def get_ground_truth(self, type='chord'):
        """Traverse labelled music stream to generates ground truth data for evaluation.

        :param type: 'chord' or 'key' segments, defaults to 'chord'
        :type type: str, optional
        :return: list of tuples of float, string in (<offset>, <key or chord symbol>)
        :rtype: list
        """
        res = []
        if type == 'chord':
            chord_symbols = self.get_elements_by_offset(filter="ChordSymbol")
            for offset, el in chord_symbols.items():
                chord = el[0]
                cs = f'{chord.figure}({chord.chordKindStr})'
                res.append((offset, cs))
        elif type == 'key':
            notes = self.get_elements_by_offset(filter="Note")
            for offset, el in notes.items():
                note = el[0]
                if note.lyric:
                    res.append((note.offset, note.lyric))
                    
        return res

        # input_path = "../data_KY2001/data_answer" + "/" + self.name + ".pydata"
        # with open(input_path, "rb") as f:
        #     return pickle.load(f)

    def export(self, path=RESULT_PATH, filename=None, type='mxl'):
        """Output music stream as file.

        :param path: path to write on, defaults to OUTPUT_PATH
        :type path: str, optional
        :param type: output format, defaults to 'mxl'
        :type type: str, optional
        """
        name = self.filename if not filename else filename
        filepath = os.path.join(path, name)
        self.score.write(type, fp=filepath)

    def show(self):
        self.score.show()


if __name__ == "__main__":
    # p = Piece("anonymous_Twinkle_Twinkle")
    p = Piece("Mozart_W.A._Minuet_in_F_major,_K.2")
    # print(p.get_measures())
    # print(p.get_notes())
    # print(p.get_key_signatures())
    # print(p.get_elements_by_offset())
    print(p.get_ground_truth())
    print(p.get_ground_truth(type='key'))
