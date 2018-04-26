""" Neural Network.
A 2-Hidden Layers Fully Connected Neural Network (a.k.a Multilayer Perceptron)
implementation with TensorFlow. This example is using the MNIST database
of handwritten digits (http://yann.lecun.com/exdb/mnist/).
Links:
    [MNIST Dataset](http://yann.lecun.com/exdb/mnist/).
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
"""

from __future__ import division, print_function, absolute_import
import os
import sys
import tensorflow as tf
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../../utils')

from config import DataDetails
from training_operation import next_batch

dd = DataDetails()


def multilayer_perceptron(dataset, labels, train_index, test_index,
    learning_rate=0.01,training_epochs=1000, display_step=20):

    # Network Parameters
    n_hidden_1 = 256  # 1st layer number of neurons
    n_hidden_2 = 256  # 2nd layer number of neurons
    n_hidden_3 = 256  # 3rd layer number of neurons
    n_hidden_4 = 256  # 3rd layer number of neurons

    # tf Graph input
    X = tf.placeholder("float", [None, dd.feature_size])
    Y = tf.placeholder("float", [None, dd.classification])

    # Store layers weight & bias
    weights = {
        'h1': tf.Variable(tf.random_normal([dd.feature_size, n_hidden_1])),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
        'h3': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3])),
        'h4': tf.Variable(tf.random_normal([n_hidden_3, n_hidden_4])),
        'out': tf.Variable(tf.random_normal([n_hidden_4, dd.classification]))
    }
    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1])),
        'b2': tf.Variable(tf.random_normal([n_hidden_2])),
        'b3': tf.Variable(tf.random_normal([n_hidden_3])),
        'b4': tf.Variable(tf.random_normal([n_hidden_4])),
        'out': tf.Variable(tf.random_normal([dd.classification]))
    }

    # Create model
    def neural_net(x):
        # Hidden fully connected layer with 256 neurons
        layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
        # Hidden fully connected layer with 256 neurons
        layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
        # Hidden fully connected layer with 256 neurons
        layer_3 = tf.add(tf.matmul(layer_2, weights['h3']), biases['b3'])
        # Hidden fully connected layer with 256 neurons
        layer_4 = tf.add(tf.matmul(layer_3, weights['h4']), biases['b4'])
        # Output fully connected layer with a neuron for each class
        out_layer = tf.matmul(layer_4, weights['out']) + biases['out']
        return out_layer

    # Construct model
    logits = neural_net(X)
    prediction = tf.nn.softmax(logits)

    # Define loss and optimizer
    loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
        logits=logits, labels=Y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
    train_op = optimizer.minimize(loss_op)

    # Evaluate model
    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    # Initialize the variables (i.e. assign their default value)
    init = tf.global_variables_initializer()

    # Start training
    with tf.Session() as sess:

        # Run the initializer
        sess.run(init)

        data_train, data_test = dataset[train_index], dataset[test_index]
        label_train, label_test = labels[train_index], labels[test_index]
        
        #Training cycle
        for epoch in range(1, training_epochs+1):
            # Run optimization op (backprop)
            sess.run(train_op, feed_dict={X: data_train, Y: label_train})
            if epoch % display_step == 0 or epoch == 1:
                # Calculate batch loss and accuracy
                loss, acc = sess.run([loss_op, accuracy], feed_dict={X: data_train,
                                                                    Y: label_train})
                print("Step " + str(epoch) + ", Loss= " +
                    "{:.4f}".format(loss) + ", Training Accuracy= " +
                    "{:.3f}".format(acc))

        print("Optimization Finished!")

        # Calculate accuracy for MNIST test images
        accu_value = sess.run(accuracy, feed_dict={X: data_test, Y: label_test})

        print("Accuracy:", accu_value, "\n")
        return accu_value
