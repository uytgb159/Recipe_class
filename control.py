#!/usr/bin/python
#랭킹 홈페이지 URL: https://www.10000recipe.com/ranking/home_new.html
#하이퍼링크 : https://www.10000recipe.com + href(/recipe/숫자)

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

rank_url='https://www.10000recipe.com/ranking/home_new.html'
href_url='https://www.10000recipe.com'
res=requests.get(rank_url)
soup = BeautifulSoup(res.content, "html.parser")
for href in soup.find(class_='common_sp_list_ul').find_all('li'):
    print(href.find('a')['href'])