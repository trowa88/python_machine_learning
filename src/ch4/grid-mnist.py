import pandas as pd
from sklearn import svm, metrics
from sklearn.model_selection import GridSearchCV

train_csv = pd.read_csv('./mnist/train.csv')
test_csv = pd.read_csv('./mnist/t10k.csv')

# 필요한 열 추출하기
train_label = train_csv.ix[:, 0]
train_data = train_csv.ix[:, 1:577]
test_label = test_csv.ix[:, 0]
test_data = test_csv.ix[:, 1:577]
print('학습 데이터의 수 =', len(train_label))

# 그리드 서치 매개변수 설정
params = [
    {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
    {'C': [1, 10, 100, 1000], 'kernel': ['rbf'], 'gamma': [0.001, 0.0001]}
]

# 그리드 서치 수행
clf = GridSearchCV(svm.SVC(), params, n_jobs=-1)
clf.fit(train_data, train_label)
print('학습기 =', clf.best_estimator_)

# 테스트 데이터 확인하기
pre = clf.predict(test_data)
ac_score = metrics.accuracy_score(test_label, pre)
print('정답률 =', ac_score)
