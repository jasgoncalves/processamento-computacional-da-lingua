import os
from typing import List

import nltk
import chardet
import pandas as pd

PROJECT_PATH = os.path.dirname("Trabalho2")
DATA_PATH = os.path.join(PROJECT_PATH, "data/")
OUTPUT_PATH_TASK1 = os.path.join(PROJECT_PATH, "counts/")
OUTPUT_PATH_TASK3 = os.path.join(PROJECT_PATH, "counts2/")
DELIMITER = '\t'
EXTENSION = '.txt'
INITIAL_COLUMNS = ['labels', 'questions', 'answers']
DATA_COLUMNS = ['questions', 'answers']
TRAIN_FILE_NAME = "train"
UNIGRAM_FILE_NAME = 'unigrams_'
BIGRAM_FILE_NAME = 'bigrams_'


def import_dataset(path: str, columns: str) -> pd.DataFrame:
    with open(path, 'rb') as f:
        enc = chardet.detect(f.read())
    return pd.read_csv(path, sep=DELIMITER, names=columns, encoding=enc['encoding'])  # '\t' for tab delimiter (.tsv)


def nltk_ngrams(tokens_list: List[str], ngram_order: int):
    return nltk.ngrams(tokens_list, ngram_order, pad_left=True, pad_right=True, left_pad_symbol='<s>',
                       right_pad_symbol='</s>')
