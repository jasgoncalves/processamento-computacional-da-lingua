python3 -m pip install -q -r requirements.txt

echo "====> A gerar ficheiros de unigramas e bigramas sem pré-processamento do texto."
python3 task1.py

echo "====> Classificador sem pré-processamento com unigramas."
python3 classifier.py UNIGRAM counts test-questions.txt > result.txt
python3 evaluate.py -v data/test-labels.txt result.txt

echo "====> Classificador sem pré-processamento com bigramas."
python3 classifier.py BIGRAM counts test-questions.txt > result.txt
python3 evaluate.py -v data/test-labels.txt result.txt

echo "====> Classificador sem pré-processamento com bigramas com alisamento."
python3 classifier.py BIGRAM_SMOOTHING counts test-questions.txt > result.txt
python3 evaluate.py -v data/test-labels.txt result.txt

echo "====> A gerar ficheiros de unigramas e bigramas com pré-processamento do texto."
python3 task3.py

echo "====> Classificador com pré-processamento com unigramas."
python3 classifier.py UNIGRAM counts2 test-questions.txt > result.txt
python3 evaluate.py -v data/test-labels.txt result.txt

echo "====> Classificador com pré-processamento com bigramas."
python3 classifier.py BIGRAM counts2 test-questions.txt > result.txt
python3 evaluate.py -v data/test-labels.txt result.txt

echo "====> Classificador com pré-processamento com bigramas sem alisamento."
python3 classifier.py BIGRAM_SMOOTHING counts2 test-questions.txt > result.txt
python3 evaluate.py -v data/test-labels.txt result.txt



