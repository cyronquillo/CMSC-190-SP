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


save_path = '../api/models/states/SVM_fGD.ckpt'
from config import DataDetails

dd = DataDetails()


def support_vector_machine(dataset, labels, train_index, test_index,
                           learning_rate, training_epochs, display_step=1, train_fold=4):

    # modify labels
    print(labels)
    labels = np.array([1 if y[1] == 1 else -1 for y in list(labels)])

    data_train, data_test = dataset[train_index], dataset[test_index]
    label_train, label_test = labels[train_index], labels[test_index]

    size = len(data_train)//4


    # Initialize placeholders
    x = tf.placeholder(shape=[None, dd.feature_size], dtype=tf.float32)
    y = tf.placeholder(shape=[None, 1], dtype=tf.float32)
    prediction_grid = tf.placeholder(
        shape=[None, dd.feature_size], dtype=tf.float32)

    # Create variables for svm
    b = tf.Variable(tf.random_normal(shape=[1, size]))

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
    saver = tf.train.Saver()
    
    '''
        training session
    '''
    # with tf.Session() as sess:
    #     sess.run(init)

    #     # Training loop
    #     loss_vec = []
        
    #     for epoch in range(training_epochs):
    #         batch_accuracy = []
    #         for fold in range(train_fold):
    #             lower = fold * size
    #             upper = (fold + 1) * size
    #             if upper > len(data_train):
    #                 break
    #             batch_x, batch_y = np.asarray(data_train[lower:upper]), np.asarray(label_train[lower:upper])
    #             batch_y = np.transpose([batch_y])
    #             sess.run(train_step, feed_dict={x: batch_x, y: batch_y})

    #             temp_loss = sess.run(loss, feed_dict={x: batch_x, y: batch_y})
    #             loss_vec.append(temp_loss)

    #             acc_temp = sess.run(accuracy, feed_dict={x: batch_x,
    #                                                     y: batch_y,
    #                                                     prediction_grid: batch_x})
    #             batch_accuracy.append(acc_temp)

    #         if (epoch+1) % display_step == 0 or epoch == 0:
    #             acc = sum(batch_accuracy)/float(len(batch_accuracy))
    #             print('Epoch: ' + str(epoch + 1))
    #             print('Epoch Accuracy: ' + str(acc))
    #             print('Loss = ' + str(temp_loss))
    #     saver.save(sess, save_path)
    #     lower = 0
    #     upper = size
    #     batch_x = data_test[lower:upper]
    #     batch_y = label_test[lower:upper]        
    #     accu_test = sess.run(accuracy, feed_dict=({x: batch_x,
    #                                                 y: np.transpose([batch_y]),
    #                                                 prediction_grid: batch_x}))
    #     print("Accuracy:",accu_test)
    #     return accu_test
    '''
        testing session
    '''
    with tf.Session() as sess:
        sess.run(init)

        saver.restore(sess,save_path)
        lower = 0
        upper = size
        batch_x = np.asarray(data_test[lower:upper])
        batch_y = np.asarray(label_test[lower:upper])
        predict_op = tf.nn.softmax(prediction)

        # for i in range(size):
            # batch_x[i] = batch_x[0]
            # batch_y[i] = batch_y[1]


            
        # pre = my_kernel
    
        print(prediction)
        print(prediction_output)
        # best = sess.run(prediction_output, feed_dict=({x: batch_x}))
        # accu_test = sess.run(predict_op, feed_dict=({x: batch_x,
                                                    # y: np.transpose([batch_y]),
                                                    # prediction_grid: batch_x}))
        print("Accuracy:",0)
        return 0
