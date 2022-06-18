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
sent_list=[]
word_d={}

def process_new_sentence(s):
    sent_list.append(s)
    splited = s.split(' ')
    for word in splited:
        if word not in word_d.keys():
            word_d[word]=0
        word_d[word]+=1

def compute_tf(s):
    bow=set()
    wordcount_d={}
    
    splited = s.split(' ')
    for spl in splited:
        if spl not in wordcount_d.keys():
            wordcount_d[spl]=0
        wordcount_d[spl]+=1
        bow.add(spl)
    
    tf_d={}
    for word, cnt in wordcount_d.items():
        tf_d[word]=cnt/float(len(bow))
        
    return tf_d

def compute_idf():
    Dval = len(sent_list)
    bow=set()
    
    for ii in range(0, len(sent_list)):
        splited=sent_list[ii].split(' ')
        for sp in splited:
            bow.add(sp)
            
    idf_d={}
    for tt in bow:
        cnt=0
        for ss in sent_list:
            if tt in ss.split(' '):
                cnt+=1
        idf_d[tt]=math.log(Dval/float(cnt))
    return idf_d

def analysisTFIDF(recipe):
    #1. RECIPE TEXT를 받아오면 명사만 추출해서 str만들기
    hfi_str=re.sub(u'[^ \.\,\?\!\u3130-\u318f\uac00-\ud7a3]+', '', recipe)
    kkma=Kkma()
    sentence=''
    wlist=kkma.pos(hfi_str)
    for w in wlist:
        if w[1] =="NNG":
            sentence+=w[0]+' '
    #print(sentence)
    
    #2. ElasticSearch에서 word dict가져오기
    control_word_list=['마늘 장아찌 기 건강 마늘 오늘 장아찌 법 소개 마늘 상처 세척 키친 타올 물기 제거 용기 마늘 장아찌 법 밑반찬 마늘 장아찌 법 레 마늘 장아찌 만들기 마늘 장아찌 방법 마늘 장아찌 황금 레 시 피 차로 마늘 아린 맛 제거 차 마늘 물 물 양은 마늘 용기 양 체크 하심 물 물 식초 컵 소금 소금 약간 아린 맛 제거 찬물 식초 소금 물 주심 물 식초 정도 일주일 정도 곳 마늘 방지 검정비닐 빛 차단 비닐 주일 간 실온 보관 빛깔 일주일 마늘 절임 물 준비 일주일 마늘 절임 물 준비 차 물 절임 물 사용 마늘 성분 사용 사용 분 물 식초 물 비율 물 준비 마늘 일주일 물 설탕 컵 소주 컵 간장 컵 마늘 장아찌 법 밑반찬 마늘 장아찌 법 레 요기 완성 그다음 차 마늘 장아찌 만들기 절임 물 한소 뜸 후 마늘 용기 마늘 장아찌 법 밑반찬 마늘 장아찌 법 레 만들기 완성 멸치 줌 다시마 센티 정도 두장 양파 반개 대파 조각 무우 반 조각 우려 멸치 다시마 로만 무우 대파 양파 육수 맛 불 물 다시마 다음 분분 불로 국 간장 스푼 간 때 스푼 딱이 당근 호박 후라이팬 소금 간도 계란 개 약 불로 후라이 팬 흰자 지단 준비 취향 양념장 간장 스푼 고추 가루 스푼 고추 스푼 마늘 스푼 대파 스푼 매실 액 스푼 참기름 스푼 깨 스푼 양념장 사람 입맛 양념장 황금 레 부족 입맛 조절 물 국수 동전 양이 인분 분량 때 때 찬물 면 보통 국수 봉지 분 고 찬물 정도 삶 국수 찬물 우거 면발 깃 말 체 물기 면 제일 고명 다음 육수 완성 ', '소금 오이 당 등분 오이 아래쪽 정도 여유 십자 모양 물 소금 스푼 불 백주 부 오이 소박이 비법 소금물 사용 소금물 정도 물 오이 오이 동안 부추 양파 당근 부추 나중 양념 때 새끼 손가락 마디 정도 주세 멸치 액 젓 스푼 새우젓 스푼 고추 가루 스푼 마늘 스푼 설탕 스푼 양념장 손질 부추 양파 당근 부추 주의 하세 요절 여진 오이 체 물기 제거 뒤 양념장 오이 속 끝 초보 실패 백주 부 오이 소박이 완성 식 감 간도 입맛 때 밥 물 입맛 두부 한입 크기 국물 맛 맛 비엔나 사선 떡 국물 줌 김치 김치 맛 밸런스 중요 밥공기 된장 반 술 고추 가루 술 마늘 술 국 간장 술 설탕 반 술 물 소주 컵 반 컵 두부 햄 떡 테두리 김치 가운데 양념장 사골 곰탕 육수 봉지 물 보충 대파 청양 고추 홍 고추 청양 고추 대파 향 냄새 찌개 법 이대 성공 라면 나중 추가 후 바 라면 국물 여유 전 육수 물 보충 잔 요 정도 국물 맛 찌개 완성 ', '로그 서 핫 반응 닭볶음탕 파와 청양 고추 당근 감자 주세 양파 반 후 사각 고추장 술 고추 가루 술 설탕 술 국 간장 술 마늘 술 소주잔 물 컵 주세 간장 국 간장 닭 물 시작 정도 후 물 찬물 불순물 주세 닭 팬 소주 컵 닭 내 감자 중간 양념장 후 물 주세 계랑 컵 재료 끄트머리 정도 주세 요강 불 양념장 강 중 불 사이 국물 반 때 감자 닭 젓가락 확인 하세 화력 물 닭 감자 물 물 추가 국 물이 요 정도 상태 대파 고추 양파 국 물 조리 비 추구 국물 주세 대파 청양 고추 양파 후 분 후 불 국 물 요 정 도로 국물 밥 국 물 맛 집 식당 닭볶음탕 레 완성 양념장 황금 비율 비율 주세 터득 황금 비율 황금 팁 양념장 비율 야채 분 후 불 국물 국물 닭도리탕 백숙 닭고기 국물 스타일 국물 칼 칼 취향 주세 김치 볼 가위 이용 준비 방송 줄기 부분 줄기 부분 위주 부침 가루 컵 김치 국물 컵 정도 마늘 반 스푼 수미 반찬 포인트 마늘 마늘 감칠맛 물 컵 물 반죽 농도 반죽 물 추가 물 기름 팬 반죽 모양 앞뒤 접시 직 운 김치 전 만들기 완성 ', '오이 소금 가시 부분 제거 칼등 제거 두께 감 주고 양파 파 고추 준비 분량 양념장 채소 양념장 싹 오이 무침 완성 즉석 신선 맛깔 오이 무침 식사 닭 한마리 준비 집 가족 명 준비 대식 당면 물 닭 손질 닭 사이 사이 기름 제거 요잡 내 우유 정도 지금 부분 닭 닭 물 물 부분 제가 닭 우유 후 조리 경우 닭 우유 조리 경우 한번 육수 닭볶음탕 맛 닭 내 유 유 한번 방법 사실 ㅎ 무 취향 요고 냄비 닭 한마리 기준 간장 고추장 고춧가루 양파 마늘 알 요리 당 청주 후추 약간 액 젓 액 젓 감칠맛 단 분 간장 액 젓 추가 양념 소스 주세 요거 맛 집 맛 맛 집 낙지 새우 첨가 주기도 냄비 양념장 육수 물 육수 감칠맛 물 물 대체 가능 물 당면 때 때 사이 야채 손질 감자 모서리 감자 국물 질 수가 남 감자 된장찌개 때 감자 뚜껑 중 불 정도 주세 대파 양파 당근 고추 크기 준비 정도 닭 감자 나머지 야채 국 물 분 육수 추가 양념 추가 준비 당면 첨가 불 시간 주세 당면 상관 기름 후추 선택 가능 첨가 주심 끝 ']


    #3. TFIDF 계산하기
    for ee in range(0,4,1):
        process_new_sentence(control_word_list[ee])
    process_new_sentence(sentence)
    
    idf_d=compute_idf()

    tf_d=compute_tf(sentence)
    tf_idf_d={}
    for word, tfval in tf_d.items():
        tf_idf_d[word]=tfval*idf_d[word]
        #print(word, tfval*idf_d[word])
        
    tfidf_dict = dict(sorted(tf_idf_d.items(), key=lambda x: x[1], reverse=True))
    nn=0
    top10_d={}
    for key, val in tfidf_dict.items():
        top10_d[key]=val
        nn+=1
        if(nn==10):
            break
    print(top10_d)

    #4. SCORE높은 TOP10개 단어를 RETURN
    return top10_d
    
if __name__=='__main__':
    #두부닭가슴살유부초밥 재료
    recipe='냉동 (or 훈제)닭가슴살을 삶아서 찢어준다 찢은 닭가슴살 작게 잘라준다(가위나 칼 사용) 유부에 들어가니깐 기호대로 크기는 알아서^^ 두부를 물에 데쳐서 건진 다음 자른 닭가슴살과 함께 버무린다 이때 소금이나 후추로 조금 간을 해요 버물버물/ 잘 두부랑 닭가슴살이 섞이도록 무쳐주세요 유부초밥 안에 있는 후레이크와 소스 넣아주세요 다시 버물려줍니다 잘 버물려지면 유부의 물기를 짜서 두부닭가슴살을 유부안에 담아줍니다 완성!'
    analysisTFIDF(recipe)
    