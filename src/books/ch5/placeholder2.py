import tensorflow as tf

a = tf.placeholder(tf.int32, [None])  # 배열의 크기를 None 으로 지정

# 배열의 모든 값을 10배하는 연산 정의하기
b = tf.constant(10)
x10_op = a * b

# 세션 시작
sess = tf.Session()

# 플레이스 홀더 값을 넣고 실행
r1 = sess.run(x10_op, feed_dict={a: [1, 2, 3, 4, 5]})
print(r1)
r2 = sess.run(x10_op, feed_dict={a: [10, 20]})
print(r2)
