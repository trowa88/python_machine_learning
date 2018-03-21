import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# MNIST 손글씨 이미지 데이터 읽어 들이기
mnist = input_data.read_data_sets('mnist/', one_hot=True)

pixels = 28 * 28
nums = 10

# 플레이스 홀더 정의
x = tf.placeholder(tf.float32, shape=(None, pixels), name='x')  # 이미지 데이터
y_ = tf.placeholder(tf.float32, shape=(None, nums), name='y_')  # 정답 레이블


# 가중치와 바이어스를 초기화하는 함수
def weight_variable(name, shape):
    w_init = tf.truncated_normal(shape, stddev=0.1)
    w = tf.Variable(w_init, name='w_' + name)
    return w


def bias_variable(b_name, b_size):
    b_init = tf.constant(0.1, shape=[b_size])
    b = tf.Variable(b_init, name='b_' + b_name)
    return b


# 합성곱 계층을 만드는 함수
def conv2d(con_x, con_w):
    return tf.nn.conv2d(con_x, con_w, strides=[1, 1, 1, 1], padding='SAME')


# 최대 풀링층을 만드는 함수
def max_pool(max_x):
    return tf.nn.max_pool(max_x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


# 합성곱층1
with tf.name_scope('conv1') as conv1:
    w_conv1 = weight_variable('conv1', [5, 5, 1, 32])
    b_conv1 = bias_variable('conv1', 32)
    x_image = tf.reshape(x, [-1, 28, 28, 1])
    h_conv1 = tf.nn.relu(conv2d(x_image, w_conv1) + b_conv1)

# 풀링층1
with tf.name_scope('pool1') as pool1:
    h_pool1 = max_pool(h_conv1)

# 합성곱층2
with tf.name_scope('conv2') as conv2:
    w_conv2 = weight_variable('conv2', [5, 5, 32, 64])
    b_conv2 = bias_variable('conv2', 64)
    h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)

# 풀링층2
with tf.name_scope('pool2') as pool2:
    h_pool2 = max_pool(h_conv2)

# 전결합층
with tf.name_scope('fully_connected') as fully_connected:
    n = 7 * 7 * 64
    w_fc = weight_variable('fc', [n, 1024])
    b_fc = bias_variable('fc', 1024)
    h_pool2_flat = tf.reshape(h_pool2, [-1, n])
    h_fc = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc) + b_fc)

# 드롭아웃(과잉 적합) 막기
with tf.name_scope('dropout') as dropout:
    keep_prob = tf.placeholder(tf.float32)
    h_fc_drop = tf.nn.dropout(h_fc, keep_prob)

# 출력층
with tf.name_scope('readout') as readout:
    w_fc2 = weight_variable('fc2', [1024, 10])
    b_fc2 = bias_variable('fc2', 10)
    y_conv = tf.nn.softmax(tf.matmul(h_fc_drop, w_fc2) + b_fc2)

# 모델 학습시키기
with tf.name_scope('loss') as loss:
    cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
with tf.name_scope('training') as training:
    optimizer = tf.train.AdamOptimizer(1e-4)
    train_step = optimizer.minimize(cross_entropy)

# 모델 평가하기
with tf.name_scope('predict') as predict:
    predict_step = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy_step = tf.reduce_mean(tf.cast(predict_step, tf.float32))


# feed_dict 설정하기
def set_feed(images, labels, prob):
    return {x: images, y_: labels, keep_prob: prob}


# 세션 시작하기
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    tw = tf.summary.FileWriter('log_dir', graph=sess.graph)
    # 테스트 전용 피드 만들기
    test_fd = set_feed(mnist.test.images, mnist.test.labels, 1)
    # 학습 시작하기
    for step in range(10000):
        batch = mnist.train.next_batch(50)
        fd = set_feed(batch[0], batch[1], 0.5)
        _, loss = sess.run([train_step, cross_entropy], feed_dict=fd)
        if step % 100 == 0:
            acc = sess.run(accuracy_step, feed_dict=test_fd)
            print('step=', step, 'loss=', loss, 'acc=', acc)
    # 최종 결과 출력
    acc = sess.run(accuracy_step, feed_dict=test_fd)
    print('정답률=', acc)
