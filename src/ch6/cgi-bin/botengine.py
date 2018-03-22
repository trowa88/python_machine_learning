import json
import os
import random
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup
from konlpy.tag import Twitter

dict_file = 'chatbot-data.json'
dic = {}
twitter = Twitter()


# 딕셔너리에 단어 등록
def register_dic(words):
    global dic
    if len(words) == 0:
        return
    tmp = ['@']
    for i in words:
        word = i[0]
        if word == '' or word == '\r\n' or word == '\n':
            continue
        tmp.append(word)
        if len(tmp) < 3:
            continue
        if len(tmp) > 3:
            tmp = tmp[1:]
        set_word(dic, tmp)
        if word == '.' or word == '?':
            tmp = ['@']
            continue
    # 딕셔너리가 변경될 때마다 저장하기
    json.dump(dic, open(dict_file, 'w', encoding='utf-8'))


# 딕셔너리에 글 등록하기
def set_word(word_dic, s3):
    w1, w2, w3 = s3
    if w1 not in word_dic:
        word_dic[w1] = {}
    if w2 not in word_dic[w1]:
        word_dic[w1][w2] = {}
    if w3 not in word_dic[w1][w2]:
        word_dic[w1][w2][w3] = 0
    word_dic[w1][w2][w3] += 1


# 문장 만들기
def make_sentence(head):
    if head not in dic:
        return ''
    ret = []
    if head != '@':
        ret.append(head)
    top = dic[head]
    w1 = word_choice(top)
    w2 = word_choice(top[w1])
    ret.append(w1)
    ret.append(w2)
    while True:
        if w1 in dic and w2 in dic[w1]:
            w3 = word_choice(dic[w1][w2])
        else:
            w3 = ''
        ret.append(w3)
        if w3 == '.' or w3 == ' ? ' or w3 == '':
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


# 챗봇 응답 만들기
def make_reply(text):
    # 단어 학습시키기
    if text[-1] not in ['.', '?']:
        text += '.'
    words = twitter.pos(text)
    register_dic(words)
    # 사전에 단어가 있다면 그것을 기반으로 문장 만들기
    for word in words:
        face = word[0]
        if face in dic:
            return make_sentence(face)
    return make_sentence('@')


# 딕셔너리가 있다면 읽어 들이기
if os.path.exists(dict_file):
    dic = json.load(open(dict_file, 'r'))
