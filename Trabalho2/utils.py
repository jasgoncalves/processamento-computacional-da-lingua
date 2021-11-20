import os
from typing import List
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import pad_sequence
import chardet
import pandas as pd
import enum
import spacy
from nltk.corpus import stopwords

try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenize/punkt')
except:
    nltk.download('punkt')
    nltk.download('stopwords')

PROJECT_PATH = os.path.dirname("Trabalho2")
DATA_PATH = os.path.join(PROJECT_PATH, "data/")
OUTPUT_PATH_TASK1 = os.path.join(PROJECT_PATH, "counts/")
OUTPUT_PATH_TASK3 = os.path.join(PROJECT_PATH, "counts2/")
DELIMITER = '\t'
EXTENSION = '.txt'
INITIAL_COLUMNS = ['labels', 'questions', 'answers']
DATA_COLUMNS = ['questions', 'answers']
TRAIN_FILE_NAME = "train"
EVAL_FILE_NAME = "eval"
UNIGRAM_FILE_NAME = 'unigrams_'
BIGRAM_FILE_NAME = 'bigrams_'
nlp = spacy.load("en_core_web_sm")

class Ngram(enum.Enum):
    UNIGRAM = 0,
    BIGRAM = 1,
    BIGRAM_SMOOTHING = 2

class Label(enum.Enum):
    GEOGRAPHY = 0,
    HISTORY = 1,
    LITERATURE = 2,
    MUSIC = 3,
    SCIENCE = 4

def to_labels(sentence : list) -> str: 
    text = ' '.join(sentence)
    doc = nlp(text)
    for ent in doc.ents:
        text = text.replace(ent.text, f'__{ent.label_}__')
    return word_tokenize(text)
    

def to_lemma(sentence : list) -> str: 
    lemmatizer = nltk.WordNetLemmatizer()
    return [lemmatizer.lemmatize(word, pos='v') for word in sentence]

def to_stem(sentence : list) -> str:
    stemmer = nltk.LancasterStemmer()
    return [stemmer.stem(word) for word in sentence]

def remove_stopwords(sentence : list) -> str: 
    return [word for word in sentence if word not in stopwords.words('english')]

def clean_words(words: List[str]) -> List[str]: return [word for word in words if word.isalnum()]
def to_lower(words: List[str]) -> List[str]: return [word.lower() for word in words]
def to_year(words: List[str]) -> List[str]: return ["__YEAR__" if word.isnumeric() and len(word) == 4 else word for word in words ]


MAPPER_FUNCTIONS = [to_lemma, to_year, to_lower]


def import_dataset(path: str, columns: str) -> pd.DataFrame:
    with open(path, 'rb') as f:
        enc = chardet.detect(f.read())
    return pd.read_csv(path, sep=DELIMITER, names=columns, encoding=enc['encoding'])  # '\t' for tab delimiter (.tsv)


def nltk_ngrams(tokens_list: List[str], ngram_order: int):
    return nltk.ngrams(pad_sequence(tokens_list, n= 2, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'), ngram_order)


def apply_transform_functions(words: List[str]) -> List[str]:
    for func in MAPPER_FUNCTIONS:
        words = func(words)
    return words
