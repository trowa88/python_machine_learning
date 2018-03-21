import tensorflow as tf

# 상수 정의
a = tf.constant(120, name='a')
b = tf.constant(130, name='b')
c = tf.constant(140, name='c')

# 변수 정의
v = tf.Variable(0, name='v')

# 데이터 플로우 그래드 정의
calc_op = a + b + c
assign_op = tf.assign(v, calc_op)

# 세션 실행하기
sess = tf.Session()
sess.run(assign_op)

print(sess.run(v))
