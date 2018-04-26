
'''
Logistic Regression: https://github.com/aymericdamien/TensorFlow-Examples/
KFold Cross Validation: http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html
'''

from __future__ import print_function
import os
import sys
import tensorflow as tf
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../../utils')

from config import DataDetails
from training_operation import next_batch

dd = DataDetails()



def logistic_regression(dataset, labels, train_index, test_index,
    learning_rate=0.01, training_epochs=10000, batch_size=100, display_step=500):
    
    data_train, data_test = dataset[train_index], dataset[test_index]
    label_train, label_test =labels[train_index], labels[test_index]
    # Parameters
        
    x = tf.placeholder(tf.float32, [None, dd.feature_size])
    y = tf.placeholder(tf.float32, [None, dd.classification])

    # Set model weights
    W = tf.Variable(tf.zeros([dd.feature_size, dd.classification]))
    b = tf.Variable(tf.zeros([dd.classification]))

    # Construct model
    pred = tf.nn.softmax(tf.matmul(x, W) + b)  # Softmax

    # Minimize error using cross entropy
    cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred), reduction_indices=1))
    # Gradient Descent
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

    # Initialize the variables (i.e. assign their default value)
    init = tf.global_variables_initializer()

    # Start training
    with tf.Session() as sess:

        # Run the initializer
        sess.run(init)
        
        # Training cycle
        for epoch in range(training_epochs):
            batch_x, batch_y = next_batch(batch_size, data_train, label_train)
            # Run optimization op (backprop) and cost op (to get loss value)
            _, cost_val = sess.run([optimizer, cost], feed_dict={x: data_train,
                                                            y: label_train})
            if (epoch+1) % display_step == 0:
                print("Epoch:", '%04d' % (epoch+1),
                    "cost=", "{:.9f}".format(cost_val))

        print("Optimization Finished!")

        # Test model
        correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
        # Calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        accu_value = accuracy.eval({x: data_test, y: label_test})

        print("Accuracy:", accu_value, "\n")
        return accu_value

