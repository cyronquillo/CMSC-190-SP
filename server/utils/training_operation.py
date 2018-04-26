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


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])
    
def has_converged(num1, num2, dp=6):
    num1 = truncate(num1, dp)
    num2 = truncate(num2, dp)
    return num1 == num2

