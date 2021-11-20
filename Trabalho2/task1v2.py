from utils import DELIMITER, OUTPUT_PATH_TASK1, DATA_PATH, INITIAL_COLUMNS, EXTENSION, TRAIN_FILE_NAME, \
    UNIGRAM_FILE_NAME, BIGRAM_FILE_NAME, import_dataset, nltk_ngrams

import nltk






if __name__ == "__main__":
    training_dataset = import_dataset(f'{DATA_PATH}{TRAIN_FILE_NAME}{EXTENSION}', INITIAL_COLUMNS)  # import file train.txt
    training_dataset['ngrams'] = training_dataset.questions.apply(lambda question:\
        set(nltk.ngrams(nltk.word_tokenize(question), 2, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>')))
    training_dataset.ngrams = training_dataset.ngrams.apply(lambda ngrams: [' '.join(ngram) for ngram in ngrams])

    
    print(training_dataset.head(10))