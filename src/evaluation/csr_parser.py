import csv
import pickle
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

class Metric:
    
    def __init__(self):
        self.ground_truth = []
        self.result = []

    def CSR(self):
        if not self.ground_truth or not self.result:
            return False
        # gt_start = 0.0
        res_start, res_end = 0.0, self.result[0][2]
        match_duration = 0.0
        res_idx = 0
        for segment in self.ground_truth:
            gt_end = segment[2]
            while True:
                if self.result[res_idx][0] == segment[0] and self.result[res_idx][1] == segment[1]:
                    match_duration += res_end - res_start
                else:
                    print(f'Unmatched result from {round(res_start, 2)}: <{self.result[res_idx][0]}-{segment[0]}>, <{self.result[res_idx][1]}-{segment[1]}>')
                
                if res_idx+1 >= len(self.result):
                    break
                if self.result[res_idx+1][2] < gt_end:
                    res_start = res_end
                    res_idx += 1
                    res_end = self.result[res_idx][2]
                else:
                    break
            # gt_start = gt_end
        return match_duration / self.ground_truth[-1][2]

    def parse_result(self, filename):
        with open(filename + '.csv', newline='') as f:
            reader = csv.reader(f)
            data = [tuple(row) for row in reader]
        for row in data:
            try:
                numeral = row[1].split('7')[0]
                offset = float(row[0])
            except ValueError:
                x, y = map(int, row[0].split('/')) # int or float? int now
                offset = x / y
            self.result.append((numeral, row[2], offset))

    def parse_ground_truth(self, filename):
        with open(filename + '.pydata', 'rb') as f:
            data = pickle.load(f)

        for chord, offset in data:
            numeral, scale = self.convert_chord_name(chord)
            self.ground_truth.append((numeral, scale, offset))

    def convert_chord_name(self, chord):
        a, b = chord.split('(')
        scale = a[:-1]
        numeral = b[:-1]
        if a[-1] == 'M':
            scale = scale + ' Major'
        else:
            scale = scale.lower() + ' Minor'
        return numeral, scale


if __name__ == "__main__":
    m = Metric()
    m.parse_ground_truth('data/ground_truth/Twinkle-Twinkle')
    m.parse_result('result/csv/result_KTC_NoCommon_3_.1/anonymous_Twinkle_Twinkle')
    print(m.CSR())
