#!/usr/bin/env python3

import cgi
import html
import os

from sklearn.externals import joblib

pkl_file = os.path.dirname(__file__) + '/freq.pkl'
clf = joblib.load(pkl_file)


# 텍스트 입력 양식 출력하기
def show_form(s_text, s_msg=''):
    print('Content-Type: text/html; charset=utf-8')
    print()
    print('''
        <html>
        <body>
        <form>
          <textarea name="text" cols="40" rows="8">{0}</textarea>
          <p><input type="submit" value="판정" /></p>
          <p>{1}</p>
        </form>
        </body>
        </html>
    '''.format(html.escape(s_text), s_msg))


# 판정하기
def detect_lang(d_text):
    # 알파벳 출현 빈도 구하기
    d_text = d_text.lower()
    code_a, code_z = (ord('a'), ord('z'))
    cnt = [0 for _ in range(26)]
    for ch in d_text:
        n = ord(ch) - code_a
        if 0 <= n <= 26:
            cnt[n] += 1

    total = sum(cnt)
    if total == 0:
        return '입력이 없습니다'
    freq = list(map(lambda x: x/total, cnt))

    # 언어 예측하기
    res = clf.predict([freq])

    # 언어 코드를 한국어로 변환하기
    lang_dic = {
        'en': '영어',
        'fr': '프랑스어',
        'id': '인도네시아어',
        'tl': '타갈로그어'
    }
    return lang_dic[res[0]]


# 입력 양식의 값 읽어 들이기
form = cgi.FieldStorage()
text = form.getvalue('text', default='')
msg = ''
if text:
    lang = detect_lang(text)
    msg = '판정 결과: ' + lang
show_form(text, msg)
