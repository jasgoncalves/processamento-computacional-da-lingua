import argparse
from ctypes import ArgumentError
import enum
from typing import Tuple, List

from numpy import log10
from nltk import word_tokenize, download

from utils import BIGRAM_FILE_NAME, UNIGRAM_FILE_NAME, EXTENSION, \
    import_dataset, nltk_ngrams, DATA_COLUMNS, DATA_PATH, apply_transform_functions, Ngram

download('punkt')
download('stopwords')


class Label(enum.Enum):
    GEOGRAPHY = 0,
    HISTORY = 1,
    LITERATURE = 2,
    MUSIC = 3,
    SCIENCE = 4


COLUMNS = ['word', 'freq']
LABELS = [Label.GEOGRAPHY, Label.HISTORY, Label.LITERATURE, Label.MUSIC, Label.SCIENCE]
UNIGRAM_THRESHOLD = .95
BIGRAM_THRESHOLD = .1

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


def ngram_load_data(file_name: str, count_folder : str) -> Tuple[dict, dict, dict, dict, dict]:
    return \
        import_dataset_as_set(f'{count_folder}/{file_name}', Label.GEOGRAPHY.name), \
        import_dataset_as_set(f'{count_folder}/{file_name}', Label.HISTORY.name), \
        import_dataset_as_set(f'{count_folder}/{file_name}', Label.LITERATURE.name), \
        import_dataset_as_set(f'{count_folder}/{file_name}', Label.MUSIC.name), \
        import_dataset_as_set(f'{count_folder}/{file_name}', Label.SCIENCE.name)


def import_dataset_as_set(file_name: str, label: Label):
    df = import_dataset(f'{file_name}{label}{EXTENSION}', COLUMNS)
    return {row[0]: row[1] for row in df.values.tolist()}


def ngram_classification(sentence: str, ngram: Ngram, vocabulary_size: int = 0, normalize : bool = False) -> str:
    value, label, new_value = \
        get_calculation(sentence, Label.GEOGRAPHY, ngram, vocabulary_size, normalize), \
        Label.GEOGRAPHY.name, \
        get_calculation(sentence, Label.HISTORY, ngram, vocabulary_size, normalize)
    if new_value > value:
        value, label = new_value, Label.HISTORY.name
    new_value = get_calculation(sentence, Label.LITERATURE, ngram, vocabulary_size, normalize)
    if new_value > value:
        value, label = new_value, Label.LITERATURE.name
    new_value = get_calculation(sentence, Label.MUSIC, ngram, vocabulary_size, normalize)
    if new_value > value:
        value, label = new_value, Label.MUSIC.name
    new_value = get_calculation(sentence, Label.SCIENCE, ngram, vocabulary_size, normalize)
    if new_value > value:
        value, label = new_value, Label.SCIENCE.name
    return label


def get_calculation(sentence: str, label: Label, ngram: Ngram, vocabulary_size: int = 0, normalize : bool = False):
    if ngram == ngram.UNIGRAM:
        return unigram_calculation(sentence, label, normalize)
    elif ngram == ngram.BIGRAM:
        return bigram_calculation(sentence, label, normalize)
    elif ngram == ngram.BIGRAM_SMOOTHING:
        return bigram_calculation(sentence, label, True, vocabulary_size, normalize)
    else:
        raise ArgumentError(f"Invalid argument value {ngram.name}")


def get_set(label: Label, ngram: Ngram):
    if ngram == ngram.UNIGRAM:
        return get_unigram_set(label)
    elif ngram == ngram.BIGRAM or ngram == ngram.BIGRAM_SMOOTHING:
        return get_bigram_set(label)
    else:
        raise ArgumentError(f"Invalid argument value {ngram.name}")


def get_unigram_set(label: Label):
    if label == label.GEOGRAPHY:
        return __geography_unigram
    if label == label.HISTORY:
        return __history_unigram
    if label == label.SCIENCE:
        return __science_unigram
    if label == label.LITERATURE:
        return __literature_unigram
    if label == label.MUSIC:
        return __music_unigram
    else:
        raise ArgumentError(f"Invalid argument value {label.name}")


def get_bigram_set(label: Label):
    if label == label.GEOGRAPHY:
        return __geography_bigram
    if label == label.HISTORY:
        return __history_bigram
    if label == label.SCIENCE:
        return __science_bigram
    if label == label.LITERATURE:
        return __literature_bigram
    if label == label.MUSIC:
        return __music_bigram
    else:
        raise ArgumentError(f"Invalid argument value {label.name}")


## handling unknown words
def unigram_likelihood(unigram_count: int, words_count: int, threshold: float = 0) -> float:
    return log10(
        ((threshold * unigram_count / words_count) + ((1 - threshold) / words_count) if words_count != 0 else 0))


def bigram_likelihood(unigram_count: int, bigram_count: int, smooth: bool, vocabulary: int, threshold) -> float:
    value = log10(
        ((bigram_count + threshold) / (unigram_count + (vocabulary * threshold)) if unigram_count + vocabulary != 0 else 0) if smooth else
        (bigram_count / unigram_count if unigram_count != 0 else 0))
    return value

def transform_sentence(sentence: List[str]) -> List[str]:
    sentence = apply_transform_functions(sentence)
    return sentence


def unigram_calculation(sentence: str, label: Label, normalize : bool = False) -> float:
    unigram_dataframe = get_set(label, Ngram.UNIGRAM)
    calculation = 0
    tokenized_sentence = word_tokenize(sentence, language='english')
    if normalize:
        tokenized_sentence = transform_sentence(tokenized_sentence)
    for word in tokenized_sentence:
        word_count = unigram_dataframe.get(word, 0)
        calculation += unigram_likelihood(word_count, len(unigram_dataframe), UNIGRAM_THRESHOLD)
    return calculation


def bigram_calculation(sentence: str, label: Label, smooth: bool = False, vocabulary_size: int = 0, normalize : bool = False) -> float:
    unigram_dataframe = get_set(label, Ngram.UNIGRAM)
    bigram_dataframe = get_set(label, Ngram.BIGRAM)
    vocabulary = vocabulary_size if smooth else len(unigram_dataframe)
    calculation = 0
    tokenized_sentence = word_tokenize(sentence, language='english')
    if normalize:
        tokenized_sentence = transform_sentence(tokenized_sentence)
    for bigram in nltk_ngrams(tokenized_sentence, 2):
        unigram_count = unigram_dataframe.get(bigram[0], 0)
        bigram_count = bigram_dataframe.get(' '.join(bigram), 0)
        calculation += bigram_likelihood(unigram_count, bigram_count, smooth, vocabulary, BIGRAM_THRESHOLD)
    return calculation


def get_vocabulary_size():
    unigram_dict = __geography_unigram.copy()
    unigram_dict.update(__history_unigram)
    unigram_dict.update(__literature_unigram)
    unigram_dict.update(__music_unigram)
    unigram_dict.update(__science_unigram)
    return len(unigram_dict)


def unigram_load_data(count_folder : str):
    return ngram_load_data(UNIGRAM_FILE_NAME, count_folder)


def bigram_load_data(count_folder : str):
    return ngram_load_data(BIGRAM_FILE_NAME, count_folder)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Bla bla bla bla ...")
    PARSER.add_argument("classification_type", default=Ngram.UNIGRAM, help="UNIGRAM, BIGRAM, BIGRAM_SMOOTHING")
    PARSER.add_argument('counts_folder', help='Counts files folder')
    PARSER.add_argument('test_file', help='Test dataset file')
    args = PARSER.parse_args()

    counts_folder = args.counts_folder
    test_file = args.test_file
    classification_type = args.classification_type

    # counts_folder = 'counts2'
    # test_file = 'eval-questions.txt'
    # classification_type = 'UNIGRAM'

    __geography_unigram, __history_unigram, __literature_unigram, __music_unigram, __science_unigram = unigram_load_data(counts_folder)
    __geography_bigram, __history_bigram, __literature_bigram, __music_bigram, __science_bigram = bigram_load_data(counts_folder)
    vocabulary_size = get_vocabulary_size()

    evaluation_dataframe = import_dataset(f'{DATA_PATH}{test_file}', DATA_COLUMNS)
    evaluation_dataframe.questions.apply(
        lambda question: print(ngram_classification(question, Ngram[classification_type], vocabulary_size, True if counts_folder == 'counts2' else False)))
