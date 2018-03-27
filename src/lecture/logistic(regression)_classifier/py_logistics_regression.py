import math
import numpy as np
import matplotlib.pyplot as plt


# z 는 값(scalar)일 수도 있고, vector 또는 matrix 일 수도 있다.
def sigmoid(z):
    return 1 / (1 + math.e ** -z)


def cost_function(w, x, y):
    m_ = y.size  # 100

    # 최초 실행시 값 : [[0.5] [0.5] [0.5] ... [0.5]]
    h = sigmoid(np.dot(w, x))

    # 값 1개. 곱셈(*)은 element-wise 곱셈
    cost_ = -(1/m_) * sum(y * np.log(h) + (1-y) * np.log(1-h))

    # (h-y)는 1행 m열
    grad_ = (1/m_) * np.dot(x, h-y)

    return cost_, grad_


xy = np.loadtxt('ex2data1.txt', unpack=True, dtype='float32', delimiter=',')
print(xy.shape)
print(xy[:, :5])

x_data = xy[:-1]
y_data = xy[-1]

# y_data 가 1 또는 0인 값의 인덱스 배열 생성
pos = np.where(y_data == 1)
neg = np.where(y_data == 0)

# 옥타브와 비슷한 형태로 그래프 출력
# x_data[0, pos]에서 0은 행, pos 는 열을 가리킨다. 쉼표 양쪽에 범위 또는 인덱스 배열 지정 가능.
t1 = plt.plot(x_data[0, pos], x_data[1, pos], color='black', marker='+', markersize=7)
t2 = plt.plot(x_data[0, neg], x_data[1, neg], markerfacecolor='yellow', marker='o', markersize=7)

plt.xlabel('exam 1 score')
plt.ylabel('exam 2 score')
plt.legend([t1[0], t2[0], ['Admitted', 'Not admitted']])
# decision boundary 직선.
# 안에 들어있는 값은 gradient descent 알고리즘을 구현한 이후에 발생한 값
# x값은 x_data 에서의 최소값과 최대값. y값은 W값을 이용해서 계산된 값.
plt.plot([28.059, 101.828], [96.166, 20.653], 'b')
plt.show()

n, m = x_data.shape
print('m, n : ', m, n)

# 1로 구성된 배열을 맨 앞에 추가
x_data = np.vstack((np.ones(m), x_data))
print(x_data.shape)
print(x_data[:, :5])

W = np.zeros(n+1)

cost, grad = cost_function(W, x_data, y_data)
print('---------------------------------')
print('cost: ', cost)
print('grad: ', *grad)
