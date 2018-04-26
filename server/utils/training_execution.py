from __future__ import print_function
import os
import sys
from sklearn.model_selection import KFold

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../api/models')

from training_operation import get_data_and_label, numpy_array

from LR_fGD import logistic_regression
from SVM_sk import support_vector_machine
from NN_fA import multilayer_perceptron

models = {
    'LR': [logistic_regression, 'Logistic Regression'], 
    'SVM': [support_vector_machine, 'Support Vector Machine'],
    'NN': [multilayer_perceptron, 'Multilayer Perceptron']
}

fold = 5
kf = KFold(n_splits = fold)

dataset, labels = get_data_and_label()
labels = numpy_array(labels)
dataset = numpy_array(dataset)

def run_model(model=models['SVM']):
    accuracy_list = []
    curr_fold = 1
    print("Running", model[1], "Classification: ")
    for train_index, test_index in kf.split(dataset):
        print("Processing Fold:", curr_fold)
        curr_fold += 1
        accuracy_value = model[0](dataset, labels, train_index, test_index)
        accuracy_list.append(accuracy_value)
        break
    print('KFold Average Accuracy: ' + 
          str(sum(accuracy_list)/float(len(accuracy_list))))


def train_classifier()

run_model()
