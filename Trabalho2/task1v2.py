from utils import DELIMITER, OUTPUT_PATH_TASK1, DATA_PATH, INITIAL_COLUMNS, EXTENSION, TRAIN_FILE_NAME, \
    UNIGRAM_FILE_NAME, BIGRAM_FILE_NAME, import_dataset, nltk_ngrams

import nltk
import collections, functools, operator


def get_ngrams(sentence):
    return list(nltk.ngrams(nltk.word_tokenize(sentence), 2, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'))

def calculate_ngrams_frequency(ngrams):
    return {row[0]: row[1] for row in nltk.FreqDist([' '.join(ngram) for ngram in ngrams]).items()}

def export_dataset(data_frame, columns: str, file_name: str):
    np.savetxt(fname=file_name, X=data_frame.filter(items=columns).values.tolist(), delimiter=DELIMITER, fmt=FMT, encoding='utf-8')

if __name__ == "__main__":
    training_dataset = import_dataset(f'{DATA_PATH}{TRAIN_FILE_NAME}{EXTENSION}', INITIAL_COLUMNS)  # import file train.txt
    training_dataset['ngrams'] = training_dataset.questions.apply(lambda question: get_ngrams(question))
    training_dataset.ngrams = training_dataset.ngrams.apply(lambda ngrams: calculate_ngrams_frequency(ngrams))


    test = dict(functools.reduce(operator.add, map(collections.Counter, training_dataset.query('labels == "LITERATURE"').ngrams.tolist())))
    
    

    
    print(test)