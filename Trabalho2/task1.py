from typing import List

import nltk
import pandas as pd
from pandas import DataFrame

nltk.download('punkt')

DATA_PATH = "Trabalho2/data/"
OUTPUT_PATH = "Trabalho2/counts/"
DELIMITER = '\t'
TRAIN_FILE_NAME = "train.txt"
TRAIN_COLUMNS = ['labels', 'questions', 'answers']


def import_dataset(path: str, columns: List[str]) -> DataFrame:
    return pd.read_csv(path, sep=DELIMITER, names=columns)  # '\t' for tab delimiter (.tsv)

def get_words_by_tag(df: DataFrame):
    label_words = dict()
    unique_labels = df.labels.unique()

    for label in unique_labels:
        label_words[label] = []
        label_lines = df[df.labels == label]
        for question in label_lines.questions:
            label_words[label].extend(nltk.word_tokenize(question))
        for answer in label_lines.answers:
            label_words[label].extend(nltk.word_tokenize(answer))

    return label_words


def generate_ngrams(words_dict, ngram_order: int):
    if ngram_order == 1:
        output_file = "unigrams"
    elif ngram_order == 2:
        output_file = "bigrams"
    else:
        output_file = "unigrams"

    for tag in words_dict.keys():
        ngrams = nltk.ngrams(words_dict[tag], ngram_order, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>')
        freq_dist = nltk.FreqDist(ngrams)

        with open(f"{OUTPUT_PATH}/{output_file}_{tag}.txt", "a", encoding="utf-8") as writer:
            for entry in freq_dist:
                writer.write(' '.join(list(entry)))
                writer.write(f'{DELIMITER}{str(freq_dist[entry])}\n')


if __name__ == "__main__":
    training_dataset = import_dataset(f'{DATA_PATH}{TRAIN_FILE_NAME}', TRAIN_COLUMNS)  # import file train.txt
    label_words_dict = get_words_by_tag(training_dataset)
    generate_ngrams(label_words_dict, 1)
    generate_ngrams(label_words_dict, 2)
