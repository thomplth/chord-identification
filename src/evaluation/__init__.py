# if __name__ == "__main__":
#     import os, sys
#     sys.path.insert(1, os.path.join(sys.path[0], '..'))

# from preprocess.piece import Piece

import csv
import pickle
from music21 import converter, stream

# from utility.constant import (
#     HEPTATONIC_DICTIONARY,
#     SEMITONE_TO_INTERVAL_DICTIONARY,
#     INTERVAL_TO_SEMITONE_DICTIONARY,
# )


"""Naming convention for the result file
result_KTC_NoCommon_4_.1
KTC = Key then Chord, KAC = Key and Chord (refer to report for details)
No Common = No Commonity of Chord, Simple Common = x/15 distribution one, ComplexCommon = Hybrid distribution
3rd number is note variation theshold
4th number: note duration theshold
"""

SCORE_PATH = "../data"
GT_PATH = "../data/ground_truth"
RESULT_PATH = "../csv"


class Metric:
    def __init__(self, name20, name21):
        self.ground_truth = self._parse_ground_truth(name20)
        # self.result = self._parse_result(name21)
        self.length = self._get_length(name21)

    def _get_length(self, filename):
        score = converter.parse(SCORE_PATH + filename + ".mxl")
        return score.duration.quarterLength

    def _parse_result(self, filename, seventh=True):
        res = []
        with open(RESULT_PATH + filename + ".csv", newline="") as f:
            reader = csv.reader(f)
            data = [tuple(row) for row in reader]

        for row in data:
            try:
                if seventh:
                    numeral = row[1]
                else:
                    numeral = row[1].split("7")[0]
                offset = float(row[0])
            except ValueError:
                x, y = map(int, row[0].split("/"))  # int or float? int now
                offset = x / y
            res.append((numeral, row[2], offset))

        return res

    def _parse_ground_truth(self, filename):
        res = []
        with open(GT_PATH + filename + ".pydata", "rb") as f:
            data = pickle.load(f)

        for chord, offset in data:
            numeral, scale = self.convert_chord_name(chord)
            res.append((numeral, scale, offset))

        return res

    def convert_chord_name(self, chord):
        a, b = chord.split("(")
        scale = a[:-1]
        numeral = b[:-1]
        if len(scale) > 1:
            if scale[1] == "b":
                scale = scale[0] + "-"
            elif scale[1] == "#":
                scale = scale[0] + "#"
            else:
                print(scale)

        if a[-1] == "M":
            scale = scale + " Major"
        else:
            scale = scale.lower() + " Minor"
        return numeral, scale

    def chord_perfect_match(piece, prediction):
        """Perfect Matches
        Hard evaluation method for chord segmentation.
        Only checks the number of correct slicings.

        :rtype: float score in 0-1 range
        """

        target = piece.get_chord_seg_target()
        aligned = 0
        segments = min(len(prediction), len(target))
        for i in range(segments):
            if prediction[i] == target[i][1]:
                aligned += 1

        return aligned / len(target)

    def chord_symbol_recall(self):
        """Chord Symbol Recall (chord_symbol_recall)
        Also called Average Overlap Score or Relative Correct Overlap.
        MIREX has used an approximate chord_symbol_recall calculated by sampling both the ground-truth and the automatic annotations every 10 ms and dividing the number of correctly annotated samples by the total number of samples. Following Christopher Harte (2010, §8.1.2)

        :rtype: float score in 0-1 range
        """
        if not self.ground_truth or not self.result:
            return False

        match_duration = 0.0
        res_idx = 0

        # Calculate relative correct overlap with ground truth data as basis
        for gt_idx, segment in enumerate(self.ground_truth):
            gt_start = segment[2]
            if gt_idx + 1 < len(self.ground_truth):
                gt_end = self.ground_truth[gt_idx + 1][2]
            else:
                gt_end = self.length

            # Increment matching duration if result chord matches with GT
            # End if result segment time exceed GT
            while True:
                res_start = max(self.result[res_idx][2], gt_start)
                if res_idx + 1 < len(self.result):
                    res_end = self.result[res_idx + 1][2]
                else:
                    res_end = self.length

                if (
                    self.result[res_idx][0] == segment[0]
                    and self.result[res_idx][1] == segment[1]
                ):
                    match_duration += min(res_end - res_start, gt_end - res_start)
                    # print(f'Matched at {gt_start} for {res_start} - {res_end}')
                else:
                    if self.result[res_idx][1] == segment[1]:
                        print(
                            f"Unmatched result at {res_start}: <{self.result[res_idx][0]}-{segment[0]}>"
                        )
                    elif self.result[res_idx][0] == segment[0]:
                        print(
                            f"Unmatched result at {res_start}: <{self.result[res_idx][1]}-{segment[1]}>"
                        )
                    else:
                        print(
                            f"Unmatched result at {res_start}: <{self.result[res_idx][0]}-{segment[0]}>, <{self.result[res_idx][1]}-{segment[1]}>"
                        )

                if gt_end == res_end:
                    res_idx += 1
                    break
                elif gt_end < res_end:
                    break
                else:
                    res_idx += 1

        return match_duration / self.length


if __name__ == "__main__":
    name20 = "Étude_in_C_Minor"
    name21 = "Chopin_F._Etude_in_C_Minor,_Op.25_No.12_(Ocean)"

    res = []
    for i in [3, 4]:
        for j in [1, 2]:
            m = Metric(name20, name21)
            m.parse_ground_truth("data/ground_truth/" + name20)
            m.parse_result(f"result/csv/result_KTC_NoCommon_{i}_.{j}/" + name21)
            a = m.chord_symbol_recall()

            m2 = Metric()
            m2.get_length("data/" + name21)
            m2.parse_ground_truth("data/ground_truth/" + name20)
            m2.parse_result(
                f"result/csv/result_KTC_NoCommon_{i}_.{j}/" + name21, seventh=False
            )
            b = m2.chord_symbol_recall()
            res.append((f"KTC_NoCommon_{i}_.{j}/", (a, b)))

    m = Metric()
    m.parse_ground_truth("data/ground_truth/" + name20)
    m.parse_result("result/csv/result_KTC_ComplexCommon_4_.2/" + name21)
    a = m.chord_symbol_recall()
    m2 = Metric()
    m2.parse_ground_truth("data/ground_truth/" + name20)
    m2.parse_result("result/csv/result_KTC_ComplexCommon_4_.2/" + name21)
    b = m2.chord_symbol_recall()
    res.append(("KTC_ComplexCommon_4_.2", (a, b)))

    m = Metric()
    m.parse_ground_truth("data/ground_truth/" + name20)
    m.parse_result("result/csv/result_KAC_NoCommon_4_.2/" + name21)
    a = m.chord_symbol_recall()
    m2 = Metric()
    m2.parse_ground_truth("data/ground_truth/" + name20)
    m2.parse_result("result/csv/result_KAC_NoCommon_4_.2/" + name21)
    b = m2.chord_symbol_recall()
    res.append(("KAC_NoCommon_4_.2", (a, b)))

    m = Metric()
    m.parse_ground_truth("data/ground_truth/" + name20)
    m.parse_result("result/csv/result_KAC_SimpleCommon_4_.2/" + name21)
    a = m.chord_symbol_recall()
    m2 = Metric()
    m2.parse_ground_truth("data/ground_truth/" + name20)
    m2.parse_result("result/csv/result_KAC_SimpleCommon_4_.2/" + name21)
    b = m2.chord_symbol_recall()
    res.append(("KAC_SimpleCommon_4_.2", (a, b)))

    print(name21)
    for k, t in res:
        print(k, t)


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
