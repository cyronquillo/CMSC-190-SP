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
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../../utils')

from config import DataDetails
from training_operation import next_batch

dd = DataDetails()


def multilayer_perceptron(dataset, labels, train_index, test_index,
    learning_rate, training_epochs, threshold, display_step=10):

    # Network Parameters
    n_hidden_1 = 256  # 1st layer number of neurons
    n_hidden_2 = 256  # 2nd layer number of neurons

    # tf Graph input
    X = tf.placeholder("float", [None, dd.feature_size])
    Y = tf.placeholder("float", [None, dd.classification])

    # Store layers weight & bias
    weights = {
        'h1': tf.Variable(tf.random_normal([dd.feature_size, n_hidden_1])),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
        'out': tf.Variable(tf.random_normal([n_hidden_2, dd.classification]))
    }
    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1])),
        'b2': tf.Variable(tf.random_normal([n_hidden_2])),
        'out': tf.Variable(tf.random_normal([dd.classification]))
    }

    # Create model
    def neural_net(x):
        # Hidden fully connected layer with 256 neurons
        layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
        # Hidden fully connected layer with 256 neurons
        layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
        # Output fully connected layer with a neuron for each class
        out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
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
        train_accuracy = -1
        #Training cycle
        for epoch in range(1, training_epochs+1):
            # Run optimization op (backprop)
            sess.run(train_op, feed_dict={X: data_train, Y: label_train})
            if epoch % display_step == 0 or epoch == 1:
                # Calculate batch loss and accuracy
                loss, train_accuracy = sess.run([loss_op, accuracy], feed_dict={X: data_train,
                                                                    Y: label_train})
                print("Step " + str(epoch) + ", Loss= " +
                    "{:.4f}".format(loss) + ", Training Accuracy= " +
                    "{:.3f}".format(train_accuracy))

        print("Optimization Finished!")

        test_accuracy = sess.run(accuracy, feed_dict={X: data_test, Y: label_test})

        y_true = np.argmax(label_test, 1)
        y_pred = sess.run(prediction, feed_dict={X: data_test})
        y_pred = np.array(
            [1 if y[1] >= threshold else 0 for y in list(y_pred)])

        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)

        print("Training Accuracy: ", train_accuracy)
        print("Testing Accuracy:", test_accuracy)
        print("Precision Score:", precision)
        print("Recall Score:", recall)
        print("F1 Score:", f1)

        return train_accuracy, test_accuracy, precision, recall, f1
