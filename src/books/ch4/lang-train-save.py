import json

from sklearn import svm
from sklearn.externals import joblib

with open('./lang/freq.json', 'r', encoding='utf-8') as fp:
    d = json.load(fp)
    data = d[0]

# 데이터 학습하기
clf = svm.SVC()
clf.fit(data['freq_list'], data['labels'])

# 학습 데이터 저장하기
joblib.dump(clf, './lang/freq.pkl')
print('ok')
