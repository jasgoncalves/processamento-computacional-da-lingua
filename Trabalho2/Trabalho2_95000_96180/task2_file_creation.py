from pandas import DataFrame
import numpy as np

from utils import DATA_PATH, DELIMITER, EXTENSION, INITIAL_COLUMNS, import_dataset

FILE_NAME = 'test'
FMT = '% s'
LABELS_FILE_NAME = f'{FILE_NAME}-labels'
LABELS_COLUMNS = ['labels']
QUESTIONS_FILE_NAME = f'{FILE_NAME}-questions'
QUESTIONS_COLUMNS = ['questions', 'answers']


def export_dataset(data_frame: DataFrame, columns: str, file_name: str):
    np.savetxt(fname=file_name, X=data_frame.filter(items=columns).values.tolist(), delimiter=DELIMITER, fmt=FMT, encoding='utf-8')


if __name__ == "__main__":
    evaluation_dataset = import_dataset(f'{DATA_PATH}{FILE_NAME}{EXTENSION}', INITIAL_COLUMNS)  # import file eval.txt
    export_dataset(evaluation_dataset, LABELS_COLUMNS,
                   f'{DATA_PATH}{LABELS_FILE_NAME}{EXTENSION}')  # create file eval-labels.txt
    export_dataset(evaluation_dataset, QUESTIONS_COLUMNS,
                   f'{DATA_PATH}{QUESTIONS_FILE_NAME}{EXTENSION}')  # create file eval-questions.txt
