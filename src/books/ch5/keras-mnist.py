from keras import Sequential
from keras.datasets import mnist
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import Adam
from keras.utils import np_utils

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 데이터를 float32 자료형으로 변환하고 정규화하기
x_train = x_train.reshape(60000, 784).astype('float32')
x_test = x_test.reshape(10000, 784).astype('float')
x_train /= 255
x_test /= 255

# 레이블 데이터를 0-9까지의 카테고리를 나타내는 배열로 변환하기
y_train = np_utils.to_categorical(y_train, 10)
y_test = np_utils.to_categorical(y_test, 10)

# 모델 구조 정의
model = Sequential()
model.add(Dense(512, input_shape=(784,)))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(10))
model.add(Activation('softmax'))

# 모델 구축
model.compile(
    loss='categorical_crossentropy',
    optimizer=Adam(),
    metrics=['accuracy']
)

# 데이터 훈련
hist = model.fit(x_train, y_train)

# 테스트 데이터로 평가
score = model.evaluate(x_test, y_test, verbose=1)
print('loss=', score[0])
print('accuracy=', score[1])
