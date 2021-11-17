import argparse
from ctypes import ArgumentError
import enum
import chardet
from pandas import DataFrame
from pandas import read_csv
from numpy import log10
from nltk import word_tokenize, ngrams, download

download('punkt')

from Trabalho2.utils import BIGRAM_FILE_NAME, UNIGRAM_FILE_NAME, EXTENSION, OUTPUT_PATH_TASK1, \
    import_dataset, nltk_ngrams, DATA_COLUMNS


class Label(enum.Enum):
    GEOGRAPHY = 0,
    HISTORY = 1,
    LITERATURE = 2,
    MUSIC = 3,
    SCIENCE = 4


class Ngram(enum.Enum):
    UNIGRAM = 0,
    BIGRAM = 1,
    BIGRAM_SMOOTHING = 2


COLUMNS = ['word', 'freq']
LABELS = [Label.GEOGRAPHY, Label.HISTORY, Label.LITERATURE, Label.MUSIC, Label.SCIENCE]
UNIGRAM_THRESHOLD = .95

__geography_unigram = None
__history_unigram = None
__literature_unigram = None
__music_unigram = None
__science_unigram = None

__geography_bigram = None
__history_bigram = None
__literature_bigram = None
__music_bigram = None
__science_bigram = None


def ngram_load_data(file_name: str) -> DataFrame:
    return \
        import_dataset(f'{OUTPUT_PATH_TASK1}{file_name}{Label.GEOGRAPHY.name}{EXTENSION}', COLUMNS), \
        import_dataset(f'{OUTPUT_PATH_TASK1}{file_name}{Label.HISTORY.name}{EXTENSION}', COLUMNS), \
        import_dataset(f'{OUTPUT_PATH_TASK1}{file_name}{Label.LITERATURE.name}{EXTENSION}', COLUMNS), \
        import_dataset(f'{OUTPUT_PATH_TASK1}{file_name}{Label.MUSIC.name}{EXTENSION}', COLUMNS), \
        import_dataset(f'{OUTPUT_PATH_TASK1}{file_name}{Label.SCIENCE.name}{EXTENSION}', COLUMNS)


def ngram_classification(sentence: str, ngram: Ngram) -> str:
    value, label, new_value = get_calculation(sentence, Label.GEOGRAPHY, ngram), Label.GEOGRAPHY.name, get_calculation(
        sentence, Label.HISTORY, ngram)
    if new_value > value:
        value, label = new_value, Label.HISTORY.name
    new_value = get_calculation(sentence, Label.LITERATURE, ngram)
    if new_value > value:
        value, label = new_value, Label.LITERATURE.name
    new_value = get_calculation(sentence, Label.MUSIC, ngram)
    if new_value > value:
        value, label = new_value, Label.MUSIC.name
    new_value = get_calculation(sentence, Label.SCIENCE, ngram)
    if new_value > value:
        value, label = new_value, Label.SCIENCE.name
    return label


def get_calculation(sentence: str, label: Label, ngram: Ngram):
    if (ngram == ngram.UNIGRAM):
        return unigram_calculation(sentence, label)
    elif (ngram == ngram.BIGRAM):
        return bigram_calculation(sentence, label)
    elif(ngram == ngram.BIGRAM_SMOOTHING):
        return bigram_calculation(sentence, label, True)
    else:
        raise ArgumentError(f"Invalid arument value {ngram.name}")


def get_dataframe(label: Label, ngram: Ngram):
    if (ngram == ngram.UNIGRAM):
        return get_unigram_dataframe(label)
    elif(ngram == ngram.BIGRAM or ngram == ngram.BIGRAM_SMOOTHING):
        return get_bigram_dataframe(label)
    else:
        raise ArgumentError(f"Invalid arument value {ngram.name}")


def get_unigram_dataframe(label: Label):
    if (label == label.GEOGRAPHY):
        return __geography_unigram
    if (label == label.HISTORY):
        return __history_unigram
    if (label == label.SCIENCE):
        return __science_unigram
    if (label == label.LITERATURE):
        return __literature_unigram
    if (label == label.MUSIC):
        return __music_unigram
    else:
        raise ArgumentError(f"Invalid arument value {label.name}")


def get_bigram_dataframe(label: Label):
    if (label == label.GEOGRAPHY):
        return __geography_bigram
    if (label == label.HISTORY):
        return __history_bigram
    if (label == label.SCIENCE):
        return __science_bigram
    if (label == label.LITERATURE):
        return __literature_bigram
    if (label == label.MUSIC):
        return __music_bigram
    else:
        raise ArgumentError(f"Invalid arument value {label.name}")


## handling unknown words
def unigram_likehood(unigram_count: int, words_count: int, threshold: float = 0) -> float:
    return log10(
        ((threshold * unigram_count / words_count) + ((1 - threshold) / words_count) if words_count != 0 else 0))


def bigram_likehood(unigram_count : int, bigram_count : int, smooth : bool, vocabulary : int ) -> float:
    value = log10(((bigram_count + 1) / (unigram_count + vocabulary) if unigram_count + vocabulary != 0 else 0) if smooth\
         else (bigram_count / unigram_count if unigram_count != 0 else 0))
    return value

def unigram_calculation(sentence : str, label : Label) -> float:
    unigram_dataframe = get_dataframe(label, Ngram.UNIGRAM)
    calculation = 0
    for word in word_tokenize(sentence):
        word_count = get_word_count(word, unigram_dataframe)
        calculation += unigram_likehood(word_count, len(unigram_dataframe), UNIGRAM_THRESHOLD)
    return calculation

def bigram_calculation(sentence : str, label : Label, smooth : bool = False) -> float:
    unigram_dataframe = get_dataframe(label, Ngram.UNIGRAM)
    bigram_dataframe = get_dataframe(label, Ngram.BIGRAM)
    vocabulary = get_vocabulary_size() if smooth else len(unigram_dataframe)
    calculation = 0
    for bigram in ngrams(word_tokenize(sentence), 2, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'):
        unigram_count = get_word_count(bigram[0], unigram_dataframe)
        bigram_count = get_word_count(' '.join(bigram), bigram_dataframe)
        calculation += bigram_likehood(unigram_count, bigram_count, smooth, vocabulary)
    return calculation

def get_word_count(word : str, dataframe : DataFrame) -> int:
    row = dataframe[dataframe.word == word]
    return row.freq.iloc[0] if not row.empty else 0

def get_vocabulary_size():
    return len(__geography_unigram.merge(__history_unigram, how='outer', on='word')\
        .merge(__literature_unigram, how='outer', on='word')\
            .merge(__music_unigram, how='outer', on='word')\
                .merge(__science_unigram, how='outer', on='word'))

def unigram_load_data(counts_folder : str) -> DataFrame:
    return ngram_load_data(UNIGRAM_FILE_NAME, counts_folder)

def bigram_load_data(counts_folder : str) -> DataFrame:
    return ngram_load_data(BIGRAM_FILE_NAME, counts_folder)


if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(description="Bla bla bla bla ...")
    PARSER.add_argument("classification_type", default=Ngram.UNIGRAM, help="UNIGRAM, BIGRAM, BIGRAM_SMOOTHING")
    PARSER.add_argument('counts_folder', help='Counts files folder')
    PARSER.add_argument('test_file', help='Test dataset file')
    args = PARSER.parse_args()

    __geography_unigram, __history_unigram, __literature_unigram, __music_unigram, __science_unigram = unigram_load_data(args.counts_folder)
    __geography_bigram, __history_bigram, __literature_bigram, __music_bigram, __science_bigram = bigram_load_data(args.counts_folder)

    evaluation_dataframe = import_dataset(f'{DATA_PATH}{args.test_file}', DATA_COLUMNS)
    evaluation_dataframe.questions.apply(lambda question: print(ngram_classification(question, Ngram[args.classification_type])))
