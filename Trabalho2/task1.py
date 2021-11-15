import itertools
import nltk

nltk.download('punkt')


def get_words_by_tag(file):
    tags = dict()

    with open(file) as reader:
        lines = reader.readlines()
        for line in lines:
            line_split = line.split("\t")
            category = line_split[0]
            words = list(itertools.chain.from_iterable([nltk.word_tokenize(sentence) for sentence in line_split[1:]]))
            if category not in tags.keys():
                tags[category] = []
            tags[category].extend(words)

    return tags


words_by_tag = get_words_by_tag("data/train.txt")


def generate_unigrams(file, output_folder="counts"):
    global words_by_tag
    if not words_by_tag:
        words_by_tag = get_words_by_tag(file)

    for tag in words_by_tag.keys():
        unigrams = nltk.ngrams(words_by_tag[tag], 1, pad_left=True, pad_right=True, left_pad_symbol='<s>',
                                    right_pad_symbol='</s>')
        freq = nltk.FreqDist(unigrams)
        with open("{0}/unigrams_{1}.txt".format(output_folder, tag), "a") as writer:
            for entry in freq:
                writer.write(entry[0] + " " + str(freq[entry]) + "\n")


def generate_bigrams(file, output_folder="counts"):
    global words_by_tag
    if not words_by_tag:
        words_by_tag = get_words_by_tag(file)

    for tag in words_by_tag.keys():
        bigrams = nltk.ngrams(words_by_tag[tag], 2, pad_left=True, pad_right=True, left_pad_symbol='<s>',
                                    right_pad_symbol='</s>')
        freq = nltk.FreqDist(bigrams)
        with open("{0}/bigrams_{1}.txt".format(output_folder, tag), "a") as writer:
            for entry in freq:
                writer.write(entry[0] + " " + entry[1] + " " + str(freq[entry]) + "\n")


generate_unigrams("data/train.txt")
generate_bigrams("data/train.txt")
