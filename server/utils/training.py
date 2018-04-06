import numpy as np
from config import DataDetails

foo = DataDetails()

def get_data_and_label():
    data = open('../../data/debates/vectorized.txt', 'r')

    dataset = []
    for datum in data:
        datum = [float(x) for x in datum.split(',')]
        dataset.append(datum)
    
    classifications = open('../../data/debates/ground_sentence_class.txt', 'r')

    labels = []
    for cl in classifications:
        classification = [0,0]
        classification[int(cl)] = 1
        labels.append(classification)
    
    return dataset, labels

def numpy_array(arr):
    # return numpy array version of dataset and label
    return np.asarray(arr)
