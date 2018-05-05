
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

save_path = './model_checkpoint/main_model.ckpt'

def main_model(dataset, labels, test_data, learning_rate, training_epochs, display_step=10):

    print(dataset)
    print(test_data)
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
    saver = tf.train.Saver()
    
    if test_data is None:
        #do training
        with tf.Session() as sess:

            # Run the initializer
            sess.run(init)
            train_accuracy = -1
            # Training cycle
            for epoch in range(training_epochs):
                # Run optimization op (backprop) and cost op (to get loss value)
                _, cost_val = sess.run([optimizer, cost], feed_dict={x: dataset,
                                                                y: labels})

                train_accuracy = accuracy.eval({x: dataset, y: labels})

                if (epoch+1) % display_step == 0:
                    print("Epoch:", '%04d' % (epoch+1),
                        "cost=", "{:.9f}".format(cost_val),
                        "acc=", train_accuracy)

            print("Optimization Finished!")
            saver.save(sess, save_path)
            exit()
    else:
        with tf.Session() as sess:
            sess.run(init)
            saver.restore(sess, save_path)

            probability_score = sess.run(pred, feed_dict={x: [test_data]})                   
            return probability_score[0][1]

