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
from training_execution import train_main_model, use_main_model



dataset, labels = get_data_and_label()
labels = numpy_array(labels)
dataset = numpy_array(dataset)

labels = np.array([1 if y[1] == 1 else 0 for y in list(labels)])


learning_rate = 0.01
training_epochs = 5000   
def train():
    train_main_model(
        {
            'learning_rate': learning_rate,
            'training_epochs': training_epochs
        }
    )

    
def classify(vector):
    prob_score = use_main_model(
        {
            'learning_rate': learning_rate,
            'training_epochs': training_epochs,
            'input': vector
        }
    )
    print(prob_score)
    # return prob_score

classify([0])
