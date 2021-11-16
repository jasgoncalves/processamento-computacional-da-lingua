from ctypes import ArgumentError
import nltk
import enum
from numpy import log10
import pandas as pd
from pandas import DataFrame

class Label(enum.Enum):
    GEOGRAPHY = 0,
    HISTORY = 1,
    LITERATURE = 2,
    MUSIC = 3,
    SCIENCE = 4

class Ngram(enum.Enum):
    UNIGRAM = 0,
    BIGRAM = 1,

LABELS_DATA_PATH = 'Trabalho2\\counts\\'
DELIMITER = '\t'
COLUMNS = ['word', 'freq']
UNIGRAM_FILE_NAME = 'unigrams_'
BIGRAM_FILE_NAME = 'bigrams_'
EXTENSION = '.txt'
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

def import_dataset(path : str, columns : str) -> DataFrame:
    return pd.read_csv(path, sep = DELIMITER, names = columns) # '\t' for tab delimiter (.tsv)

def ngram_load_data(file_name : str) -> DataFrame:
    return\
        import_dataset(f'{LABELS_DATA_PATH}{file_name}{Label.GEOGRAPHY.name}{EXTENSION}', COLUMNS),\
        import_dataset(f'{LABELS_DATA_PATH}{file_name}{Label.HISTORY.name}{EXTENSION}', COLUMNS),\
        import_dataset(f'{LABELS_DATA_PATH}{file_name}{Label.LITERATURE.name}{EXTENSION}', COLUMNS),\
        import_dataset(f'{LABELS_DATA_PATH}{file_name}{Label.MUSIC.name}{EXTENSION}', COLUMNS),\
        import_dataset(f'{LABELS_DATA_PATH}{file_name}{Label.SCIENCE.name}{EXTENSION}', COLUMNS)

def ngram_classification(sentence : str, ngram : Ngram) -> str:

    value, label, new_value = get_calculation(sentence, Label.GEOGRAPHY, ngram), Label.GEOGRAPHY.name, get_calculation(sentence, Label.HISTORY, ngram)
    # print(f'{Label.GEOGRAPHY.name}:{value}') 
    # print(f'{Label.HISTORY.name}:{new_value}') 
    if new_value > value:
        value, label = new_value, Label.HISTORY.name
    new_value = get_calculation(sentence, Label.LITERATURE, ngram)
    # print(f'{Label.LITERATURE.name}:{new_value}') 
    if new_value > value:
        value, label = new_value, Label.LITERATURE.name
    new_value = get_calculation(sentence, Label.MUSIC, ngram)
    # print(f'{Label.MUSIC.name}:{new_value}') 
    if new_value > value:
        value, label = new_value, Label.MUSIC.name
    new_value = get_calculation(sentence, Label.SCIENCE, ngram)
    # print(f'{Label.SCIENCE.name}:{new_value}') 
    if new_value > value:
        value, label = new_value, Label.SCIENCE.name
    return label

def get_calculation(sentence : str, label : Label, ngram : Ngram):
    if(ngram == ngram.UNIGRAM):
        return unigram_calculation(sentence, label)
    elif(ngram == ngram.BIGRAM):
        return bigram_calculation(sentence, label)
    else:
        raise ArgumentError(f"Invalid arument value {ngram.name}")

def get_dataframe(label : Label, ngram : Ngram):
    if(ngram == ngram.UNIGRAM):
        return get_unigram_dataframe(label)
    elif(ngram == ngram.BIGRAM):
        return get_bigram_dataframe(label)
    else:
        raise ArgumentError(f"Invalid arument value {ngram.name}")

def get_unigram_dataframe(label : Label):
    if(label == label.GEOGRAPHY):
        return __geography_unigram
    if(label == label.HISTORY):
        return __history_unigram
    if(label == label.SCIENCE):
        return __science_unigram
    if(label == label.LITERATURE):
        return __literature_unigram
    if(label == label.MUSIC):
        return __music_unigram
    else:
        raise ArgumentError(f"Invalid arument value {label.name}")

def get_bigram_dataframe(label : Label):
    if(label == label.GEOGRAPHY):
        return __geography_bigram
    if(label == label.HISTORY):
        return __history_bigram
    if(label == label.SCIENCE):
        return __science_bigram
    if(label == label.LITERATURE):
        return __literature_bigram
    if(label == label.MUSIC):
        return __music_bigram
    else:
        raise ArgumentError(f"Invalid arument value {label.name}")

## handling unknown words
def unigram_likehood(unigram_count : int, words_count : int, threshold : float = 0) -> float:
    return log10(((threshold * unigram_count / words_count) + ((1 - threshold) / words_count) if words_count != 0 else 0))

def bigram_likehood(unigram_count : int, bigram_count : int, smooth : bool, words_count : int ) -> float:
    value = log10(bigram_count / unigram_count if unigram_count != 0 else 0) 
    return value

def unigram_calculation(sentence : str, label : Label) -> float:
    dataset = get_dataframe(label, Ngram.UNIGRAM)
    words_count = len(dataset)
    calculation = 1
    for word in nltk.word_tokenize(sentence):
        try:
            value = dataset[dataset.word == word].freq.iloc[0]
        except:
            value = 0
        calculation += unigram_likehood(value, words_count, UNIGRAM_THRESHOLD)
    return calculation

def bigram_calculation(sentence : str, label : Label, smooth : bool = True) -> float:
    unigram_dataset = get_dataframe(label, Ngram.UNIGRAM)
    bigram_dataset = get_dataframe(label, Ngram.BIGRAM)
    unigram_dataset, bigram_dataset = rebuil_matrix(sentence, unigram_dataset, bigram_dataset)
    words_count = len(unigram_dataset)
    calculation = 1
    for bigram in nltk.ngrams(nltk.word_tokenize(sentence), 2, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'):
        try:
            unigram_value = unigram_dataset[unigram_dataset.word == bigram[0]].freq.iloc[0]
        except:
            unigram_value = 0
        try:
            bigram_value = bigram_dataset[bigram_dataset.word == ' '.join(bigram)].freq.iloc[0]
        except:
            bigram_value = 0
        calculation += bigram_likehood(unigram_value, bigram_value, smooth, words_count)
    return calculation

def rebuil_matrix(sentence: str, unigram_dataset : DataFrame, bigram_dataset : DataFrame):
    words_count = len(unigram_dataset)
    for bigram in nltk.ngrams(nltk.word_tokenize(sentence), 2, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'):
        df = unigram_dataset[unigram_dataset.word == bigram[0]]
        if df.empty:
            words_count += 1
            unigram_dataset.loc[len(unigram_dataset.index)] = [bigram[0], 0]
        df = unigram_dataset[unigram_dataset.word == bigram[0]]
        if df.empty:
            words_count += 1
            unigram_dataset.loc[len(unigram_dataset.index)] = [bigram[1], 0]
        df = bigram_dataset[bigram_dataset.word == ' '.join(bigram)]
        if df.empty:
            bigram_dataset.loc[len(bigram_dataset.index)] = [' '.join(bigram), 0]
            bigram_dataset.freq = bigram_dataset.freq.apply(lambda freq: freq + 1)
    unigram_dataset.freq = unigram_dataset.freq.apply(lambda freq: freq + words_count)
    
    return unigram_dataset, bigram_dataset

def unigram_classification(sentence : str) -> str:
    return ngram_classification(sentence, Ngram.UNIGRAM) 

def bigram_classification(sentence : str) -> str:
    return ngram_classification(sentence, Ngram.BIGRAM)     

def unigram_load_data() -> DataFrame:
    return ngram_load_data(UNIGRAM_FILE_NAME)

def bigram_load_data() -> DataFrame:
    return ngram_load_data(BIGRAM_FILE_NAME)

if __name__ == "__main__":

    __geography_unigram, __history_unigram, __literature_unigram, __music_unigram, __science_unigram = unigram_load_data()

    # print(unigram_classification('This book by Virginia Woolf inspired Michael Cunningham''s novel ""The Hours""')) ## LITERATURE
    # print(unigram_classification('The ""amiable"" former name of the Tongan archipelago')) ## GEOGRAPHY
    # print(unigram_classification('PBS fans know that ""Evening at Pops"" refers to this city''s Pops')) ## MUSIC
    # print(unigram_classification('According to Chuck Jones, whenever possible, this force of nature was to be Wile E. Coyote''s greatest enemy')) ## SCIENCE
    # print(unigram_classification('In 1843 Congress allocated $30,000 to string one between Baltimore & Washington; it was completed in 1844')) ## HISTORY

    __geography_bigram, __history_bigram, __literature_bigram, __music_bigram, __science_bigram = bigram_load_data()

    print(bigram_classification("This book by Virginia Woolf inspired Michael Cunningham's novel ""The Hours""")) ## LITERATURE
    print(bigram_classification("The ""amiable"" former name of the Tongan archipelago")) ## GEOGRAPHY
    print(bigram_classification("PBS fans know that ""Evening at Pops"" refers to this city's Pops")) ## MUSIC
    print(bigram_classification("According to Chuck Jones, whenever possible, this force of nature was to be Wile E. Coyote's greatest enemy")) ## SCIENCE
    print(bigram_classification("This state's been ""on my mind"" since it entered the Union 3 times, in 1788, 1868 & 1870")) ## HISTORY