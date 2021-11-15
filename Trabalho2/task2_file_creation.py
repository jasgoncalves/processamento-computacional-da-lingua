import pandas as pd
from pandas import DataFrame
import numpy as np

DATA_PATH = "Trabalho2\\data\\"
DELIMITER = '\t'
EVAL_FILE_NAME = "eval.txt"
EVAL_COLUMNS = ['labels', 'questions', 'answers']
FMT = '% s'
LABELS_FILE_NAME = "eval-labels.txt"
LABELS_COLUMNS = ['labels']
QUESTIONS_FILE_NAME = "eval-questions.txt"
QUESTIONS_COLUMNS = ['questions', 'answers']


def import_dataset(path : str, columns : str) -> DataFrame:
    return pd.read_csv(path, sep = DELIMITER, names = columns) # '\t' for tab delimiter (.tsv)

def export_dataset(data_frame : DataFrame, columns : str, file_name : str):
    np.savetxt(fname = file_name, X = data_frame.filter(items=columns).values.tolist(), delimiter = DELIMITER, fmt = FMT)

if __name__ == "__main__":
    evaluation_dataset = import_dataset(f'{DATA_PATH}{EVAL_FILE_NAME}', EVAL_COLUMNS) # import file eval.txt
    export_dataset(evaluation_dataset, LABELS_COLUMNS, f'{DATA_PATH}{LABELS_FILE_NAME}') # create file eval-labels.txt
    export_dataset(evaluation_dataset, QUESTIONS_COLUMNS, f'{DATA_PATH}{QUESTIONS_FILE_NAME}') # create file eval-questions.txt