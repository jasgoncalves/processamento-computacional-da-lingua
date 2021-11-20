# python3 -m pip install -r requirements.txt

python3 classifier.py UNIGRAM counts2 eval-questions.txt > result.txt
python3 evaluate.py -v data/eval-labels.txt result.txt

python3 classifier.py BIGRAM counts2 eval-questions.txt > result.txt
python3 evaluate.py -v data/eval-labels.txt result.txt

python3 classifier.py BIGRAM_SMOOTHING counts2 eval-questions.txt > result.txt
python3 evaluate.py -v data/eval-labels.txt result.txt


# python3 classifier.py UNIGRAM counts eval-questions.txt > result.txt
# python3 evaluate.py -v data/eval-labels.txt result.txt

# python3 classifier.py BIGRAM counts eval-questions.txt > result.txt
# python3 evaluate.py -v data/eval-labels.txt result.txt

# python3 classifier.py BIGRAM_SMOOTHING counts eval-questions.txt > result.txt
# python3 evaluate.py -v data/eval-labels.txt result.txt
