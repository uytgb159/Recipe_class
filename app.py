#!/usr/bin/python

from flask import Flask, render_template, request
from progpkg import crawl, analysis, elastic

app = Flask(__name__)

@app.route('/') # 접속url
def home():
  return render_template('home.html', result1 = final_list[0], result2 = final_list[1], result3 = final_list[2], result4 = final_list[3])
  
@app.route('/search', methods = ["POST", "GET"]) #second page
def recipe():
  if request.method == "POST":
    addSource = request.form["include"]
    subList = list(request.form["exclude"].split())
    word_i = crawl.crawl(addSource, subList)
    tfidf = []
    for res in word_i:
      tfidf.append(analysis.analysisTFIDF(res['recipe']))
  return render_template('search.html', addSource = addSource, subList = subList, tfidf = tfidf, word_i = word_i)

if __name__=="__main__":
  app.run(debug=True)
