import tensorflow as tf

# 데이터 플로우 그래프 구축
a = tf.constant(20, name='a')
b = tf.constant(30, name='b')
mul_op = a * b

# 세션 생성
sess = tf.Session()

# TensorBoard 사용
tw = tf.summary.FileWriter('log_dir', graph=sess.graph)

# 세션 실행
print(sess.run(mul_op))
