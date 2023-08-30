import chardet # 인코딩 방식 확인 라이브러리
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import networkx as nx

def extract_keywords(text, n_keywords=10):
    # 문장 토큰화
    sentences = sent_tokenize(text)

    # 단어 토큰화, 불용어 제거
    stop_words = set(stopwords.words('english'))
    words = [word_tokenize(sentence) for sentence in sentences]
    words = [[word.lower() for word in sentence if word.isalnum() and word.lower() not in stop_words] 
             for sentence in words]

    # 그래프 생성 및 TextRank 알고리즘 적용
    co_occurrence = {word: Counter() for sentence in words for word in sentence}
    for sentence in words:
        for i, word1 in enumerate(sentence):
            for j, word2 in enumerate(sentence):
                if i != j:
                    co_occurrence[word1][word2] += 1

    graph = nx.from_dict_of_lists(co_occurrence)
    scores = nx.pagerank(graph)

    # 가장 높은 Score를 갖는 상위 n_keywords 개의 단어 추출
    keywords = sorted(scores, key=scores.get, reverse=True)[:n_keywords]

    return keywords
'''
위 코드에서 extract_keywords() 함수는 입력된 text 문자열에서 TextRank 알고리즘을 사용하여 상위 n_keywords개의 키워드를 추출합니다.
해당 함수는 알고리즘 단계별로 다음과 같이 동작합니다.

문장 토큰화

단어 토큰화, 불용어 제거

단어들의 공기 빈도수를 계산하여 그래프 생성

TextRank 알고리즘을 적용하여 각 단어의 Score 계산

가장 높은 Score 값을 갖는 상위 n_keywords 개의 단어 추출

extract_keywords 에서는 먼저 입력된 text 문자열을 nltk 라이브러리의 sent_tokenize() 함수를 사용하여 문장 토큰화한 후,
word_tokenize() 함수를 사용하여 단어 토큰화를 수행하고, stopwords를 사용하여 불용어를 제거합니다.
그 다음 단어들의 공기 빈도수를 계산하여 그래프를 생성하고, networkx 라이브러리의 pagerank() 함수를 사용하여 각 단어의 Score 값을 계산합니다.
마지막으로 각 단어의 Score 값에 따라 내림차순으로 정렬하여 상위 n_keywords개의 단어를 추출하여 반환합니다.
위 코드를 실행하면, 입력된 예시 문자열에서 가장 높은 Score 값을 갖는 상위 10개의 단어가 추출되어 keywords 변수에 저장되고 출력됩니다.
'''

def read_file(text_Route): # 경로를 인자로 받으면 파이썬을 읽어주는 함수
    encoding_method = check_Encoding(text_Route)
    f = open(f"{text_Route}", "r", encoding = encoding_method)
    text = f.read()
    text = using_regex(text) # 텍스트 전처리
    with open("wine_text_result.txt", "w", encoding="utf-8") as file:
        file.write(text)
    return text

def check_Encoding(text_Route): # 텍스트 경로를 인자로 받으면 어떤 방식의 인코딩을 사용했는지 반환해주는 함수
    with open(text_Route, 'rb') as f:
        result = chardet.detect(f.read())
        print(f"입력되는 텍스트는 {result['confidence']}의 확률로 {result['encoding']}방식의 인코딩을 사용하였습니다" )
    return result['encoding']

def using_regex(text): # 파싱이 깨진 문자, 및 잘못 끊긴 문장 등을 정리하는 코드
    origin_text = ["Ch창teau","�셲","��","�쁶","�쁁","Sim훾i훾","Gori큄ka","precedent","�쁆ros","R챕zeau","premi챔re","횋","�쁋ivre","�섲","�셎","챔","척","횊","챕","�쁣","처","�쁥","챠","첬","체","휓","찼","횆","챰","횕"]
    fix_text = ["Château","'s","--","-w","-B","Simčič","Goriška","précédent","Eros","Rézeau","première","E","Livre","d'A","'S","è","ô","E","é","-f","o","-h","i","ú","ü","ğ","á","Ä","n","ï"]
    for i in range(len(origin_text)):
        text = re.sub(rf'{origin_text[i]}', fix_text[i] , text, flags=re.IGNORECASE)
    text = re.sub(r'(?<!\n)\n{2,}(?!\n)', ' ', text)
    text = re.sub(r'((?<=[a-z0-9])[.?!](?=\s*\n*(?![a-z0-9])))', r'\1\n', text)
    text = re.sub(r'((?<=\d)\s|(?<=\()\w\.\s)', '', text)
    return text.strip()



    