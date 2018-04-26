import os
import sys
import pickle
import numpy as np

import sklearn as sk
from sklearn import svm
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../../utils')

from training_operation import get_data_and_label, numpy_array

save_path = 'SVM.sav'



dataset, labels = get_data_and_label()
labels = numpy_array(labels)
dataset = numpy_array(dataset)

labels = np.array([1 if y[1] == 1 else 0 for y in list(labels)])

def train():

    

    model = svm.SVC(kernel='rbf', gamma='auto', verbose=2,
                    max_iter=-1, probability=True)

    model.fit(dataset, labels)

    pickle.dump(model, open(save_path, 'wb'))

    y_pred = model.predict(dataset)
    print("Train Accuracy:", sk.metrics.accuracy_score(labels, y_pred))


def vectorize_input(sentence):
    

    
def classify(vector):
    model = pickle.load(open(save_path, 'rb'))
    # y_pred = model.predict(dataset)
    # print("Train Accuracy:", accuracy_score(labels, y_pred))
    # print("Train F1 Score:", f1_score(labels, y_pred))
    # print("Train Precision:", precision_score(labels, y_pred))
    # print("Train Recall:", recall_score(labels, y_pred))
    prob_score = model.predict_proba(vector)
    y_pred = model.predict(vector)
    return prob_score

classify()
