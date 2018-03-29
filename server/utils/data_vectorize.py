
from config import DataDetails
# import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, SentimentOptions
import nltk
from nltk.tokenize import RegexpTokenizer
sentence_tokenizer = RegexpTokenizer(r'\w+')

foo = DataDetails()

def get_from_wdc(sentence):
    '''
        gets the sentiment score and entities in the sentence
    '''

    API_KEY = foo.API_KEY
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version=API_KEY['version'],
        username=API_KEY['username'],
        password=API_KEY['password']
    )

    try:
        response = natural_language_understanding.analyze(
            text=sentence,
            features=Features(entities=EntitiesOptions(), sentiment=SentimentOptions())
        )
        # print(json.dumps(response, indent=2))
    except:
        print("entered exception")
        return get_from_wdc(sentence)

    return response["sentiment"]["document"]["score"], response["entities"]

def get_word_count(sentence):
    words = sentence_tokenizer.tokenize(sentence)

    return len(words)

def get_pos_tags(sentence):
    words = nltk.word_tokenize(sentence)

    return nltk.pos_tag(words)

def vectorize_data():
    f_read = open("../data/debates/preprocessed.txt", "r")
    f_write = open("../data/debates/vectorized.txt", "w")
    data = ""
    feature_index = foo.features
    i = 1
    for line in f_read:
        print("extracting feature for unit: ", i)
        i += 1
        features = [0] * foo.feature_size

        sentiment, entities = get_from_wdc(line)

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
        word_count = get_word_count(line)
        word_count_index = feature_index["word_count"]
        features[word_count_index] = word_count


        '''
            stores part-of-speech tags for each words per sentence
        '''

        pos_tags = get_pos_tags(line)
        for pos_tuple in pos_tags:
            feature_tag = "pos_" + pos_tuple[1]
            if feature_tag in feature_index:
                pos_index = feature_index[feature_tag]
                features[pos_index] += 1
        
        
        '''
            write features extracted from current sentences to vectorized file
        '''

        string_line_features = ','.join(str(x) for x in features)
        f_write.write(string_line_features + "\n")
    f_write.close()
    f_read.close()


vectorize_data()


        


    
