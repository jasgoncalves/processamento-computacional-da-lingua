import nltk
import enum
import pandas as pd
from pandas import DataFrame

class Label(enum.Enum):
    GEOGRAPHY = 0,
    HISTORY = 1,
    LITERATURE = 2,
    MUSIC = 3,
    SCIENCE = 4

LABELS_DATA_PATH = 'Trabalho2\\counts\\'
DELIMITER = ' '
COLUMNS = ['word', 'freq']
UNIGRAM_FILE_NAME = 'unigrams_'
BIGRAM_FILE_NAME = 'bigrams_'
EXTENSION = '.txt'
LABELS = [Label.GEOGRAPHY, Label.HISTORY, Label.LITERATURE, Label.MUSIC, Label.SCIENCE]

__geography = None
__history = None
__literature = None
__music = None
__science = None

def import_dataset(path : str, columns : str) -> DataFrame:
    return pd.read_csv(path, sep = DELIMITER, names = columns) # '\t' for tab delimiter (.tsv)

def ngram_load_data(file_name : str) -> tuple(DataFrame, DataFrame, DataFrame, DataFrame, DataFrame):
    return\
        import_dataset(f'{LABELS_DATA_PATH}{file_name}{Label.GEOGRAPHY.name}{EXTENSION}', COLUMNS),\
        import_dataset(f'{LABELS_DATA_PATH}{file_name}{Label.HISTORY.name}{EXTENSION}', COLUMNS),\
        import_dataset(f'{LABELS_DATA_PATH}{file_name}{Label.LITERATURE.name}{EXTENSION}', COLUMNS),\
        import_dataset(f'{LABELS_DATA_PATH}{file_name}{Label.MUSIC.name}{EXTENSION}', COLUMNS),\
        import_dataset(f'{LABELS_DATA_PATH}{file_name}{Label.SCIENCE.name}{EXTENSION}', COLUMNS)

def ngram_classification(sentence : str, ngram_calculation : function) -> str:
    value, new_value, label = ngram_calculation(sentence, __geography), unigram_calculation(sentence, __history), Label.GEOGRAPHY.name
    if new_value > value:
        value, label = new_value, Label.HISTORY.name
    new_value = ngram_calculation(sentence, __literature)
    if new_value > value:
        value, label = new_value, Label.LITERATURE.name
    new_value = ngram_calculation(sentence, __music)
    if new_value > value:
        value, label = new_value, Label.MUSIC.name
    new_value = ngram_calculation(sentence, __science)
    if new_value > value:
        label = Label.SCIENCE.name
    
    return label

## handling unknown words
def unigram_word_likehood(value : int, words_list : int, threshold : float = .05) -> float:
    return ((1 - threshold) * (value / words_list)) + (threshold / words_list) if words_list != 0 else 0

def unigram_calculation(sentence : str, dataset : DataFrame) -> float:
    words_list = len(dataset)
    calculation = 1
    for word in nltk.word_tokenize(sentence): 
        try:
            value = dataset[dataset.word == word].freq.iloc[0]
        except:
            value = 0
        calculation *= unigram_word_likehood(value, words_list)
    
    return calculation

def bigram_calculation(sentence : str, dataset : DataFrame) -> float:
    words_list = len(dataset)
    calculation = 1
    for word in nltk.word_tokenize(sentence): 
        try:
            value = dataset[dataset.word == word].freq.iloc[0]
        except:
            value = 0
        calculation *= unigram_word_likehood(value, words_list)
    
    return calculation

def unigram_classification(sentence : str) -> str:
    return ngram_classification(sentence, unigram_calculation)

def bigram_classification(sentence : str) -> str:
    return ngram_classification(sentence, bigram_calculation)

def unigram_load_data() -> tuple(DataFrame, DataFrame, DataFrame, DataFrame, DataFrame):
    return ngram_load_data(UNIGRAM_FILE_NAME)

def bigram_load_data() -> tuple(DataFrame, DataFrame, DataFrame, DataFrame, DataFrame):
    return ngram_load_data(BIGRAM_FILE_NAME)

if __name__ == "__main__":
    
    __geography, __history, __literature, __music, __science = unigram_load_data()

    print(unigram_classification('This book by Virginia Woolf inspired Michael Cunningham''s novel ""The Hours""')) ## LITERATURE
    print(unigram_classification('The ""amiable"" former name of the Tongan archipelago')) ## GEOGRAPHY
    print(unigram_classification('PBS fans know that ""Evening at Pops"" refers to this city''s Pops')) ## MUSIC
    print(unigram_classification('According to Chuck Jones, whenever possible, this force of nature was to be Wile E. Coyote''s greatest enemy')) ## SCIENCE
    print(unigram_classification('In 1843 Congress allocated $30,000 to string one between Baltimore & Washington; it was completed in 1844')) ## HISTORY
    
    __geography, __history, __literature, __music, __science = bigram_load_data()
    
    print(bigram_classification('This book by Virginia Woolf inspired Michael Cunningham''s novel ""The Hours""')) ## LITERATURE
    print(bigram_classification('The ""amiable"" former name of the Tongan archipelago')) ## GEOGRAPHY
    print(bigram_classification('PBS fans know that ""Evening at Pops"" refers to this city''s Pops')) ## MUSIC
    print(bigram_classification('According to Chuck Jones, whenever possible, this force of nature was to be Wile E. Coyote''s greatest enemy')) ## SCIENCE
    print(bigram_classification('In 1843 Congress allocated $30,000 to string one between Baltimore & Washington; it was completed in 1844')) ## HISTORY