from nltk.util import ngrams


def get_unigrams(file, output_folder=""):
    tags = dict()

    with open(file) as reader:
        lines = reader.readlines()
        for line in lines:
            print(line.split("\t"))


get_unigrams("data/train.txt")
