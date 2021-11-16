from typing import List, Dict, Any

import nltk
import pandas as pd
from pandas import DataFrame

from Trabalho2.utils import DELIMITER, OUTPUT_PATH, DATA_PATH, INITIAL_COLUMNS, EXTENSION, TRAIN_FILE_NAME, \
    UNIGRAM_FILE_NAME, BIGRAM_FILE_NAME

nltk.download('punkt')


def import_dataset(path: str, columns: List[str]) -> DataFrame:
    return pd.read_csv(path, sep=DELIMITER, names=columns)  # '\t' for tab delimiter (.tsv)


def clean_words(words: List[str]) -> List[str]:
    return [word for word in words if word.isalnum()]


def get_words_by_tag(df: DataFrame) -> Dict[Any, list]:
    label_words = dict()
    unique_labels = df.labels.unique()

    for label in unique_labels:
        label_words[label] = []
        label_lines = df[df.labels == label]
        for question in label_lines.questions:
            question_words = nltk.word_tokenize(question, language='english')
            label_words[label].extend(clean_words(question_words))
        for answer in label_lines.answers:
            answer_words = nltk.word_tokenize(answer, language='english')
            label_words[label].extend(clean_words(answer_words))

    return label_words


def generate_ngrams(words_dict: Dict[Any, list], ngram_order: int):
    if ngram_order == 1:
        output_file = UNIGRAM_FILE_NAME
    elif ngram_order == 2:
        output_file = BIGRAM_FILE_NAME
    else:
        output_file = UNIGRAM_FILE_NAME

    for tag in words_dict.keys():
        ngrams = nltk.ngrams(words_dict[tag], ngram_order, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>')
        freq_dist = nltk.FreqDist(ngrams)

        with open(f"{OUTPUT_PATH}/{output_file}{tag}{EXTENSION}", "w", encoding="utf-8") as writer:
            for entry in freq_dist:
                writer.write(' '.join(list(entry)))
                writer.write(f'{DELIMITER}{str(freq_dist[entry])}\n')


if __name__ == "__main__":
    training_dataset = import_dataset(f'{DATA_PATH}{TRAIN_FILE_NAME}{EXTENSION}', INITIAL_COLUMNS)  # import file train.txt
    label_words_dict = get_words_by_tag(training_dataset)
    generate_ngrams(label_words_dict, 1)
    generate_ngrams(label_words_dict, 2)
