import pandas as pd

import sys
from collections import Counter
from typing import Self
from math import log2

class DecisionTree:
    def __init__(self, df: pd.DataFrame) -> None:
        dataset: pd.DataFrame = df.iloc[:, :-1]
        class_labels: pd.Series = df.iloc[:, -1]
        features: list[str] = df.columns[:-1].to_list()
        feature_values: dict[str, list[str]] = {feature : list(dataset[feature].unique()) for feature in features}
        self.root: DecisionNode = DecisionNode().build(dataset, class_labels, features, feature_values)

    def classify(self, tuple: pd.Series) -> str:
        return self.root.classify(tuple)

class DecisionNode:
    def __init__(self, value: str = None) -> None:
        self.value: str = value
        self.label: str = None
        self.children: list[DecisionNode] = list()

    def build(self, dataset: pd.DataFrame, class_labels: pd.Series, left_features: list[str], feature_values: dict[str, list[str]]) -> Self:
        if len(class_labels.unique()) == 1:
            self.label = class_labels.iloc[0]
            return self
        
        if len(left_features) == 0:
            self.label = Counter(class_labels).most_common(1)[0][0]
            return self

        gain_ratios: dict[str, float] = {feature : gain_ratio(dataset, class_labels, feature) for feature in left_features}
        best_feature: str = max(gain_ratios, key = gain_ratios.get)
        left_features.remove(best_feature)
        self.label = best_feature

        for value in feature_values[best_feature]:
            child_node = DecisionNode(value)
            child_dataset: pd.DataFrame = dataset[dataset[best_feature] == value]
            child_class_labels: pd.Series = class_labels[dataset[best_feature] == value]
            if len(child_class_labels) == 0:
                child_node.label = Counter(class_labels).most_common(1)[0][0]
                self.children.append(child_node)
                continue
            self.children.append(child_node.build(child_dataset, child_class_labels, left_features.copy(), feature_values))
        return self
    
    def classify(self, tuple: pd.Series) -> str:
        if len(self.children) == 0:
            return self.label

        for child_node in self.children:
            if child_node.value == tuple[self.label]:
                return child_node.classify(tuple)
        return self.children[-1].classify(tuple)

def info(class_labels: pd.Series) -> float:
    result: float = 0.
    for count in Counter(class_labels.to_list()).values():
        p: float = count / len(class_labels)
        result -= p * log2(p)
    return result

def gain_ratio(dataset: pd.DataFrame, class_labels: pd.Series, feature: str) -> float:
    info_parent: float = info(class_labels)
    info_children: float = 0.
    split_info: float = 0.

    for value in dataset[feature].unique():
        child_class_labels: pd.Series = class_labels[dataset[feature] == value]
        split_ratio = len(child_class_labels) / len(class_labels)
        info_children += split_ratio * info(child_class_labels)
        split_info -= split_ratio * log2(split_ratio)

    gain: float = info_parent - info_children
    return gain / split_info

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f'usage: python {sys.argv[0]} [training file name] [test file name] [result file name]')
        quit()
    
    training_file_name: str = sys.argv[1]
    test_file_name: str = sys.argv[2]
    result_file_name: str = sys.argv[3]

    training_dataset: pd.DataFrame = pd.read_csv(training_file_name, sep = '\t')
    class_label_name: str = training_dataset.columns[-1]
    decision_tree: DecisionTree = DecisionTree(training_dataset)

    test_dataset: pd.DataFrame = pd.read_csv(test_file_name, sep = '\t')
    test_result: list[str] = [decision_tree.classify(test_dataset.iloc[row_index]) for row_index in range(len(test_dataset))]
    test_dataset[class_label_name] = test_result

    test_dataset.to_csv(result_file_name, sep = '\t', index = False)