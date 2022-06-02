#!/usr/bin/python
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from konlpy.tag import Kkma
from konlpy.utils import pprint
from elasticsearch import Elasticsearch
es_host="http://localhost:9200"

def analysis(word_l):
   print(word_l) 
    
if __name__=='__main__':
    #김치볶음밥 재료
    words=['김치', '스팸', '밥', '굴소스', '올리고당', '고추장', '맛술', '참기름', '후춧가루', '팬', '중불', '비법양념장']
    analysis(words)
