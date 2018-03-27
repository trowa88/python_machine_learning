import tensorflow as tf
import numpy as np

# 03train.txt
# #x0 x1 x2 y
# 1   1   0   1
# 1   0   2   2
# 1   3   0   3
# 1   0   4   4
# 1   5   0   5

xy = np.loadtxt('03train.txt', unpack=True, dtype='float32')
x_data = xy[:-1]
y_data = xy[-1]

print(type(xy))
print(xy.shape)
print(len(x_data))

W = tf.Variable(tf.random_uniform([1, len(x_data)], -1, 1))

# feature 갯수만큼 곱하는 이 부분을 제외하면 one-variable 과 다른 곳이 없다.
hypothesis = tf.matmul(W, x_data)

cost = tf.reduce_mean(tf.square(hypothesis - y_data))
rate = tf.Variable(0.1)
optimizer = tf.train.GradientDescentOptimizer(rate)
train = optimizer.minimize(cost)

init = tf.global_variables_initializer()

sess = tf.Session()
sess.run(init)

for step in range(2001):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(cost), sess.run(W))

sess.close()
