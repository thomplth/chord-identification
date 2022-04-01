import numpy as np
import random
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score
from utility import get_files

RANDOM_STATE = 24
TRAINING_DATA_PATH = "../data/SegmentedChroma/KYDataset"
old_header = list(
    map(
        str,
        "c c# d d# e f f# g g# a a# b".split(" "),
    )
)

# TODO: handle tonic also
def chroma_augmentation(dataflame):
    augmented_dataflame = dataflame.copy()

    for idx in range(1, 12):
        df = dataflame.copy()
        new_header = old_header[idx:] + old_header[:idx]
        rename_dict = dict(zip(old_header, new_header))
        df = df.rename(columns=rename_dict)
        augmented_dataflame = pd.concat([augmented_dataflame, df], ignore_index=True)
    return augmented_dataflame


# TODO: handle tonic also
def chroma_alignment(df):
    note_to_pitch_dict = {
        "C#": 1,
        "D-": 1,
        "D": 2,
        "D#": 3,
        "E-": 3,
        "E": 4,
        "F": 5,
        "F#": 6,
        "G-": 6,
        "G": 7,
        "G#": 8,
        "A-": 8,
        "A": 9,
        "A#": 10,
        "B-": 10,
        "B": 11,
    }
    aligned_chromas = df.loc[(df["tonic"] == "C")]
    for tonic, pitch in note_to_pitch_dict.items():
        tmp_chroma = df.loc[(df["tonic"] == tonic)]
        new_header = old_header[-pitch:] + old_header[:-pitch]
        rename_dict = dict(zip(old_header, new_header))
        tmp_chroma = tmp_chroma.rename(columns=rename_dict)
        aligned_chromas = pd.concat([aligned_chromas, tmp_chroma], ignore_index=True)
    return aligned_chromas


# Prepare
def sepearate_data(training_data_path):
    training_csv = get_files(training_data_path, ".csv")
    df_list = []
    for csv in training_csv:
        df = pd.read_csv(TRAINING_DATA_PATH + "/" + csv, index_col=None, header=0)
        df_list.append(df)
    df = pd.concat(df_list, axis=0, ignore_index=True)

    # remove strange things:
    # case 1: sum of chroma is 0
    df = df[df["total"] > 0]
    # case 2: no chord (is_major = None)
    df = df.dropna(axis=0, how="any")

    # rotation of chroma
    # df = chroma_augmentation(df)
    df = chroma_alignment(df)

    def simplify_label():
        df.loc[df["chord_tonality"] == "Major seventh", ["chord_tonality"]] = "Major"
        df.loc[df["chord_tonality"] == "Dominant seventh", "chord_tonality"] = "Major"
        df.loc[df["chord_tonality"] == "Minor seventh", "chord_tonality"] = "Minor"
        df.loc[
            df["chord_tonality"] == "Diminished seventh", "chord_tonality"
        ] = "Diminished"
        df.loc[
            df["chord_tonality"] == "Half-diminished seventh", "chord_tonality"
        ] = "Diminished"
        df.loc[
            df["chord_tonality"] == "Italian sixth", "chord_tonality"
        ] = "Augmented sixth"
        df.loc[
            df["chord_tonality"] == "German sixth", "chord_tonality"
        ] = "Augmented sixth"
        df.loc[
            df["chord_tonality"] == "French sixth", "chord_tonality"
        ] = "Augmented sixth"
        # further simplify
        # df.loc[df["chord_tonality"] == "Augmented", "chord_tonality"] = "Major"
        # df.loc[df["chord_tonality"] == "Augmented sixth", "chord_tonality"] = "Major"
        # df.loc[df["chord_tonality"] == "Diminished", "chord_tonality"] = "Minor"

    simplify_label()

    X = df.drop(
        ["offset", "tonic", "total", "numeral", "chord_tonality"], axis=1
    ).copy()

    Y = df["chord_tonality"].copy()
    Y = pd.get_dummies(Y)  # One hot encoding
    print(Y)

    chroma_train, chroma_test, form_train, form_test = train_test_split(
        X, Y, train_size=0.9, random_state=RANDOM_STATE
    )
    return chroma_train, chroma_test, form_train, form_test


def display_tree(decision_tree, feature_names):
    result = export_text(decision_tree, feature_names=feature_names)
    print(result)


# Building Tree
def build_tree(train_X, train_Y, alpha=0):
    decision_tree = DecisionTreeClassifier(
        random_state=RANDOM_STATE, splitter="random", ccp_alpha=alpha
    )
    decision_tree = decision_tree.fit(train_X, train_Y)

    # display_tree(decision_tree, feature_names=list(train_X))
    return decision_tree


def test_tree(decision_tree, test_X, test_Y):
    pred = decision_tree.predict(test_X)
    # print(confusion_matrix(test_Y, pred))
    print(classification_report(test_Y, pred))


def get_score(decision_tree, X, Y):
    return decision_tree.score(X, Y)


def prune_tree(decision_tree, train_X, train_Y, test_X, test_Y):
    path = decision_tree.cost_complexity_pruning_path(train_X, train_Y)
    alphas = path.ccp_alphas[:-1]  # last one must be 1

    alphas_details = []
    for a in alphas:
        tmp_dt = decision_tree = DecisionTreeClassifier(
            random_state=RANDOM_STATE, splitter="random", ccp_alpha=a
        )
        scores = cross_val_score(tmp_dt, train_X, train_Y, cv=5)
        alphas_details.append((a, np.mean(scores), np.std(scores)))
        best_alpha = max(alphas_details, key=lambda item: item[1])[0]

    # best_alpha = alphas.index(max_test_score)
    return max(best_alpha + (random.random() * 0.05 - 0.05), 0)


def main():
    best_alpha = 0
    chroma_train, chroma_test, form_train, form_test = sepearate_data(
        TRAINING_DATA_PATH
    )

    decision_tree = build_tree(chroma_train, form_train, best_alpha)
    # display_tree(decision_tree, feature_names=list(chroma_train))
    test_tree(decision_tree, chroma_test, form_test)
    # best_alpha = prune_tree(
    #     decision_tree, chroma_train, form_train, chroma_test, form_test
    # )
    # print(best_alpha)


if __name__ == "__main__":
    main()
