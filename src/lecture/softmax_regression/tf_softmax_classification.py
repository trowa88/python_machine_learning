import tensorflow as tf
import numpy as np

# softmax 이기 때문에 y를 표현할 때, 벡터로 표현한다.

# 05train.txt
# #x0 x1 x2 y[A   B   C]
# 1   2   1   0   0   1     # C
# 1   3   2   0   0   1
# 1   3   4   0   0   1
# 1   5   5   0   1   0     # B
# 1   7   5   0   1   0
# 1   2   5   0   1   0
# 1   6   6   1   0   0     # A
# 1   7   7   1   0   0

xy = np.loadtxt('05train.txt', unpack=True, dtype='float32')

# xy는 6x8. xy[:3]은 3x8. 행렬 곱셈을 하기 위해 미리 transpose.
x_data = np.transpose(xy[:3])
y_data = np.transpose(xy[3:])

print('x_data : ', x_data.shape)  # x_data : (8, 3)
print('y_data : ', y_data.shape)  # y_data: (8, 3)

X = tf.placeholder('float', [None, 3])  # x_data 와 같은 크기의 열 가짐. 행 크기는 모름.
Y = tf.placeholder('float', [None, 3])  # tf.float32 라고 써도 됨

W = tf.Variable(tf.zeros([3, 3]))  # 3x3 행렬. 전체 0.

# softmax 알고리즘 적용. X*W = (8x3) * (3x3) = (8x3)
hypothesis = tf.nn.softmax(tf.matmul(X, W))

# cross-entropy cost 함수
cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(hypothesis), reduction_indices=1))

learning_rate = 0.01
train = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    for step in range(2001):
        sess.run(train, feed_dict={X: x_data, Y: y_data})
        if step % 200 == 0:
            feed = {X: x_data, Y: y_data}
            print('{:4} {:8.6}'.format(step, sess.run(cost, feed_dict=feed)), *sess.run(W))
    print('---------------------------------------')

    # 1은 bias 로 항상 1. (11, 7)은 x 입력
    a = sess.run(hypothesis, feed_dict={X: [[1, 11, 7]]})
    print('a : ', a, sess.run(tf.argmax(a, 1)))

    b = sess.run(hypothesis, feed_dict={X: [[1, 3, 4]]})
    print('b : ', b, sess.run(tf.argmax(b, 1)))

    c = sess.run(hypothesis, feed_dict={X: [[1, 1, 0]]})
    print('c : ', c, sess.run(tf.argmax(c, 1)))

    # 한번에 여러 개 판단 가능
    d = sess.run(hypothesis, feed_dict={X: [[1, 11, 7], [1, 3, 4], [1, 1, 0]]})
    print('d : ', *d, end=' ')
    print(sess.run(tf.argmax(d, 1)))
