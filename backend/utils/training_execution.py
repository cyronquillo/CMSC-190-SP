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
from main_model import main_model

models = {
    'SVM': [support_vector_machine, 'Support Vector Machine'],
    'NN': [multilayer_perceptron, 'Multilayer Perceptron'],
    'LR': [logistic_regression, 'Logistic Regression'],
    'main': [main_model, 'Logistic Regression']
}

fold = 5
kf = KFold(n_splits = fold)

dataset, labels = get_data_and_label()
labels = numpy_array(labels)
dataset = numpy_array(dataset)

def train_main_model(params):
    main_model = models['main']
    print("Training " + main_model[1] +  ":")
    main_model[0](dataset, labels, None, 
        params['learning_rate'], params['training_epochs'])
def use_main_model(params):
    main_model = models['main']
    
    prob_score = main_model[0](dataset, labels, params['input'],
                    params['learning_rate'], params['training_epochs'])

    return prob_score

def run_model():
    threshold = 0.5
    learning_rates = ['auto', 0.01, 0.001]
    training_epochs = [100, 500, 1000, 2000, 5000]
    fp = open('../api/models/metrics/metrics_' + str(threshold) + '.txt', 'w')
    for key in models:
        fp.write('\n' + key + ':\nparameters:\n')
        for lr in learning_rates:
            for epoch in training_epochs:
                if lr == 'auto' and key != 'SVM' :
                    break
                if key == 'SVM':
                    fp.write('gamma=' + str(lr) + '\t')
                else:
                    fp.write('learning_rate=' + str(lr) + '\t')    
                fp.write('epoch_size=' + str(epoch) + '\n')

                test_accuracy_list = []
                train_accuracy_list = []
                f1_score_list = []
                precision_list = []
                recall_list = []


                curr_fold = 1
                print("Running", models[key][1], "Classification: ")
                for train_index, test_index in kf.split(dataset):
                    print("Processing Fold:", curr_fold)
                    curr_fold += 1
                    train_accuracy, test_accuracy, precision, recall, f1 = models[key][0](
                        dataset, labels, train_index, test_index, lr, epoch, threshold)
                    test_accuracy_list.append(test_accuracy)
                    train_accuracy_list.append(train_accuracy)
                    f1_score_list.append(f1)
                    precision_list.append(precision)
                    recall_list.append(recall)
                kfold_test_acc = str(
                    sum(test_accuracy_list)/float(len(test_accuracy_list)))
                kfold_train_acc = str(
                    sum(train_accuracy_list)/float(len(train_accuracy_list)))
                kfold_f1 = str(
                    sum(f1_score_list)/float(len(f1_score_list)))
                kfold_precision = str(
                    sum(precision_list)/float(len(precision_list)))
                kfold_recall = str(
                    sum(recall_list)/float(len(recall_list)))
                print('KFold Average Train Accuracy: ' + 
                    kfold_train_acc)
                fp.write('kfold train accuracy: ' + kfold_train_acc + '\n')
                fp.write('kfold test accuracy: ' + kfold_test_acc + '\n')
                fp.write('kfold precision score: ' + kfold_precision + '\n')
                fp.write('kfold recall score: ' + kfold_recall + '\n')
                fp.write('kfold f1 score: ' + kfold_f1 + '\n')
