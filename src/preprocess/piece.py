from logging import exception
from music21 import converter, stream
import csv
import configparser
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))


CONFIG = configparser.ConfigParser()
configpath = os.path.dirname(os.path.dirname(__file__))
CONFIG.read(os.path.join(configpath, "config.ini"))

try:
    DATA_PATH = CONFIG["locations"]["data_path"]
    DATASET_PATH = DATA_PATH + CONFIG["locations"]["dataset_path"]
    GT_PATH = CONFIG["locations"]["gt_path"]
    RESULT_PATH = CONFIG["locations"]["result_path"]
except KeyError:
    print("failed to read config.ini, or invalid index specified")
    raise SystemExit


class Piece:
    """Container of a music21.stream object with custom data extration methods and enhanced abstraction."""

    def __init__(self, filename):
        """
        :param filename: filename of the music piece (with or without extension)
        :type filename: str
        """
        self.name = (
            filename[:-4]
            if filename.endswith(".mxl") or filename.endswith(".xml")
            else filename
        )
        self.score = converter.parse(os.path.join(DATASET_PATH, filename))
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
            return [list(part.getElementsByClass("Measure")) for part in parts_iter]
        else:
            return list(custom_stream.recurse().getElementsByClass("Measure"))

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
            return [
                self.__get_elements_in_measures(measures, "Note") for measures in parts
            ]
        else:
            return list(custom_stream.recurse().getElementsByClass("Note"))

    def get_ground_truth(self, type="chord"):
        """Traverse labelled music stream to generates text-based ground truth data for evaluation.

        :param type: 'chord' or 'key' segments, defaults to 'chord'
        :type type: str, optional
        :return: list of tuples of float, string, char, string in (<offset>, <tonic>, <key>, <chord>);
                 or list of tuples of float, string, char in (<offset>, <tonic>, <key>)
        :rtype: list
        """
        res = []
        notes = self.get_elements_by_offset(filter=["Note", "Chord"])

        # Archived code for chordsymbol-lookup
        # if type == 'chord':
        # chord_symbols = self.get_elements_by_offset(filter="ChordSymbol")
        # for offset, el in chord_symbols.items():
        #     chord = el[0]
        #     cs = f'{chord.figure}({chord.chordKindStr})'
        #     res.append((offset, cs))

        chord, tonic, key = "", "", ""
        if type == "chord":
            for offset, el in notes.items():
                for note in el:
                    if note.lyric:
                        try:
                            lyric = note.lyric.replace("♭", "b")

                            if "(" in note.lyric:
                                tonic = lyric.split("(")[0][:-1]
                                key = lyric.split("(")[0][-1]
                                chord = lyric.split("(")[1][:-1]

                                res.append((note.offset, tonic, key, chord))
                            else:
                                chord = lyric
                                res.append((note.offset, tonic, key, chord))

                        except Exception as e:
                            print(
                                f"\033[93m[{e}] for chord {note.lyric} at {note.offset} of {self.name}\033[0m"
                            )
        elif type == "key":
            for offset, el in notes.items():
                for note in el:
                    if note.lyric and "(" in note.lyric:
                        tonic = note.lyric.split("(")[0][:-1]
                        tonic = tonic[:-1] + "b" if tonic.endswith("♭") else tonic
                        key = note.lyric.split("(")[0][-1]
                        res.append((note.offset, tonic, key))
        else:
            raise ValueError("Type must be either chord or key")

        return res

    def export(self, path=RESULT_PATH, filename=None, type="mxl"):
        """Output music stream as mxl file (by default).

        :param path: path to write on, defaults to OUTPUT_PATH
        :type path: str, optional
        :param type: output format, defaults to 'mxl'
        :type type: str, optional
        """
        name = self.filename if not filename else filename
        filepath = os.path.join(path, name)
        self.score.write(type, fp=filepath)

    def _export_ground_truth(self):
        """Single use function for generating ground truth csv files"""
        try:
            gt = self.get_ground_truth()

            path = os.path.join(GT_PATH, self.name + ".csv")
            file = open(path, "w", newline="")
            writer = csv.writer(file)
            writer.writerow(("offset", "tonic", "key", "numeral"))
            for segment in gt:
                writer.writerow(segment)
            file.close()

            gt = self.get_ground_truth(type="key")

            path = os.path.join(GT_PATH + "_key", self.name + ".csv")
            file = open(path, "w", newline="")
            writer = csv.writer(file)
            writer.writerow(("offset", "tonic", "key"))
            for segment in gt:
                writer.writerow(segment)
            file.close()
        except Exception:
            print(self.name)
            print(gt)

    def show(self):
        self.score.show()


if __name__ == "__main__":
    # p = Piece("Chopin_F._Waltz_in_A_Minor,_Op.34_No.2")
    # p.flattened.show()

    # for tup in p.get_ground_truth():
    #     print(tup)
    # print()
    # for tup in p.get_ground_truth(type='key'):
    #     print(tup)
    # raise SystemExit

    scores = [f for f in os.listdir(DATASET_PATH) if f.endswith(".mxl")]
    chord_dict = {}

    for score in scores:
        p = Piece(score)
        print(score, "processing...")
        p._export_ground_truth()

        # res, tmpdict = p.get_ground_truth()
        # print(tmpdict)

        # path = os.path.join(DATA_PATH, 'counter', p.name + '.csv')
        # with open(path, 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(('chord', 'occurance'))
        #     for k, v in tmpdict.items():
        #         writer.writerow((k, v))

    #     for k, v in tmpdict.items():
    #         if k not in chord_dict:
    #             chord_dict[k] = v
    #         else:
    #             chord_dict[k] += v

    # path = os.path.join(DATA_PATH, 'chords_count.csv')
    # with open(path, 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(('chord', 'occurance'))
    #     for k, v in chord_dict.items():
    #         writer.writerow((k, v))