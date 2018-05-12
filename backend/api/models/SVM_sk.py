import os
import sys
import numpy as np

import sklearn as sk
from sklearn import svm
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../../utils')


from config import DataDetails

dd = DataDetails()


def support_vector_machine(dataset, labels, train_index, test_index,
                           kernel_coeff, training_epochs, threshold):

    
    #modify labels
    labels = np.array([1 if y[1] == 1 else 0 for y in list(labels)])

    #train and test data
    data_train, data_test = dataset[train_index], dataset[test_index]
    label_train, label_test = labels[train_index], labels[test_index]


    # construct SVM model
    model = svm.SVC(kernel='rbf', gamma = kernel_coeff, verbose = 2, max_iter = training_epochs, probability = True)
    

    model.fit(data_train, label_train)


    y_train = model.predict(data_train)       
    print("Epoch: ", training_epochs) 
    
    
    y_pred = model.predict_proba(data_test)

    y_pred = np.array(
        [1 if y[1] >= threshold else 0 for y in list(y_pred)])

    train_accuracy = accuracy_score(label_train, y_train)
    test_accuracy = accuracy_score(label_test, y_pred)
    precision = precision_score(label_test, y_pred)
    recall = recall_score(label_test, y_pred)
    f1 = f1_score(label_test, y_pred)


    print("Train Accuracy:", train_accuracy)
    print("Test Accuracy: ", test_accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1 Score: ", f1)

    return train_accuracy, test_accuracy, precision, recall, f1


