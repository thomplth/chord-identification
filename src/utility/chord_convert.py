if __name__ == "__main__":
    import os
    import sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from chord_constant import MAJOR_CHORD_DICT, MINOR_CHORD_DICT
from preprocess.note import Note
from utility import get_files
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


Schubert_time_signature_info = [
    {"denominator": 4, "numerator": 2},
    {"denominator": 8, "numerator": 6},
    {"denominator": 2, "numerator": 2},
    {"denominator": 4, "numerator": 4},
    {"denominator": 4, "numerator": 3},
    {"denominator": 4, "numerator": 3},
    {"denominator": 4, "numerator": 2},
    {"denominator": 4, "numerator": 3},
    {"denominator": 8, "numerator": 3},
    {"denominator": 4, "numerator": 2},
    {"denominator": 8, "numerator": 6},
    {"denominator": 4, "numerator": 2},
    ## line break ###
    {"denominator": 8, "numerator": 6},
    {"denominator": 4, "numerator": 3},
    {"denominator": 4, "numerator": 2},
    {"denominator": 4, "numerator": 3},
    {"denominator": 8, "numerator": 12},
    {"denominator": 4, "numerator": 4},
    {"denominator": 8, "numerator": 6},
    {"denominator": 4, "numerator": 2},
    {"denominator": 4, "numerator": 4},
    {"denominator": 4, "numerator": 2},
    {"denominator": 4, "numerator": 3},
    {"denominator": 4, "numerator": 3},
]

if __name__ == "__main__":
    # inpath = "../../data/ground_truth/KYDataset/"
    # outpath = "../../data/chord/KYDataset/"
    # files = get_files(inpath, ".csv")

    inpath = "../../data/ground_truth/Schubert/"
    chromapath = "../../data/chroma/Schubert/"
    outpath = "../../data/chord/Schubert/"
    files = get_files(inpath, ".csv")

    print(len(files))

    def export_chord_chroma(filename, inpath, outpath, idx):
        print(">>>", filename)
        chromafile = open(chromapath + filename, "r")
        reader = csv.reader(chromafile)
        next(reader)
        offset_threshold = next(reader)[0]
        chromafile.close()

        infile = open(inpath + filename, "r")
        outfile = open(outpath + filename, "w", newline="")
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        offset = 0.0
        tonic, chord, is_major = "?", "?", "?"
        notecount = {n: 0.0 for n in range(12)}
        chroma = [0.0 for _ in range(12)]

        next(reader)
        writer.writerow(
            ("offset", "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b")
        )
        row = next(reader)
        new_offset = float(row[0])

        def align_offset(offset_threshold, new_offset):
            sign_info = Schubert_time_signature_info[idx]
            m = 4 * sign_info["numerator"] / sign_info["denominator"]
            c = offset_threshold - m * new_offset
            return lambda offset: m * offset + c

        align_func = align_offset(float(offset_threshold), float(new_offset))

        infile.seek(0)
        next(reader)
        for row in reader:
            try:
                new_offset = float(row[0])
            except ValueError:
                num, den = row[0].split("/")
                new_offset = float(num) / float(den)
            print(new_offset, align_func(new_offset))
            new_offset = align_func(new_offset)

            while new_offset > offset + 1.0:
                offset += 1
                writer.writerow(tuple([offset] + chroma))

            counter = notecount.copy()

            # print(row)
            offset = new_offset
            tonic, chord, is_major = Note(input_str=row[1]), row[3], row[2]

            try:
                notes = pick_chord(tonic, chord, is_major == "M")
                for note in notes:
                    pitch_class = note.get_pitch_class()
                    counter[pitch_class] += 1.0
                chroma = list(counter.values())
            except KeyError:
                print(">>> ERROR <<<")
                print(row)

            writer.writerow(tuple([offset] + chroma))

        infile.close()
        outfile.close()

    for idx in range(len(files)):
        filename = files[idx]
        export_chord_chroma(filename, inpath, outpath, idx)

    # inpath = "../../data/ground_truth/Schubert/"
    # outpath = "../../data/chord/Schubert/"
    # files = get_files(inpath, ".csv")

    # print(len(files))
    # for filename in files:
    #     export_chord_chroma(filename, inpath, outpath)
