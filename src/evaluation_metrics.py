import configparser
import csv
import os
from utility import get_files

# from new_main import main
from preprocess.note import Note
from preprocess.scale import Scale
from preprocess.chord import Chord

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), "config.ini"))

GT_PATH = "../data/ground_truth/testing/"
RESULT_PATH = "../result/"
MEASURE_OUTPUT_PATH = "../result/metrics/"
try:
    KeyThenChordMode = CONFIG["param"]["KeyThenChord"] == "True"
    DTRFMode = CONFIG["param"]["UsingDTRFForSegmentation"] == "True"
    DTRFMode2 = CONFIG["param"]["UsingDTRFForIdentification"] == "True"

except KeyError:
    print("failed to read config.ini, or invalid index specified")
    raise SystemExit


def export_measurement(metrics, filename, KeyThenChordMode, DTRFMode, DTRFMode2):
    path = os.path.join(
        MEASURE_OUTPUT_PATH,
        filename + f"_({KeyThenChordMode}_{DTRFMode}_{DTRFMode2}).csv",
    )
    measure_file = open(path, "w", newline="")
    writer = csv.writer(measure_file)

    writer.writerow(
        (
            "DHD",
            "CSR on Key",
            "CSR on Chord (strict)",
            "CSR on Chord (triad)",
            "CSR on Chord (jazz)",
        )
    )
    writer.writerow(metrics)

    measure_file.close()


def get_gt_list(file_dir):
    gt_file = open(file_dir)
    csv_reader = csv.reader(gt_file)
    gt_list = []
    next(csv_reader)  # no need the header

    # Input lists of chords first
    for row in csv_reader:
        offset, tonic, scale_type, roman_num = row[:4]
        if roman_num == "?":
            continue  # ignore cases that are unknown (cleaner the data)
        tonic_note = Note(input_str=tonic)
        scale = Scale(is_major=scale_type == "M", tonic_note=tonic_note)
        chord = Chord(scale=scale, numeral=roman_num)
        try:
            offset_num = float(offset)
        except:
            # The offset is in fraction
            frac = offset.split("/")
            offset_num = round(float(frac[0]) / float(frac[1]), 6)
        if len(gt_list) > 0:
            gt_list[-1]["end"] = offset_num
            gt_list[-1]["duration"] = offset_num - gt_list[-1]["start"]
        gt_list.append({"chord": chord, "start": offset_num, "end": -1, "duration": -1})
    # gt file has no record on when the piece ends, but result can tell
    gt_file.close()
    # print(gt_list)

    # Remove duplication
    dedup_gt_list = [gt_list[0]]
    for idx in range(1, len(gt_list) - 1):
        if dedup_gt_list[-1]["chord"].is_equal(gt_list[idx]["chord"]):
            dedup_gt_list[-1]["end"] = gt_list[idx]["end"]
            dedup_gt_list[-1]["duration"] += gt_list[idx]["duration"]
        else:
            dedup_gt_list.append(gt_list[idx])
    # print(dedup_gt_list)

    return dedup_gt_list


def get_result_list(file_dir):
    gt_file = open(file_dir)
    csv_reader = csv.reader(gt_file)
    gt_list = []
    next(csv_reader)  # no need the header

    # Input lists of chords first
    for row in csv_reader:
        offset, roman_num, scale_str = row[:3]
        try:
            offset_num = float(offset)
        except:
            # The offset is in fraction
            frac = offset.split("/")
            offset_num = round(float(frac[0]) / float(frac[1]), 6)
        if roman_num == "":
            gt_list[-1]["end"] = offset_num
            break

        tonic, scale_type = scale_str.split(" ")
        tonic_note = Note(input_str=tonic)
        scale = Scale(is_major=scale_type == "Major", tonic_note=tonic_note)
        chord = Chord(scale=scale, numeral=roman_num)

        if len(gt_list) > 0:
            gt_list[-1]["end"] = offset_num
            gt_list[-1]["duration"] = offset_num - gt_list[-1]["start"]
        gt_list.append({"chord": chord, "start": offset_num, "end": -1, "duration": -1})
    # gt file has no record on when the piece ends, but result can tell
    gt_file.close()
    return gt_list


def get_chord_symbol_recall(
    gt_list, result_list, check_type="chord", chord_matching_mode=0
):

    if False and check_type == "key":

        def list_to_scale_only(chord_list):
            res = [chord_list[0]]
            for cd in chord_list[1:]:
                old_scale = res[-1]["chord"].scale
                new_scale = cd["chord"].scale
                if old_scale.is_equal(new_scale):
                    res[-1]["end"] = cd["end"]
                    res[-1]["duration"] += cd["duration"]
                else:
                    res.append(cd)
            return res

        gt_list = list_to_scale_only(gt_list)
        result_list = list_to_scale_only(result_list)

    gt_len = len(gt_list)
    result_len = len(result_list)
    total_duration = result_list[-1]["end"]
    match_duration = 0.0

    gt_idx, result_idx = 0, 0
    while True:
        gt = gt_list[gt_idx]
        res = result_list[result_idx]

        gt_chord = gt["chord"]
        res_chord = res["chord"]

        # If equal then add duration
        check_equal = False
        if check_type == "chord":
            check_equal = gt_chord.is_equal(
                res_chord,
                on_triad=chord_matching_mode == 1,
                on_jazz=chord_matching_mode == 2,
            )
        elif check_type == "key":
            check_equal = gt_chord.scale.is_equal(res_chord.scale)
        if check_equal:
            dur = min(gt["duration"], res["duration"])
            match_duration += dur

        # TODO: debug
        # if check_type == "key":
        #     print(
        #         gt_chord.scale.__str__(),
        #         res_chord.scale.__str__(),
        #         gt_idx,
        #         result_idx,
        #         match_duration,
        #     )

        # pointers moving:
        if gt["end"] < res["end"] and gt_idx < gt_len - 1:
            gt_idx += 1
        elif gt["end"] > res["end"] and result_idx < result_len - 1:
            result_idx += 1
        else:
            if gt_idx == gt_len - 1 and result_idx == result_len - 1:
                break
            gt_idx += 1
            result_idx += 1
    return round(match_duration / total_duration, 6)


def get_directional_hamming_distance(gt_list, result_list):
    gt_len = len(gt_list)
    total_duration = result_list[-1]["end"]
    match_duration = 0.0

    for gt_idx in range(gt_len):
        gt = gt_list[gt_idx]
        res = [
            r for r in result_list if r["start"] < gt["end"] and r["end"] > gt["start"]
        ]
        if len(res) == 0:
            continue
        res_start = min([r["start"] for r in res])
        res_end = max([r["end"] for r in res])

        dur = min(gt["duration"], res_end - res_start)
        match_duration += dur

    return round(match_duration / total_duration, 6)


def generate_report(KeyThenChordMode, DTRFMode, DTRFMode2):
    # load ground truth
    gt_files = get_files(GT_PATH, ".csv")
    for file_str in gt_files:
        print(">> Currently handling: " + file_str)
        gt_list = get_gt_list(GT_PATH + file_str)
        result_list = get_result_list(RESULT_PATH + "chords/" + file_str)
        gt_list[-1]["end"] = result_list[-1]["end"]
        gt_list[-1]["duration"] = result_list[-1]["end"] - gt_list[-1]["start"]

        # directional hamming distance
        dhd = min(
            get_directional_hamming_distance(gt_list, result_list),
            get_directional_hamming_distance(result_list, gt_list),
        )
        metrics = [dhd]

        # chord symbol recall
        modes = [("key", 0)]
        modes.extend([("chord", idx) for idx in range(3)])
        csr_list = [
            get_chord_symbol_recall(
                gt_list,
                result_list,
                check_type=check_type,
                chord_matching_mode=matching_mode,
            )
            for check_type, matching_mode in modes
        ]
        metrics.extend(csr_list)
        # export measurement
        export_measurement(
            tuple(metrics), file_str, KeyThenChordMode, DTRFMode, DTRFMode2
        )


if __name__ == "__main__":
    if True:
        # for idx in range(8):
        #     KeyThenChordMode = (idx & 4) > 0
        #     DTRFMode = (idx & 2) > 0
        #     DTRFMode2 = (idx & 1) > 0
        #     # main(KeyThenChordMode, DTRFMode, DTRFMode2)
        #     generate_report(KeyThenChordMode, DTRFMode, DTRFMode2)
        gt_files = get_files(MEASURE_OUTPUT_PATH, ".csv")
        path = os.path.join(MEASURE_OUTPUT_PATH, "overall.csv")
        measure_file = open(path, "w", newline="")
        writer = csv.writer(measure_file)
        writer.writerow(
            (
                "Score",
                "DHD",
                "CSR on Key",
                "CSR on Chord (strict)",
                "CSR on Chord (triad)",
                "CSR on Chord (jazz)",
                "KeyThenChordMode",
                "DTRFModeSeg",
                "DTRFModeIden",
            )
        )
        for gt_file in gt_files:
            measure_file = open(MEASURE_OUTPUT_PATH + gt_file, "r")
            csv_reader = csv.reader(measure_file)
            next(csv_reader)
            row = next(csv_reader)
            # print(row)

            gt_info = gt_file.split(".csv")
            name = gt_info[0]
            setting = gt_info[1][2:-1].split("_")

            print(name, setting)
            writer.writerow([name] + row + setting)

            measure_file.close()

        #

        measure_file.close()