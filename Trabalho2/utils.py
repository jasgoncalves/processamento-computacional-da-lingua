import os

PROJECT_PATH = os.path.dirname("Trabalho2")
DATA_PATH = os.path.join(PROJECT_PATH, "data/")
OUTPUT_PATH = os.path.join(PROJECT_PATH, "counts/")
DELIMITER = '\t'
EXTENSION = '.txt'
INITIAL_COLUMNS = ['labels', 'questions', 'answers']
TRAIN_FILE_NAME = "train"
UNIGRAM_FILE_NAME = 'unigrams_'
BIGRAM_FILE_NAME = 'bigrams_'
