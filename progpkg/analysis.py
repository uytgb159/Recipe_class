#!/usr/bin/python
import re
import requests
from elasticsearch import Elasticsearch
from konlpy.tag import Kkma
from konlpy.utils import pprint
from elasticsearch import Elasticsearch
import math
from nltk import word_tokenize
es_host="http://localhost:9200"

def analysisTFIDF(recipe):
   #RECIPE TEXT를 받아오면 명사만 추출하기
   hfi_str=re.sub(u'[^ \.\,\?\!\u3130-\u318f\uac00-\ud7a3]+', '', recipe)
   kkma=Kkma()
   word_l=[]
   wlist=kkma.pos(hfi_str)
   for w in wlist:
      if w[1] =="NNG":
         word_l.append(w[0])
   print(word_l)
   
   #ElasticSearch에서 word list가져오기
   #김치볶음밥 재료
   control_words=['김치', '스팸', '밥', '굴소스', '올리고당', '고추장', '맛술', '참기름', '후춧가루', '팬', '중불', '비법양념장']
   
   #TFIDF 계산하기
   word_d={}
   sen_list=[]
   #SCORE높은 TOP10개 단어를 RETURN
    
if __name__=='__main__':
    #두부닭가슴살유부초밥 재료
    recipe='냉동 (or 훈제)닭가슴살을 삶아서 찢어준다 찢은 닭가슴살 작게 잘라준다(가위나 칼 사용) 유부에 들어가니깐 기호대로 크기는 알아서^^ 두부를 물에 데쳐서 건진 다음 자른 닭가슴살과 함께 버무린다 이때 소금이나 후추로 조금 간을 해요 버물버물/ 잘 두부랑 닭가슴살이 섞이도록 무쳐주세요 유부초밥 안에 있는 후레이크와 소스 넣아주세요 다시 버물려줍니다 잘 버물려지면 유부의 물기를 짜서 두부닭가슴살을 유부안에 담아줍니다 완성!'
    analysisTFIDF(recipe)
