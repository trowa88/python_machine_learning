import glob
import json
import os
import re

from sklearn import svm, metrics


def check_freq(f_name):
    name = os.path.basename(f_name)
    lang = re.match(r'^[a-z]{2,}', name).group()

    with open(f_name, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.lower()

    # 숫자 세기 변수(cnt) 초기화하기
    cnt = [0 for _ in range(0, 26)]
    code_a = ord('a')
    code_z = ord('z')

    # 알파벳 출현 횟수 구하기
    for ch in text:
        n = ord(ch)
        if code_a <= n <= code_z:
            cnt[n - code_a] += 1

    # 정규화하기
    total = sum(cnt)
    freq = list(map(lambda x: x / total, cnt))
    return freq, lang


# 각 파일 처리하기
def load_files(path):
    freq_list = []
    labels = []
    file_list = glob.glob(path)
    for f_name in file_list:
        r = check_freq(f_name)
        freq_list.append(r[0])
        labels.append(r[1])
    return {'freq_list': freq_list, 'labels': labels}


data = load_files('./lang/train/*.txt')
test = load_files('./lang/test/*.txt')

# 이후를 대비해서 JSON 으로 결과 저장하기
with open('./lang/freq.json', 'w', encoding='utf-8') as fp:
    json.dump([data, test], fp)

# 학습하기
clf = svm.SVC()
clf.fit(data['freq_list'], data['labels'])

# 예측하기
predict = clf.predict(test['freq_list'])

# 결과 테스트하기
ac_score = metrics.accuracy_score(test['labels'], predict)
cl_report = metrics.classification_report(test['labels'], predict)
print('정답률=', ac_score)
print('리포트 = ')
print(cl_report)
