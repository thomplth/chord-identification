import csv
import os
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


class Metric:

    def __init__(self):
        self.ground_truth = []
        self.result = []

    def get_length(self, filename):
        score = converter.parse(filename + ".mxl")
        self.name = filename
        self.length = score.duration.quarterLength

    def CSR(self):
        try:
            if not self.ground_truth or not self.result:
                return False
            match_duration = 0.0
            res_idx = 0
            for gt_idx, segment in enumerate(self.ground_truth):
                gt_start = segment[2]
                if gt_idx+1 < len(self.ground_truth):
                        gt_end = self.ground_truth[gt_idx+1][2]
                else:
                    gt_end = self.length

                while True:
                    res_start = max(self.result[res_idx][2], gt_start)
                    if res_idx+1 < len(self.result):
                        res_end = self.result[res_idx+1][2]
                    else:
                        res_end = self.length

                    if self.result[res_idx][0] == segment[0] and self.result[res_idx][1] == segment[1]:
                        match_duration += min(res_end - res_start, gt_end - res_start)
                        # print(f'Matched at {gt_start} for {res_start} - {res_end}')
                    # else:
                    #     if self.result[res_idx][1] == segment[1]:
                    #         print(f'Unmatched result at {res_start}: <{self.result[res_idx][0]}-{segment[0]}>')
                    #     elif self.result[res_idx][0] == segment[0]:
                    #         print(f'Unmatched result at {res_start}: <{self.result[res_idx][1]}-{segment[1]}>')
                    #     else:
                    #         print(f'Unmatched result at {res_start}: <{self.result[res_idx][0]}-{segment[0]}>, <{self.result[res_idx][1]}-{segment[1]}>')

                    if gt_end == res_end:
                        res_idx += 1
                        break
                    elif gt_end < res_end:
                        break
                    else:
                        res_idx += 1
        except Exception as e:
            print(self.name)
            print(res_idx)
            return -1

        return match_duration / self.length

    def parse_result(self, filename, seventh=True):
        with open(filename + '.csv', newline='') as f:
            reader = csv.reader(f)
            data = [tuple(row) for row in reader]
        for row in data:
            try:
                if seventh:
                    numeral = row[1]
                else:
                    numeral = row[1].split('7')[0]
                offset = float(row[0])
            except ValueError:
                x, y = map(int, row[0].split('/'))  # int or float? int now
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
        if len(scale) > 1:
            if scale[1] == 'b':
                scale = scale[0] + '-'
            elif scale[1] == '#':
                scale = scale[0] + '#'
            else:
                print(scale)

        if a[-1] == 'M':
            scale = scale + ' Major'
        else:
            scale = scale.lower() + ' Minor'
        return numeral, scale


if __name__ == "__main__":
    scores = [f[:-4] for f in os.listdir('data/') if os.path.isfile('data/' + f)]
    scores.remove(
        "Beethoven_L.V._Sonatina_in_A-Flat_Major_(Op.110_No.31)_2nd_Movement"
    )
    # offset for Beethoven_L.V._Sonatina_in_A_Major_(Op.101_No.28)_2nd_Movement seems to be wrong?

    d = {}
    for score in scores:
        if not os.path.exists('data/ground_truth/' + score + '.pydata'):
            continue

        name20 = name21 = score
        res = []
        for i in [3, 4]:
            for j in [1, 2]:
                m = Metric()
                m.get_length('data/' + name21)
                m.parse_ground_truth('data/ground_truth/' + name20)
                m.parse_result(f'result/csv/result_KTC_NoCommon_{i}_.{j}/' + name21)
                a = m.CSR()

                m2 = Metric()
                m2.get_length('data/' + name21)
                m2.parse_ground_truth('data/ground_truth/' + name20)
                m2.parse_result(f'result/csv/result_KTC_NoCommon_{i}_.{j}/' + name21, seventh=False)
                b = m2.CSR()
                res.append((f'KTC_NoCommon_{i}_.{j}', (a, b)))

        m = Metric()
        m.get_length('data/' + name21)
        m.parse_ground_truth('data/ground_truth/' + name20)
        m.parse_result('result/csv/result_KTC_ComplexCommon_4_.2/' + name21)
        a = m.CSR()
        m2 = Metric()
        m2.get_length('data/' + name21)
        m2.parse_ground_truth('data/ground_truth/' + name20)
        m2.parse_result('result/csv/result_KTC_ComplexCommon_4_.2/' + name21)
        b = m2.CSR()
        res.append(('KTC_ComplexCommon_4_.2', (a, b)))

        m = Metric()
        m.get_length('data/' + name21)
        m.parse_ground_truth('data/ground_truth/' + name20)
        m.parse_result('result/csv/result_KTC_SimpleCommon_4_.2/' + name21)
        a = m.CSR()
        m2 = Metric()
        m2.get_length('data/' + name21)
        m2.parse_ground_truth('data/ground_truth/' + name20)
        m2.parse_result('result/csv/result_KTC_SimpleCommon_4_.2/' + name21)
        b = m2.CSR()
        res.append(('KTC_SimpleCommon_4_.2', (a, b)))

        m = Metric()
        m.get_length('data/' + name21)
        m.parse_ground_truth('data/ground_truth/' + name20)
        m.parse_result('result/csv/result_KAC_NoCommon_4_.2/' + name21)
        a = m.CSR()
        m2 = Metric()
        m2.get_length('data/' + name21)
        m2.parse_ground_truth('data/ground_truth/' + name20)
        m2.parse_result('result/csv/result_KAC_NoCommon_4_.2/' + name21)
        b = m2.CSR()
        res.append(('KAC_NoCommon_4_.2', (a, b)))

        m = Metric()
        m.get_length('data/' + name21)
        m.parse_ground_truth('data/ground_truth/' + name20)
        m.parse_result('result/csv/result_KAC_SimpleCommon_4_.2/' + name21)
        a = m.CSR()
        m2 = Metric()
        m2.get_length('data/' + name21)
        m2.parse_ground_truth('data/ground_truth/' + name20)
        m2.parse_result('result/csv/result_KAC_SimpleCommon_4_.2/' + name21)
        b = m2.CSR()
        res.append(('KAC_SimpleCommon_4_.2', (a, b)))

        d[score] = res

    for k, v in d.items():
        path = f'result/evaluation/{k}.csv'
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(('Mode', 'Param', 'Strict', 'Relaxed'))
            for mode, score in v:
                writer.writerow((mode[:3], mode[4:], score[0], score[1]))
