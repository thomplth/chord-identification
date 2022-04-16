if __name__ == "__main__":
    import os
    import sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from chord_constant import MAJOR_CHORD_DICT, MINOR_CHORD_DICT
from preprocess.note import Note
import csv

import sys

# Given the scale and the chord, output the notes of the chord


def pick_chord(tonic, chord, is_major):
    chord_intervals = MAJOR_CHORD_DICT[chord] if is_major else MINOR_CHORD_DICT[chord]
    base_note = tonic
    chord_notes = []
    for interval in chord_intervals:
        next_note = base_note.get_note_by_interval(interval)
        # If you get some strange notes, just DO NOT return that chord
        # if next_note.accidental > 2 or next_note.accidental < -2:
        #     return None
        chord_notes.append(next_note)
        base_note = next_note
    return chord_notes


def get_files(filename=None):
    all_scores = [f for f in os.listdir(
        '../../data/ground_truth') if f.endswith(".csv")]
    # print(all_scores)
    if filename in all_scores:
        return [filename]
    return all_scores

ENHAR = {
    'B#': 'C',
    'C-': 'B',
    'D-': 'C#',
    'E-': 'D#',
    'E#': 'F',
    'F-': 'E',
    'G-': 'F#',
    'A-': 'G#',
    'B-': 'A#'
}

if __name__ == "__main__":
    inpath = '../../data/ground_truth' + '/'
    outpath = '../../data/chord/' + 'KYDataset/'
    files = get_files()
    
    print(len(files))
    for filename in files:
        print('>>>', filename)

        infile = open(inpath + filename, 'r')
        outfile = open(outpath + filename, 'w', newline='')
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        offset = 0.0
        tonic, chord, is_major = '?', '?', '?'
        notecount = {n: 0.0 for n in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']}
        chroma = [0.0 for _ in range(12)]

        headers = next(reader)
        writer.writerow(('offset', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b'))
        for row in reader:
            try:
                new_offset = float(row[0])
            except ValueError:
                num, den = row[0].split( '/' )
                new_offset = float(num) / float(den)

            while new_offset > offset + 1.0:
                offset += 1
                writer.writerow(tuple([offset] + chroma))

            counter = notecount.copy()

            # print(row)
            offset = new_offset
            tonic, chord, is_major = Note(input_str=row[1]), row[3], row[2]

            try:
                notes = pick_chord(tonic, chord, is_major == 'M')

                for note in notes:
                    s = note.__str__()
                    if s not in counter:
                        if s not in ENHAR:
                            print('>>>', s)

                        s = ENHAR[s]
                    counter[s] += 1.0

                chroma = list(counter.values())
                # print(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
                # print(chroma)
                # print([note.__str__() for note in notes])
            except KeyError:
                print(">>> ERROR <<<")
                print(row)

            writer.writerow(tuple([offset] + chroma))

        infile.close()
        outfile.close()

'''
def get_files(filename=None):
    all_scores = [f for f in os.listdir(
        '../../data/ground_truth_Schubert') if f.endswith(".csv")]
    # print(all_scores)
    if filename in all_scores:
        return [filename]
    return all_scores

ENHAR = {
    'B#': 'C',
    'C-': 'B',
    'D-': 'C#',
    'E-': 'D#',
    'E#': 'F',
    'F-': 'E',
    'G-': 'F#',
    'A-': 'G#',
    'B-': 'A#'
}

if __name__ == "__main__":
    inpath = '../../data/ground_truth' + '_Schubert/'
    outpath = '../../data/chord/' + 'Schubert/'
    for filename in get_files():
        print('>>>', filename)

        infile = open(inpath + filename, 'r')
        outfile = open(outpath + filename, 'w', newline='')
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        offset = 0.0
        tonic, chord, is_major = '?', '?', '?'
        notecount = {n: 0.0 for n in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']}
        chroma = [0.0 for _ in range(12)]

        headers = next(reader)
        writer.writerow(('offset', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b'))
        for row in reader:
            try:
                new_offset = float(row[0])
            except ValueError:
                num, den = row[0].split( '/' )
                new_offset = float(num) / float(den)

            while new_offset > offset + 1.0:
                offset += 1
                writer.writerow(tuple([offset] + chroma))

            counter = notecount.copy()

            # print(row)
            offset = new_offset
            tonic, chord, is_major = Note(input_str=row[1]), row[3], row[2]

            try:
                notes = pick_chord(tonic, chord, is_major == 'M')

                for note in notes:
                    s = note.__str__()
                    if s not in counter:
                        if s not in ENHAR:
                            print('>>>', s)

                        s = ENHAR[s]
                    counter[s] += 1.0

                chroma = list(counter.values())
                # print(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
                # print(chroma)
                # print([note.__str__() for note in notes])
            except KeyError:
                print(">>> ERROR <<<")
                print(row)

            writer.writerow(tuple([offset] + chroma))

        infile.close()
        outfile.close()
'''