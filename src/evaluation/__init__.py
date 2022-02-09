import configparser
import os
import csv
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from preprocess.piece import Piece

CONFIG = configparser.ConfigParser()
configpath = os.path.dirname(os.path.dirname(__file__))
CONFIG.read(os.path.join(configpath, "config.ini"))

try:
    DATA_PATH = CONFIG["locations"]["data_path"]
    RESULT_PATH = CONFIG["locations"]["result_path"]
except KeyError:
    print("failed to read config.ini, or invalid index specified")
    raise SystemExit


class Metric:
    """Supplementary class for evaluation of key and/or chord prediction with established metrics
    """

    def __init__(self, piece):
        """
        :param piece: music piece for evaluation
        :type piece: Piece object in preprocess package
        """
        self.piece = piece
        self.length = piece.length
        self.results = {'key': {}, 'chord': {}}
        self.target = {'key': None, 'chord': None}

    # def __parse_result(self, filename, seventh=True):
    #     res = []
    #     with open(RESULT_PATH + filename + ".csv", newline="") as f:
    #         reader = csv.reader(f)
    #         data = [tuple(row) for row in reader]

    #     for row in data:
    #         try:
    #             if seventh:
    #                 numeral = row[1]
    #             else:
    #                 numeral = row[1].split("7")[0]
    #             offset = float(row[0])
    #         except ValueError:
    #             x, y = map(int, row[0].split("/"))  # int or float? int now
    #             offset = x / y
    #         res.append((numeral, row[2], offset))

    #     return res

    # def __parse_ground_truth(self, filename):
    #     res = []
    #     with open(GT_PATH + filename + ".pydata", "rb") as f:
    #         data = pickle.load(f)

    #     for chord, offset in data:
    #         numeral, scale = self.convert_chord_name(chord)
    #         res.append((numeral, scale, offset))

    #     return res

    def __convert_chord_name(self, chord):
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

    def perfect_matches(self, prediction, type='chord'):
        """Perfect Matches
        Hard evaluation method for key or chord identification and segmentation. Only matches in both identification and segmentation are counted.

        :return: number of matches and segments
        :rtype: tuple of (int, int)
        """
        target = self.piece.get_ground_truth(type=type)
        length = min(len(prediction), len(target))

        matched = 0
        for i in range(length):
            if prediction[i] == target[i][1]:
                matched += 1

        return (matched, length)

    def directional_hamming_distance(self, prediction, type='chord'):
        """Lost ._."""
        pass

    def symbolic_recall(self, prediction, type='chord'):
        """Chord Symbol Recall (CSR), also known as Average Overlap Score or Relative Correct Overlap
        MIREX has used an approximate chord_symbol_recall calculated by sampling both the ground-truth and the automatic annotations every 10 ms and dividing the number of correctly annotated samples by the total number of samples. Following Christopher Harte (2010, §8.1.2)

        :return: score in 0-1 range
        :rtype: float
        """
        if not self.target[type]:
            self.target[type] = self.piece.get_ground_truth(type=type)

        target = self.target[type]
        matched_duration = 0.0
        pd_idx = 0

        # Calculate relative matched overlap of prediction (PD) with ground truth (GT) data as basis
        for gt_idx, target_segment in enumerate(target):

            # Retrieve GT local Start and End offsets
            gt_start = target_segment[0]
            if gt_idx + 1 < len(target):
                gt_end = target[gt_idx + 1][1]
            else:
                gt_end = self.length

            # Increment matching duration if predicted chord matches with GT
            # End if PD segment time exceed GT
            while True:

                # Retrieve PD local Start and End offsets
                pd_start = max(prediction[pd_idx]['offset'], gt_start)
                if pd_idx + 1 < len(prediction):
                    pd_end = prediction[pd_idx + 1]['offset']
                else:
                    pd_end = self.length

                # Obtain chord prediction and target
                predicted_chord = prediction[pd_idx]['chord']['chord']
                predicted_scale = prediction[pd_idx]['chord']['scale']
                target_chord = target_segment['chord']
                target_scale = target_segment['scale']

                # Check if prediction matches with target
                if (predicted_chord == target_chord and predicted_scale == target_scale):
                    matched_duration += min(pd_end - pd_start, gt_end - pd_start)
                    print(f"Matched at {gt_start} for {pd_start} - {pd_end}")
                else:
                    print(f"Unmatched prediction at {pd_start}: ")
                    if predicted_chord != target_chord:
                        print(f"(predicted) {predicted_chord} (target) {target_chord}")
                    if predicted_scale != target_scale:
                        print(f"(predicted) {predicted_scale} (target) {target_scale}")

                if gt_end == pd_end:
                    pd_idx += 1
                    break
                elif gt_end < pd_end:
                    break
                else:
                    pd_idx += 1

        return matched_duration / self.length

    def key_symbol_recall(self, prediction):
        """Implemented Chord Symbol Recall method for Keys

        :return: score in 0-1 range
        :rtype: float
        """
        if not self.target:
            self.target = self.piece.get_ground_truth(type='key')

        matched_duration = 0.0
        pd_idx = 0

        # Calculate relative matched overlap of prediction (PD) with ground truth (GT) data as basis
        for gt_idx, target_segment in enumerate(self.target):

            # Retrieve GT local Start and End offsets
            gt_start = target_segment[0]
            if gt_idx + 1 < len(self.target):
                gt_end = self.target[gt_idx + 1][1]
            else:
                gt_end = self.length

            # Increment matching duration if predicted key matches with GT
            # End if PD segment time exceed GT
            while True:

                # Retrieve PD local Start and End offsets
                pd_start = max(prediction[pd_idx]['offset'], gt_start)
                if pd_idx + 1 < len(prediction):
                    pd_end = prediction[pd_idx + 1]['offset']
                else:
                    pd_end = self.length

                # Obtain key prediction and target
                predicted_scale = prediction[pd_idx]['chord']['scale']
                target_scale = target_segment['key']

                # Check if prediction matches with target
                if (predicted_scale == target_scale):
                    matched_duration += min(pd_end - pd_start, gt_end - pd_start)
                    print(f"Matched at {gt_start} for {pd_start} - {pd_end}")
                else:
                    print(f"Unmatched prediction at {pd_start}: (predicted) {predicted_scale} (target) {target_scale}")

                if gt_end == pd_end:
                    pd_idx += 1
                    break
                elif gt_end < pd_end:
                    break
                else:
                    pd_idx += 1

        return matched_duration / self.length

    def evaluate(self, prediction, type):
        """Generate results with all relative evaluation metrics

        :param prediction: ...
        :type type: ...
        :param type: 'chord' or 'key' segments, defaults to 'chord'
        :type type: str, optional
        """
        if type == 'chord':
            self.target['chord'] = self.piece.get_ground_truth()

            self.results['chord']['PM'] = self.perfect_matches(prediction)
            self.results['chord']['CSR'] = self.symbolic_recall(prediction)
        elif type == 'key':
            self.target['key'] = self.piece.get_ground_truth(type='key')

            self.results['key']['PM'] = self.perfect_matches(prediction, type='key')
            self.results['key']['KSR'] = self.symbolic_recall(prediction, type='key')

    def export_results(self):
        pass

    def show(self):
        """Print all test results. Run after evaluate()
        """
        pass


if __name__ == "__main__":
    p = Piece("anonymous_Twinkle_Twinkle")
    m = Metric(p)

    print(p.get_ground_truth())
    m.symbolic_recall(p.get_ground_truth())
