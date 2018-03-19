from sklearn import svm, metrics


def load_csv(f_name):
    labels = []
    images = []

    with open(f_name, 'r') as f:
        for line in f:
            cols = line.split(',')
            if len(cols) < 2:
                continue
            labels.append(int(cols.pop(0)))
            vals = list(map(lambda n: int(n) / 256, cols))
            images.append(vals)
    return {
        'labels': labels,
        'images': images
    }


data = load_csv('./mnist/train.csv')
test = load_csv('./mnist/t10k.csv')

# 학습하기
clf = svm.SVC()
clf.fit(data['images'], data['labels'])

# 예측하기
predict = clf.predict(test['images'])

# 결과 확인하기
ac_score = metrics.accuracy_score(test['labels'], predict)
cl_report = metrics.classification_report(test['labels'], predict)
print('정답률 =', ac_score)
print('리포트 =')
print(cl_report)
