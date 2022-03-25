import numpy as np
import random
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score

RANDOM_STATE = 48


# Prepare
def sepearate_data(filename):
    df = pd.read_csv(filename)
    X = df.drop(["offset", "total", "form"], axis=1).copy()
    Y = df["form"].copy()
    Y = pd.get_dummies(Y)  # One hot encoding

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
        random_state=RANDOM_STATE, splitter="random", max_depth=3, ccp_alpha=alpha
    )
    decision_tree = decision_tree.fit(train_X, train_Y)

    # display_tree(decision_tree, feature_names=list(train_X))
    return decision_tree


def test_tree(decision_tree, test_X, test_Y):
    pred = decision_tree.predict(test_X)
    print("Accuracy:", accuracy_score(test_Y, pred))


def get_score(decision_tree, X, Y):
    return decision_tree.score(X, Y)


def prune_tree(decision_tree, train_X, train_Y, test_X, test_Y):
    path = decision_tree.cost_complexity_pruning_path(train_X, train_Y)
    alphas = path.ccp_alphas[:-1]  # last one must be 1

    alphas_details = []
    for a in alphas:
        tmp_dt = decision_tree = DecisionTreeClassifier(
            random_state=RANDOM_STATE, splitter="random", max_depth=3, ccp_alpha=a
        )
        scores = cross_val_score(tmp_dt, train_X, train_Y, cv=5)
        alphas_details.append((a, np.mean(scores), np.std(scores)))
        best_alpha = max(alphas_details, key=lambda item: item[1])[0]

    # best_alpha = alphas.index(max_test_score)
    return max(best_alpha + (random.random() * 0.05 - 0.05), 0)


def main():
    best_alpha = 0
    chroma_train, chroma_test, form_train, form_test = sepearate_data(
        "Schubert_D911-01_testingdata.csv"
    )
    for i in range(3):
        decision_tree = build_tree(chroma_train, form_train, best_alpha)
        display_tree(decision_tree, feature_names=list(chroma_train))
        test_tree(decision_tree, chroma_test, form_test)
        best_alpha = prune_tree(
            decision_tree, chroma_train, form_train, chroma_test, form_test
        )
        print(i, best_alpha)


if __name__ == "__main__":
    main()
