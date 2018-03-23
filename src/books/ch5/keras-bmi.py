import pandas as pd
import numpy as np
from keras import Sequential
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Activation, Dropout

csv = pd.read_csv('../ch4/bmi.csv')

# 데이터 정규화
csv['weight'] /= 100
csv['height'] /= 200
x = csv[['weight', 'height']].as_matrix()

# 레이블
b_class = {
    'thin': [1, 0, 0],
    'normal': [0, 1, 0],
    'fat': [0, 0, 1]
}
y = np.empty((20000, 3))
for i, v in enumerate(csv['label']):
    y[i] = b_class[v]

# 훈련 전용 데이터와 테스트 전용 데이터로 나누기
x_train, y_train = x[1:15001], y[1:15001]
x_test, y_test = x[15001:20001], y[15001:20001]

# 모델 구조 정의
model = Sequential()
model.add(Dense(512, input_shape=(2,)))
model.add(Activation('relu'))
model.add(Dropout(0.1))

model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.1))

model.add(Dense(3))
model.add(Activation('softmax'))

# 모델 구축하기
model.compile(
    loss='categorical_crossentropy',
    optimizer='rmsprop',
    metrics=['accuracy']
)

# 데이터 훈련하기
hist = model.fit(
    x_train, y_train,
    batch_size=50,
    epochs=20,
    validation_split=0.1,
    callbacks=[EarlyStopping(monitor='val_loss', patience=2)],
    verbose=1
)

# 테스트 데이터로 평가하기
score = model.evaluate(x_test, y_test)
print('loss =', score[0])
print('accuracy =', score[1])
