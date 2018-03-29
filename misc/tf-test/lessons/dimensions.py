import tensorflow as tf

Scalar = tf.constant([2])
Vector = tf.constant([2, 6, 3])
Matrix = tf.constant([[2, 6, 3], [1, 4, 5], [7, 8, 9]])
Tensor = tf.constant([[[1,2,3], [2,3,4],[3,4,5]], [[4,5,6],[5,6,7],[6,7,8]]])

with tf.Session() as session:
    result = session.run(Scalar)
    print("Scalar:", result)
    result = session.run(Vector)
    print("Vector:", result)
    result = session.run(Matrix)
    print("Matrix:", result)
    result = session.run(Tensor)
    print("Tensor:", result)
