import os
import sys
import numpy as np

import sklearn as sk
from sklearn import svm
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score, accuracy_score

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../../utils')


from config import DataDetails

dd = DataDetails()


def support_vector_machine(dataset, labels, train_index, test_index,
                           kernel_coeff = 0.01, training_epochs=10000):

    
    #modify labels
    labels = np.array([1 if y[1] == 1 else -1 for y in list(labels)])

    #train and test data
    data_train, data_test = dataset[train_index], dataset[test_index]
    label_train, label_test = labels[train_index], labels[test_index]


    # construct SVM model
    model = svm.SVC(kernel='rbf', gamma ='auto', verbose = 2, max_iter = training_epochs, probability = True)
    

    model.fit(data_train, label_train)


    y_pred = model.predict(data_train)       
    print("Epoch: ", training_epochs) 
    print("Train Accuracy:", accuracy_score(label_train, y_pred))
    
    y_test = model.predict(data_test)

    
    proba = model.predict_proba([data_test[0]])
    
    print(y_test)
    print(proba)
    
    acc = accuracy_score(label_test, y_test)
    print("Test Accuracy: ", acc)

    return acc


