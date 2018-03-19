import os

from sklearn.externals import joblib

pkl_file = os.path.dirname(__file__) + '/freq.pkl'
clf = joblib.load(pkl_file)


# 텍스트 입력 양식 출력하기
def show_form(text, msg=''):
    pass
