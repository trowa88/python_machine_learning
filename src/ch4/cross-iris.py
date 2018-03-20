import random
import re

from sklearn import svm, metrics


def f_num(n):
    if re.match(r'^[0-9.]+$', n):
        return float(n)
    return n


def f_cols(li):
    return list(map(f_num, li.strip().split(',')))


# 붓꽃의 CSV 파일 읽어 들이기
lines = open('iris.csv', 'r', encoding='utf-8').read().split('\n')
csv = list(map(f_cols, lines))
del csv[0]  # 헤더 제거하기
random.shuffle(csv)  # 데이터 섞기

# 데이터를 K 개로 분할하기
K = 5
csv_k = [[] for _ in range(K)]
for i in range(len(csv)):
    csv_k[i % K].append(csv[i])


# 리스트를 훈련 전용 데이터와 테스트 전용 데이터로 분할하는 함수
def split_data_label(rows):
    data = []
    label = []
    for row in rows:
        data.append(row[0:4])
        label.append(row[4])
    return data, label


# 정답률 구하기
def calc_score(test, train):
    test_f, test_l = split_data_label(test)
    train_f, train_l = split_data_label(train)

    # 학습시키고 정답률 구하기
    clf = svm.SVC()
    clf.fit(train_f, train_l)
    pre = clf.predict(test_f)
    return metrics.accuracy_score(test_l, pre)


# K 개로 분할해서 정답률 구하기
score_list = []
for test_c in csv_k:
    # test_c 이외의 데이터를 훈련 전용 데이터로 사용하기
    train_c = []
    for i in csv_k:
        if i != test_c:
            train_c += i
    sc = calc_score(test_c, train_c)
    score_list.append(sc)

print('각각의 정답률 =', score_list)
print('평균 정답률 =', sum(score_list) / len(score_list))
