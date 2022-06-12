#!/usr/bin/python

#text analysis를 위해 기본단어들이 저장되어 있고, 사용자가 text(음식재료)를 입력하면, 
#검색 횟수를 증가시키거나 새로운 재료명을 데이타베이스에 추가시킨 후 home.html로 누적검색량이 높은 검색어 n개를 보낸다.



#1. 기본단어들을 저장해 놓아(원래는 초기 엘라스틱에 정보를 저장해놓는 코드, 데이터가 갱신될때마다 저장해두는 엘라스틱 코드 이렇게 두개 만들어야 되는데)
# 어차피 시현할때는 기본 데이터에서 입력에 따라 바뀌는 것만 보여주면 되니까 일단은 random_list에 단어저장하고, 이 코드 실행될때마다 random_list 최기화되도록 했다.
#2. 사용자가 text를 입력
#3. 기존에 있는 단어면 검색횟수를 증가시키거나, 새로운 재료명을 추가시켜
#4. home.html에 누적검색량이 높은 검색어 4개를 보내
#5. 위 작업들이 실시간으로 이루어지게 한다

import sys
from elasticsearch import Elasticsearch
#pip install elasticsearch
from flask import Flask, render_template, request

es_host="http://localhost:9200"

if __name__=='__main__':
    es = Elasticsearch(es_host)
    #근데 단어 받아서 elastic 갱신한다음 random_list역시 갱신하는거는 어떻게 구현할까
    
    random_list = ['감자', '감자', '감자', '고구마', '고구마', '도마', '벡종원', '백종원', '백종원', '요거트', '요거트', '계란', '계란', '계란', '김치', '간편음식','간편음식','간편음식', '새우', '토마토', '마라'] #랜덤 단어 저장
    #현재 세번씩 저장 되어있는 감자, 백종원, 계란, 간편음식, 두번씩 저장되어있는 고구마, 요거트, 이렇게 총 6개의 단어가 보일 것이다.
    #사용자 input을 변수 w로 받아
    w = request.form["keyword"]
    if w not in random_list:
        random_list[w] = 0
    random_list[w] += 1
    
    final_list = []
    final_list = dict(sorted(random_list.items(), key=lambda x:x[1], reverse=True))
    #print(final_list[:4])
    
    #elasticsearch에 저장
    word=list(final_list.keys())
    cnt=list(final_list.values())
    elastic = {"words": word, "count": cnt}
    res=es.index(index='keyword', id=1, document=elastic) #아직 이 코드 이해 잘 못했어
    #res = es.search()
    res=es.search(index='keyword', body={"query": {"match_all":{}}})
    #print(res)
    
    #home.html로 전달
    def home():
        return render_template("home.html", result1 = final_list[0], result2 = final_list[1], result3 = final_list[2], result4 = final_list[3])
    
