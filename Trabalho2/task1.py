from typing import List, Dict, Any

import nltk
from pandas import DataFrame

from Trabalho2.utils import DELIMITER, OUTPUT_PATH_TASK1, DATA_PATH, INITIAL_COLUMNS, EXTENSION, TRAIN_FILE_NAME, \
    UNIGRAM_FILE_NAME, BIGRAM_FILE_NAME, import_dataset, nltk_ngrams

nltk.download('punkt')


def clean_words(words: List[str]) -> List[str]:
    return [word for word in words if word.isalnum()]


def get_words_by_label(df: DataFrame) -> Dict[Any, list]:
    label_words = dict()
    unique_labels = df.labels.unique()

    for label in unique_labels:
        label_words[label] = []
        label_lines = df[df.labels == label]
        for question in label_lines.questions:
            question_words = nltk.word_tokenize(question, language='english')
            label_words[label].extend(clean_words(question_words))
        for answer in label_lines.answers:
            answer_words = nltk.word_tokenize(answer, language='english')
            label_words[label].extend(clean_words(answer_words))

    return label_words


def generate_ngrams(words_dict: Dict[Any, list], ngram_order: int, output_path: str = OUTPUT_PATH_TASK1):
    if ngram_order == 1:
        output_file = UNIGRAM_FILE_NAME
    elif ngram_order == 2:
        output_file = BIGRAM_FILE_NAME
    else:
        output_file = UNIGRAM_FILE_NAME

    for tag in words_dict.keys():
        ngrams = nltk_ngrams(words_dict[tag], ngram_order)
        freq_dist = nltk.FreqDist(ngrams)

        with open(f"{output_path}{output_file}{tag}{EXTENSION}", "w", encoding="utf-8") as writer:
            for entry in freq_dist:
                writer.write(' '.join(list(entry)))
                writer.write(f'{DELIMITER}{str(freq_dist[entry])}\n')


if __name__ == "__main__":
    training_dataset = import_dataset(f'{DATA_PATH}{TRAIN_FILE_NAME}{EXTENSION}', INITIAL_COLUMNS)  # import file train.txt
    label_words_dict = get_words_by_label(training_dataset)
    generate_ngrams(label_words_dict, 1)
    generate_ngrams(label_words_dict, 2)
