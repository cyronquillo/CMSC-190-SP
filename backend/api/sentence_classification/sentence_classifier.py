import os
import sys
import json
import numpy as np
from nltk import sent_tokenize

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../../utils')

from data_vectorize import get_from_wdc, get_word_count, get_pos_tags
from training_operation import get_data_and_label, numpy_array
from training_execution import train_main_model, use_main_model
from config import DataDetails

foo = DataDetails()

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

    
def classify(vectors):
    prob_score = use_main_model(
        {
            'learning_rate': learning_rate,
            'training_epochs': training_epochs,
            'input': vectors
        }
    )
    
    dic_prob_scores = {}
    for i in range(len(prob_score)):
        dic_prob_scores[str(i)] = str(round(prob_score[i][1], 4))
    print(json.dumps(dic_prob_scores))


def extract_features(transcript):
    sentences = sent_tokenize(transcript)
    vectors = []
    data = ""
    feature_index = foo.features
    i = 1
    for sent in sentences:
        i += 1
        features = [0] * foo.feature_size

        sentiment, entities = get_from_wdc(sent)

        '''
            stores sentiment score
        '''
        sentiment_index = feature_index['sentiment']
        features[sentiment_index] = sentiment

        '''
            stores existing entity types per sentence
        '''
        for entity in entities:
            entity_type = "et_" + entity["type"]
            entity_index = feature_index[entity_type]
            features[entity_index] += 1

        '''
            stores word count per sentence
        '''
        word_count = get_word_count(sent)
        word_count_index = feature_index["word_count"]
        features[word_count_index] = word_count

        '''
            stores part-of-speech tags for each words per sentence
        '''

        pos_tags = get_pos_tags(sent)
        for pos_tuple in pos_tags:
            feature_tag = "pos_" + pos_tuple[1]
            if feature_tag in feature_index:
                pos_index = feature_index[feature_tag]
                features[pos_index] += 1

        '''
            append features extracted from current sentences list of vectors
        '''

        vectors.append(features)
    return vectors


vectors = extract_features(sys.argv[1])
classify(vectors)
# extract_features(sentences)
# classify([0])
