
'''
Logistic Regression: https://github.com/aymericdamien/TensorFlow-Examples/
KFold Cross Validation: http: // scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html
'''

from __future__ import print_function
import os
import sys
import tensorflow as tf
from sklearn.model_selection import train_test_split, KFold
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../../utils')

from config import DataDetails
from training import get_data_and_label, numpy_array

dd = DataDetails()


dataset, labels = get_data_and_label()
labels = numpy_array(labels)
dataset = numpy_array(dataset)

def next_batch(n, data, labels):
    '''
    Return a total of n random samples and labels. 
    '''
    idx = np.arange(0, len(data))
    np.random.shuffle(idx)
    idx = idx[:n]
    data_shuffle = [data[i] for i in idx]
    labels_shuffle = [labels[i] for i in idx]

    return np.asarray(data_shuffle), np.asarray(labels_shuffle)

# Parameters
test_ratio = 0.2
learning_rate = 0.01
training_epochs = 60
batch_size = 50
display_step = 1
fold = 5
kf = KFold(n_splits = fold)
# data_train, data_test, label_train, label_test = train_test_split(
#     dataset, labels, test_size=test_ratio, random_state=42)
    
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
with tf.Session()as sess:
    # data_train, data_test, label_train, label_test = train_test_split(
    #     dataset, labels, test_size=test_ratio, random_state=42)
    # Run the initializer
    sess.run(init)
    
    f_write = open('LR.txt', 'w')
    f_write.write("KFold Cross Validation of Logistic Regression (k = " + str(fold) + ")\n")
    accu_list = []
    current_fold = 1
    for train_index, test_index in kf.split(dataset):
        print("Fold Count: ", current_fold)
        current_fold += 1
        data_train, data_test = dataset[train_index], dataset[test_index]
        label_train, label_test =labels[train_index], labels[test_index]
        # Training cycle
        for epoch in range(training_epochs):
            avg_cost = 0.0
            total_batch = int(dd.dataset_size/batch_size)
            # Loop over all batches
            for i in range(total_batch):
                batch_xs, batch_ys = next_batch(batch_size, data_train, label_train)
                # Run optimization op (backprop) and cost op (to get loss value)
                _, c = sess.run([optimizer, cost], feed_dict={x: batch_xs,
                                                            y: batch_ys})
                # Compute average loss
                avg_cost += c / total_batch
            # Display logs per epoch step
            if (epoch+1) % display_step == 0:
                print("Epoch:", '%04d' % (epoch+1),
                    "cost=", "{:.9f}".format(avg_cost))

        print("Optimization Finished!")

        # Test model
        correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
        # Calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        accu_value = accuracy.eval({x: data_test, y: label_test})
        accu_list.append(accu_value)
        print("Accuracy:", accu_value)
        f_write.write("Accuracy: " + str(accu_value) + "\n")


    f_write.write("Average Accuracy: " + str(sum(accu_list)/float(len(accu_list))))
    f_write.close()
