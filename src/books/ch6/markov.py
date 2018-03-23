import codecs
import json
import os
import random
import urllib.request
import urllib.parse

from bs4 import BeautifulSoup
from konlpy.tag import Twitter


def make_dict(words):
    tmp = ['@']
    dic = {}
    for word in words:
        tmp.append(word)
        if len(tmp) < 3:
            continue
        if len(tmp) > 3:
            tmp = tmp[1:]
            set_word3(dic, tmp)
            if word == '.':
                tmp = ['@']
                continue
    return dic


def set_word3(dic, s3):
    w1, w2, w3 = s3
    if w1 not in dic:
        dic[w1] = {}
    if w2 not in dic[w1]:
        dic[w1][w2] = {}
    if w3 not in dic[w1][w2]:
        dic[w1][w2][w3] = 0
    dic[w1][w2][w3] += 1


# 문장 만들기
def make_sentence(dic):
    ret = []
    if '@' not in dic:
        return 'no dic'
    top = dic['@']
    w1 = word_choice(top)
    w2 = word_choice(top[w1])
    ret.append(w1)
    ret.append(w2)
    while True:
        w3 = word_choice(dic[w1][w2])
        ret.append(w3)
        if w3 == '.':
            break
        w1, w2 = w2, w3
    ret = ''.join(ret)
    # 띄어쓰기
    params = urllib.parse.urlencode({
        '_callback': '',
        'q': ret
    })
    # 네이버 맞춤법 검사기를 사용합니다.
    data = urllib.request.urlopen('https://m.search.naver.com/p/csearch/dcontent/spellchecker.nhn?' + params)
    data = data.read().decode('utf-8')[1:-2]
    data = json.loads(data)
    data = data['message']['result']['html']
    data = BeautifulSoup(data, 'html.parser').getText()
    return data


def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))


# 문장 읽어 들이기
toji_file = 'toji.txt'
dict_file = 'markov-toji.json'
if not os.path.exists(dict_file):
    # 토지 텍스트 파일 읽어 들이기
    # https://ithub.korean.go.kr/user/total/database/corpusView.do 에서 텍스트파일 다운로드
    fp = codecs.open('BEXX0003.txt', 'r', encoding='utf-8')
    soup = BeautifulSoup(fp, 'html.parser')
    body = soup.select_one('body > text')
    text = body.getText()
    text = text.replace('…', '')
    # 형태소 분석
    twitter = Twitter()
    ma_list = twitter.pos(text, norm=True)
    words = []
    for word in ma_list:
        # 구두점 등은 대상에서 제외
        if word[1] not in ['Punctuation']:
            words.append(word[0])
        if word[0] == '.':
            words.append(word[0])
    # 딕셔너리 생성
    gen_dict = make_dict(words)
    json.dump(gen_dict, open(dict_file, 'w', encoding='utf-8'))
else:
    gen_dict = json.load(open(dict_file, 'r'))

# 문장 만들기
for i in range(3):
    s = make_sentence(gen_dict)
    print(s)
    print('---')
