import os
from typing import Dict, Any, List
import pandas as pd
from task1 import get_words_by_label, generate_ngrams
from utils import import_dataset, OUTPUT_PATH_TASK3, DATA_PATH, TRAIN_FILE_NAME, EXTENSION, INITIAL_COLUMNS, \
    apply_transform_functions, PROJECT_PATH, EVAL_FILE_NAME

OUTPUT_FOLDER = os.path.join(PROJECT_PATH, "data-processed/")


def data_pre_processing(words_dict: Dict[Any, List]) -> Dict[Any, List]:
    for label in words_dict.keys():
        words_dict[label] = list(map(lambda sentence: apply_transform_functions(sentence), words_dict[label]))

    return words_dict


def write_pre_processing(words_dict: Dict[Any, List]) -> None:
    with open(f"{OUTPUT_FOLDER}/words_by_tag.txt", "w", encoding="utf-8") as writer:
        for label in words_dict.keys():
            for sentence in words_dict[label]:
                writer.write(label + "\t" + " ".join(sentence) + "\n")


if __name__ == "__main__":
    training_dataset = import_dataset(f'{DATA_PATH}{TRAIN_FILE_NAME}{EXTENSION}', INITIAL_COLUMNS)  # import file train.txt
    evaluation_dataset = import_dataset(f'{DATA_PATH}{EVAL_FILE_NAME}{EXTENSION}', INITIAL_COLUMNS)  # import file eval.txt
    dataset = pd.concat([training_dataset, evaluation_dataset])
    label_words_dict = get_words_by_label(dataset)
    label_words_dict = data_pre_processing(label_words_dict)
    write_pre_processing(label_words_dict)
    generate_ngrams(label_words_dict, 1, OUTPUT_PATH_TASK3)
    generate_ngrams(label_words_dict, 2, OUTPUT_PATH_TASK3)
