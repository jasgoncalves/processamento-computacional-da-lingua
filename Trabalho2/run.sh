python3 -m pip install -r requirements.txt

python3 classifier.py UNIGRAM counts2 test-questions.txt > result.txt
python3 evaluate.py -v data/test-labels.txt result.txt

python3 classifier.py BIGRAM counts2 test-questions.txt > result.txt
python3 evaluate.py -v data/test-labels.txt result.txt

python3 classifier.py BIGRAM_SMOOTHING counts2 test-questions.txt > result.txt
python3 evaluate.py -v data/test-labels.txt result.txt


python3 classifier.py UNIGRAM counts test-questions.txt > result.txt
python3 evaluate.py -v data/test-labels.txt result.txt

python3 classifier.py BIGRAM counts test-questions.txt > result.txt
python3 evaluate.py -v data/test-labels.txt result.txt

python3 classifier.py BIGRAM_SMOOTHING counts test-questions.txt > result.txt
python3 evaluate.py -v data/test-labels.txt result.txt
