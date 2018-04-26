# Nonlinear SVM Example
#----------------------------------
#
# This function wll illustrate how to
# implement the gaussian kernel on
# the iris dataset.
#
# Gaussian Kernel:
# K(x1, x2) = exp(-gamma * abs(x1 - x2)^2)

from __future__ import print_function
import os
import sys
import tensorflow as tf
from sklearn.model_selection import train_test_split, KFold
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../../utils')

from config import DataDetails
from training_operation import next_batch

dd = DataDetails()

def support_vector_machine(dataset, labels, train_index, test_index,
    learning_rate=0.01, training_epochs=500, testing=2**32, display_step=500, batch_size=100):

    # Parameters
    # learning_rate = 0.01
    # training_epochs = 1000
    # testing = 100
    # display_step = 100
    # batch_size = 100


    # modify labels
    labels = np.array([1 if y[1] == 1 else -1 for y in list(labels)])

    #data split
    # data_train, data_test, label_train, label_test = train_test_split(
        # dataset, labels, test_size = test_ratio, random_state = 42)

    # Initialize placeholders
    x = tf.placeholder(shape=[None, dd.feature_size], dtype=tf.float32)
    y = tf.placeholder(shape=[None, 1], dtype=tf.float32)
    prediction_grid = tf.placeholder(shape=[None, dd.feature_size], dtype=tf.float32)

    # Create variables for svm
    b = tf.Variable(tf.random_normal(shape=[1, batch_size]))

    # Gaussian (RBF) kernel
    gamma = tf.constant(-25.0)
    sq_dists = tf.multiply(2., tf.matmul(x, tf.transpose(x)))
    my_kernel = tf.exp(tf.multiply(gamma, tf.abs(sq_dists)))

    # Compute SVM Model
    first_term = tf.reduce_sum(b)
    b_vec_cross = tf.matmul(tf.transpose(b), b)
    y_cross = tf.matmul(y, tf.transpose(y))
    second_term = tf.reduce_sum(tf.multiply(
        my_kernel, tf.multiply(b_vec_cross, y_cross)))
    loss = tf.negative(tf.subtract(first_term, second_term))

    # Gaussian (RBF) prediction kernel
    rA = tf.reshape(tf.reduce_sum(tf.square(x), 1), [-1, 1])
    rB = tf.reshape(tf.reduce_sum(tf.square(prediction_grid), 1), [-1, 1])
    pred_sq_dist = tf.add(tf.subtract(rA, tf.multiply(2., tf.matmul(
        x, tf.transpose(prediction_grid)))), tf.transpose(rB))
    pred_kernel = tf.exp(tf.multiply(gamma, tf.abs(pred_sq_dist)))

    prediction_output = tf.matmul(tf.multiply(
        tf.transpose(y), b), pred_kernel)
    prediction = tf.sign(prediction_output-tf.reduce_mean(prediction_output))
    accuracy = tf.reduce_mean(
        tf.cast(tf.equal(tf.squeeze(prediction), tf.squeeze(y)), tf.float32))

    # Declare optimizer
    my_opt = tf.train.GradientDescentOptimizer(learning_rate)
    train_step = my_opt.minimize(loss)

    # Initialize variables
    init = tf.global_variables_initializer()


    with tf.Session() as sess:
        sess.run(init)

        data_train, data_test = dataset[train_index], dataset[test_index]
        label_train, label_test = labels[train_index], labels[test_index]

        # Training loop
        loss_vec = []
        batch_accuracy = []
        for epoch in range(training_epochs):
            batch_x, batch_y = next_batch(batch_size, data_train, label_train)
            batch_y = np.transpose([batch_y])
            sess.run(train_step, feed_dict={x: batch_x, y: batch_y})

            temp_loss = sess.run(loss, feed_dict={x: batch_x, y: batch_y})
            loss_vec.append(temp_loss)

            acc_temp = sess.run(accuracy, feed_dict={x: batch_x,
                                                    y: batch_y,
                                                    prediction_grid: batch_x})
            batch_accuracy.append(acc_temp)

            if (epoch+1) % display_step == 0:
                print('Epoch: ' + str(epoch + 1))
                print('Loss = ' + str(temp_loss))
        batch_test_accuracy = []
        for test in range(testing):
            try:
                lower = test * batch_size
                upper = (test+1) * batch_size            
                batch_x = data_test[lower:upper] 
                batch_y = label_test[lower:upper]
                accu_test = sess.run(accuracy, feed_dict=({ x: batch_x, 
                                        y: np.transpose([batch_y]),
                                        prediction_grid: batch_x}))
                batch_test_accuracy.append(accu_test)
            except:
                #terminate testing when everything on test data has been tested
                break
        
        test_accuracy = sum(batch_test_accuracy)/float(len(batch_test_accuracy))
        print("Accuracy:", test_accuracy, "\n")
        return test_accuracy
        
