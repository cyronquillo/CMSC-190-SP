import tensorflow as tf


state = tf.Variable(0)



one = tf.constant(1)
new_value = tf.add(state, one)
update = tf.assign(state,new_value)

a = tf.placeholder(tf.float32)
b = a*2
init_op = tf.global_variables_initializer()

with tf.Session() as session:
    result = session.run(b, feed_dict = {a:3.5})
    print(result)
    session.run(init_op)
    print(session.run(state))
    for _ in range(3):
        session.run(update)
        print(session.run(state))
