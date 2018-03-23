import json

import numpy as np
from keras import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split

max_words = 56681
nb_classes = 6
batch_size = 64
epochs = 20


# MLP 모델 생성
def build_model():
    model = Sequential()
    model.add(Dense(512, input_shape=(max_words,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model


# 데이터 읽어 들이기
data = json.load(open('./newstext/data-mini.json'))
# data = json.load(open('./newstext/data.json'))
X = data['X']  # 텍스트를 나타내는 데이터
Y = data['Y']  # 카테고리 데이터

# 학습하기
X_train, X_text, Y_train, Y_test = train_test_split(X, Y)
Y_train = np_utils.to_categorical(Y_train, nb_classes)
print(len(X_train), len(Y_train))
model = KerasClassifier(
    build_fn=build_model,
    epochs=epochs,
    batch_size=batch_size
)
model.fit(np.array(X_train), np.array(Y_train))

# 예측하기
y = model.predict(np.array(X_text))
ac_score = metrics.accuracy_score(Y_test, y)
cl_report = metrics.classification_report(Y_test, y)
print('정답률 =', ac_score)
print('리포트 =\n', cl_report)
