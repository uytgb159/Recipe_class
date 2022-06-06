#!/usr/bin/python
#TF-IDF를 계산하기 위한 대조군 TEXT를 만들고 DB에 집어넣는다. 만개의 레시피 - 랭킹 페이지에 있는 요리들의 조리순서에 있는 명사들을 추출해 LIST를 만들고 조리도구들을 추가로 LIST에 10번 집어넣는다.
#랭킹 홈페이지 URL: https://www.10000recipe.com/ranking/home_new.html
#하이퍼링크 : https://www.10000recipe.com + href(/recipe/숫자)

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from konlpy.tag import Kkma
from konlpy.utils import pprint
from elasticsearch import Elasticsearch

def hfilter(s):
    return re.sub(u'[^ \.\,\?\!\u3130-\u318f\uac00-\ud7a3]+', '', s)

es_host="http://localhost:9200"
#instru_l=['도마', '칼', '채칼', '필러', '가위', '강판', '다지기', '절구', '주걱', '스푼', '국자', '뒤집개', '누르개', '집게', '거품기', '스패츌러', '브러쉬', '믹싱볼', '바구니', '계량컵', '채망', '채반', '거름망']

#1. 만개의 레시피 랭킹 창에 있는 요리들의 하이퍼링크 주소 크롤링
rank_url='https://www.10000recipe.com/ranking/home_new.html'
href_url='https://www.10000recipe.com'
res=requests.get(rank_url)
soup = BeautifulSoup(res.content, "html.parser")

html_l=soup.find(class_='common_sp_list_ul').find_all('li')

#2. 각 요리별로 조리방법의 text를 크롤링(25개 씩 4개 set으로 분리)
cnt=0
sen_list=['', '', '', '']
for href in html_l:
    address=href_url+href.find('a')['href']
    res = requests.get(address)
    soup = BeautifulSoup(res.content, "html.parser")
    tb = soup.find(class_='view_step')
    tb_l=tb.find_all(class_='media-body')
    for sen in tb_l:
        sen_list[cnt//25]+=sen.text.strip('\n')
    cnt+=1
    print(cnt,"/100")
#print(sen_list)

hfil_strl=[]
for ii in range(0,4,1):
    hfil_strl.append(hfilter(sen_list[ii]))

#print(hfil_strl)


#3. 형태소 분석: 명사만 뽑아내기
kkma=Kkma()
word_l=[]
sentence=''
print('morphological analysing...')
for ii in range(0,4,1):
    wlist=kkma.pos(hfil_strl[ii])
    for w in wlist:
        if w[1] =="NNG":
            sentence+=w[0]+' '
    word_l.append(sentence)
    sentence=''
#print(word_l)

#4. ElasticSearch에 word list 집어넣기
print('putting word list in ElasticSearch')
es=Elasticsearch(es_host)
e={"control_word":'control',
    "word_list":word_l}
res=es.index(index='control_words2', id=1, document=e)
print("FINISH")