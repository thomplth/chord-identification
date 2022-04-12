import numpy as np
import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score, auc
from matplotlib import pyplot as plt
from joblib import dump
from itertools import combinations
from imblearn.combine import SMOTEENN

RANDOM_STATE = 24
best_alpha = 0


def preparation():
    training_csv = []
    testing_csv = []
    abc_csv = []

    test_data = [
        "Chopin_F._Prelude_in_D-Flat_Major_Op.28_No.15",
        "Chopin_F._Nocturne_in_F_Minor_Op.55_No.1",
        "Beethoven_L.V._Sonata_in_A-Flat_Major_(Op.110_No.31)_2nd_Movement",
        "anonymous_Twinkle_Twinkle",
        "Chopin_F._Etude_in_F_Minor_Op.10_No.9",
        "Mendelsshon_F._Songs_Without_Words_(Op._19_No._6)",
        "Schubert_D911-23",
        "Schubert_D911-24",
    ]
    for dirname, _, filenames in os.walk("/kaggle/input"):
        for filename in filenames:
            file_name = os.path.join(dirname, filename)
            if filename.startswith("op"):
                abc_csv.append(file_name)
            elif filename[:-4] in test_data:
                testing_csv.append(file_name)
            else:
                training_csv.append(file_name)

    def create_dataframe(csv_list, li=False):
        df_list = []
        for csv in csv_list:
            df = pd.read_csv(csv, index_col=None, header=0)
            if li:
                print(csv, df["chord_tonality"].value_counts())
            df_list.append(df)
        df = pd.concat(df_list, axis=0, ignore_index=True)
        return df

    static_training_df = create_dataframe(training_csv)
    static_testing_df = create_dataframe(testing_csv)
    abc_df = create_dataframe(abc_csv)

    def clean_data(df):
        # remove strange things:
        # case 1: sum of chroma is 0
        df = df[df["total"] > 0]
        # case 2: no chord (is_major = None)
        df = df.dropna(axis=0, how="any")
        return df

    static_training_df = clean_data(static_training_df)
    static_testing_df = clean_data(static_testing_df)
    abc_df = clean_data(abc_df)

    def split_train_test(dataflame, train_size=0.85):
        train, test = train_test_split(
            dataflame, train_size=train_size, random_state=RANDOM_STATE
        )
        return train, test

    train, test = split_train_test(abc_df)
    static_training_df = pd.concat(
        [static_training_df, train], axis=0, ignore_index=True
    )
    static_testing_df = pd.concat([static_testing_df, test], axis=0, ignore_index=True)
    static_testing_df.append(test)
    print(static_training_df["chord_tonality"].value_counts())
    print(static_testing_df["chord_tonality"].value_counts())
    return static_training_df, static_testing_df


def simplify_label(simplicity, df):
    # Higher simplicity, fewer labels
    if simplicity > 0:
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
    if simplicity > 1:
        # further simplify
        df.loc[df["chord_tonality"] == "Augmented", "chord_tonality"] = "Major"
        df.loc[df["chord_tonality"] == "Augmented sixth", "chord_tonality"] = "Major"
        df.loc[df["chord_tonality"] == "Diminished", "chord_tonality"] = "Minor"
    return df


def split_label(dataflame):
    X = dataflame.drop(
        ["offset", "tonic", "total", "numeral", "chord_tonality"], axis=1
    ).copy()
    Y = dataflame["chord_tonality"].copy()
    Y = pd.get_dummies(Y)  # One hot encoding
    return X, Y


def generate_chroma_diff_header(num_list):
    indices_pairs = list(combinations(num_list, 2))
    header = [
        f"{min(val_1, val_2)}/{max(val_1, val_2)}" for val_1, val_2 in indices_pairs
    ]
    return header


old_header = generate_chroma_diff_header(range(12))

# Parameters Handling
def boolean_chroma(dataflame):
    dataflame[old_header] = dataflame[old_header].astype("bool")
    return dataflame


# more data points
def chroma_augmentation(dataflame):
    augmented_dataflame = dataflame.copy()
    for idx in range(1, 12):
        df = dataflame.copy()
        new_header = generate_chroma_diff_header(
            list(range(idx, 12)) + list(range(idx))
        )
        rename_dict = dict(zip(old_header, new_header))
        df = df.rename(columns=rename_dict)
        augmented_dataflame = pd.concat([augmented_dataflame, df], ignore_index=True)
    return augmented_dataflame


def get_roc(test_Y, pred, labels):
    test_Y = test_Y.to_numpy()  # convert into numpy
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    print(test_Y)
    print(pred)
    for i in range(len(labels)):
        class_name = labels[i]
        tmp = roc_curve(test_Y[:, i], pred[:, i])
        fpr[class_name], tpr[class_name], _ = tmp
        roc_auc[class_name] = auc(fpr[class_name], tpr[class_name])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(test_Y.ravel(), pred.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    plt.figure(figsize=(8.5, 8.5))
    for cls_name in fpr.keys():
        plt.plot(
            fpr[cls_name],
            tpr[cls_name],
            label="ROC curve of class {0} (area = {1:0.3f})".format(
                cls_name, roc_auc[cls_name]
            ),
        )
    plt.plot([0, 1], [0, 1], "k--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.02])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Some extension of Receiver operating characteristic to multiclass")
    plt.legend(loc="lower right")
    plt.show()
    print("roc_auc = {0:0.4f}".format(roc_auc_score(test_Y, pred)))


def build_tree(train_X, train_Y, max_depth, alpha=0):
    decision_tree = DecisionTreeClassifier(
        random_state=RANDOM_STATE,
        ccp_alpha=alpha,
        max_depth=max_depth,
    )
    decision_tree = decision_tree.fit(train_X, train_Y)
    return decision_tree


def test_tree(decision_tree, test_X, test_Y, labels):
    pred = decision_tree.predict(test_X)
    print(classification_report(test_Y, pred, target_names=labels))
    return pred


def get_ccp_alphas_graph(
    decision_tree, chroma_train, form_train, chroma_test, form_test
):
    # get_ccp_alphas
    ccp_alphas = decision_tree.cost_complexity_pruning_path(
        chroma_train, form_train
    ).ccp_alphas[:-1]
    ccp_alphas = list(set([min(max(0, alpha), 1) for alpha in ccp_alphas]))
    ccp_alphas.sort()
    new_trees = [build_tree(chroma_train, form_train, alpha) for alpha in ccp_alphas]
    train_scores = [clf.score(chroma_train, form_train) for clf in new_trees]
    test_scores = [clf.score(chroma_test, form_test) for clf in new_trees]
    fig, ax = plt.subplots()
    ax.set_xlabel("alpha")
    ax.set_ylabel("accuracy")
    ax.set_title("Accuracy vs alpha for training and testing sets")
    ax.plot(ccp_alphas, train_scores, marker="o", label="train", drawstyle="steps-post")
    ax.plot(ccp_alphas, test_scores, marker="o", label="test", drawstyle="steps-post")
    ax.legend()
    plt.show()

    # get tree with highest test scores:
    best_score = max(test_scores)
    best_tree_idx = test_scores.index(best_score)
    # only the first one (but it is better as it has higher train score, usually)
    best_tree = new_trees[best_tree_idx]
    return best_tree


def balance_dataset(X, Y):
    smt = SMOTEENN(random_state=RANDOM_STATE)
    X_smt, y_smt = smt.fit_resample(X, Y.to_numpy())
    return X_smt, y_smt


static_training_df, static_testing_df = preparation()
