from typing import Dict, Any

from nltk import download, word_tokenize, FreqDist
from nltk.lm.preprocessing import flatten

from pandas import DataFrame, isna
from utils import DELIMITER, OUTPUT_PATH_TASK1, DATA_PATH, INITIAL_COLUMNS, EXTENSION, TRAIN_FILE_NAME, \
    UNIGRAM_FILE_NAME, BIGRAM_FILE_NAME, import_dataset, nltk_ngrams

download('punkt')


def get_words_by_label(df: DataFrame) -> Dict[Any, list]:
    label_words = dict()
    unique_labels = df.labels.unique()

    for label in unique_labels:
        label_words[label] = []
        label_lines = df[df.labels == label]
        for question in label_lines.questions:
            if not isna(question):
                question_words = word_tokenize(question, language='english')
                label_words[label].append(question_words)
        for answer in label_lines.answers:
            if not isna(answer):
                answer_words = word_tokenize(answer, language='english')
                label_words[label].append(answer_words)

    return label_words

def generate_ngrams(words_dict: dict, ngram_order: int, output_path: str = OUTPUT_PATH_TASK1):
    if ngram_order == 1:
        output_file = UNIGRAM_FILE_NAME
    elif ngram_order == 2:
        output_file = BIGRAM_FILE_NAME
    else:
        output_file = UNIGRAM_FILE_NAME

    for tag in words_dict.keys():
        tag_ngrams = [list(nltk_ngrams(sentence, ngram_order)) for sentence in words_dict[tag]]
        tag_ngrams = list(flatten(sentence_ngrams for sentence_ngrams in tag_ngrams))
        freq_dist = FreqDist(tag_ngrams)

        with open(f"{output_path}{output_file}{tag}{EXTENSION}", "w", encoding="utf-8") as writer:
            for entry in freq_dist:
                writer.write(' '.join(list(entry)))
                writer.write(f'{DELIMITER}{str(freq_dist[entry])}\n')


if __name__ == "__main__":
    training_dataset = import_dataset(f'{DATA_PATH}{TRAIN_FILE_NAME}{EXTENSION}', INITIAL_COLUMNS)  # import file train.txt
    label_words_dict = get_words_by_label(training_dataset)
    generate_ngrams(label_words_dict, 1)
    generate_ngrams(label_words_dict, 2)
