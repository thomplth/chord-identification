if __name__ == "__main__":
    import os, sys

    sys.path.insert(1, os.path.join(sys.path[0], ".."))

from utility.entities import Note_duration_dict
from preprocess.note import Note


def determine_valid_combined_segment_by_tree(
    note_profile: Note_duration_dict, rule_based_result: bool, models
):
    chroma: list[float] = [0.0 for _ in range(12)]
    for note, duration in note_profile.items():
        pitch = Note(input_str=note).get_pitch_class()
        chroma[pitch] += duration
    chroma = [round(dur, 6) for dur in chroma]
    chroma.reverse()

    # use models
    results = [rule_based_result]
    for model in models:
        pred = model.predict([chroma])
        results.append(pred[0])
    # print(results, results.count(True) > results.count(False))
    # pooling:
    return results.count(True) > results.count(False)
