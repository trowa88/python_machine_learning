import tensorflow as tf
from matplotlib import pyplot as plt

X = [1., 2., 3.]
Y = [1., 2., 3.]
m = len(X)

W = tf.placeholder(tf.float32)

hypothesis = tf.multiply(W, X)
cost = tf.reduce_sum(tf.pow(hypothesis-Y, 2)) / m

init = tf.global_variables_initializer()

sess = tf.Session()
sess.run(init)

# 그래프로 표시하기 위해 데이터를 누적할 리스트
W_val, cost_val = [], []

for i in range(-30, 51):
    x_pos = i * 0.1
    y_pos = sess.run(cost, feed_dict={W: x_pos})
    print('{:3.1f}, {:3.1f}'.format(x_pos, y_pos))

    # 그래프에 표시할 데이터 누적.
    W_val.append(x_pos)
    cost_val.append(y_pos)

sess.close()

plt.plot(W_val, cost_val, 'ro')
plt.ylabel('Cost')
plt.xlabel('W')
plt.show()
