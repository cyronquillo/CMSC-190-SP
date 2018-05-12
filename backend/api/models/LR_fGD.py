
'''
Logistic Regression: https://github.com/aymericdamien/TensorFlow-Examples/
KFold Cross Validation: http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html
'''

from __future__ import print_function
import os
import sys
import tensorflow as tf
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../../utils')

from config import DataDetails

dd = DataDetails()



def logistic_regression(dataset, labels, train_index, test_index,
    learning_rate, training_epochs, threshold, display_step=10):

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

    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Initialize the variables (i.e. assign their default value)
    init = tf.global_variables_initializer()

    # Start training
    with tf.Session() as sess:

        # Run the initializer
        sess.run(init)
        train_accuracy = -1
        # Training cycle
        for epoch in range(training_epochs):
            # Run optimization op (backprop) and cost op (to get loss value)
            _, cost_val = sess.run([optimizer, cost], feed_dict={x: data_train,
                                                            y: label_train})

            train_accuracy = accuracy.eval({x: data_train, y: label_train})

            if (epoch+1) % display_step == 0:
                print("Epoch:", '%04d' % (epoch+1),
                    "cost=", "{:.9f}".format(cost_val))

        print("Optimization Finished!")
    
        
        y_true = np.argmax(label_test, 1)
        y_pred = sess.run(pred, feed_dict={x: data_test})
        y_pred = np.array([1 if y[1] >=threshold else 0 for y in list(y_pred)])
