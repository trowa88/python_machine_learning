import tensorflow as tf
import numpy as np

# 04train.txt
# #x0 x1 x2 y
# 1   2   1   0
# 1   3   2   0
# 1   3   5   0
# 1   5   5   1
# 1   7   5   1
# 1   2   5   1

xy = np.loadtxt('04train.txt', unpack=True, dtype='float32')

# print(xy[0], xy[-1])  # [1. 1. 1. 1. 1. 1.] [0. 0. 0. 1. 1. 1.]

x_data = xy[:-1]
y_data = xy[-1]

X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)

# feature 별 가중치를 난수로 초기화. feature 는 bias 포함해서 3개. 1행 3열.
W = tf.Variable(tf.random_uniform([1, len(x_data)], -1.0, 1.0))

# 행렬 곱셈. (1x3) * (3x6)
h = tf.matmul(W, X)
hypothesis = tf.div(1., 1. + tf.exp(-h))  # exp(-h) = e ** -h. e 는 자연 상수

cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) * tf.log(1 - hypothesis))
rate = tf.Variable(0.1)
optimizer = tf.train.GradientDescentOptimizer(rate)
train = optimizer.minimize(cost)

init = tf.global_variables_initializer()

sess = tf.Session()
sess.run(init)

for step in range(2001):
    sess.run(train, feed_dict={X: x_data, Y: y_data})
    if step % 20 == 0:
        print(step, sess.run(cost, feed_dict={X: x_data, Y: y_data}), sess.run(W))

print('-----------------------------------------------')

# 결과가 0 또는 1로 계산되는 것이 아니라 0과 1 사이의 값으로 나오기 때문에 True/False 는 직접 판단
print('[1, 2, 2] : ', sess.run(hypothesis, feed_dict={X: [[1], [2], [2]]}) > 0.5)
print('[1, 5, 5] : ', sess.run(hypothesis, feed_dict={X: [[1], [5], [5]]}) > 0.5)
print('[1, 4, 2] [1, 0, 10] : ', end=' ')
print(sess.run(hypothesis, feed_dict={X: [[1, 1], [4, 0], [2, 10]]}) > 0.5)

# exp() 에는 실수만 전달
print(tf.exp([1., 2., 3.]).eval(session=sess))  # [ 2.7182817  7.389056  20.085537 ]
print(tf.exp([-1., -2., -3.]).eval(session=sess))  # [0.36787945 0.13533528 0.04978707]

sess.close()
