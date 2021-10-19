import os.path

import requests
# Web
from bs4 import BeautifulSoup
# NLP
from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Mecab
from konlpy.tag import Okt
from konlpy.tag import Twitter
from pykospacing import Spacing

# from typing import Set

# if there aren't dir, make
if (os.path.isdir("./resource/test_word_all/")) != 1:
    os.makedirs("./resource/test_word_all/")

# 54~76 쪽까지
for page in range(0, 1):  # 23
    # 교과서 페이지가 저장된 txt 파일에서 본문 가져오기

    file_name = "./resource/test_resource/" + str(page + 1) + ".txt"
    file = open(file_name, 'r', encoding='utf-8')
    text = file.read()
    file.close()

    # 띄어쓰기 삭제
    text_1 = text.replace(" ", "")
    # print(text)

    # NLP 객체 생성
    mecab = Mecab()
    kkma = Kkma()
    okt = Okt()
    twitter = Twitter()
    komoran = Komoran()
    spacing = Spacing()

    # 자연어 처리된 결과를 리스트로 저장
    data_a = [
        # kkma.nouns(text),
        # kkma.nouns(text_1),
        mecab.nouns(text),
        mecab.nouns(text_1),

        okt.nouns(text),
        okt.nouns(text_1),
        twitter.nouns(text),
        twitter.nouns(text_1),
        # komoran.nouns(text),
        # komoran.nouns(text_1),
        spacing(text.replace('.', '')).split()
    ]

    # 여러개의 리스트를 하나의 리스트로 저장
    data = []
    for num in range(0, 7):
        print(data_a[num])
        data.extend(data_a[num])

    # 중복된 단어 삭제
    rm_overlap = set(data)
    data = list(rm_overlap)

    # 자료 올림차순 정리
    data.sort()

    # 단어를 저장할 txt 파일 열기
    list_file_name = "./resource/test_word_all/" + str(page + 1) + ".txt"
    list_file = open(list_file_name, 'a', encoding='utf-8')

    # 모든 단어에 대해 단어에 대해 실행
    for num in data:
        # 한 글자 단어 삭제
        if len(num) != 1:

            # 한국 표준어 대사전 웹크롤링
            url = 'https://stdict.korean.go.kr/search/searchResult.do?pageSize=10&searchKeyword=' + num
            response = requests.get(url)

            # 웹크롤링을 성공하면
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')

                # 단어의 뜻만 추출
                titles = soup.select('#searchDataVO > div > ul > li > dl > dt > span > font')

                # 뜻이 없는 단어 삭제
                if len(titles) != 0:
                    # 뜻을 한 줄로 저장
                    a = num
                    for title in titles:
                        a = a + "|" + title.text

                    print(a)

                    # txt 파일에 쓰기
                    list_file.write(a + "\n")

            else:
                print(response.status_code)

    # txt 파일 닫기
    list_file.close()
