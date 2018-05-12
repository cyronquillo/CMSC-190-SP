import requests
import urllib.parse

def get_score_on_claimbuster(url):  
    try:  
        req = requests.get(url)
        print(req)
        res = req.json()['results']
        return res[0]['score']
    except:
        print("entered exception")
        return get_score_on_claimbuster(url)

def generate_url_extension(delimiter, sentence):
    url_extension = urllib.parse.quote_plus(sentence)
    url_extension = url_extension.replace('+', delimiter)
    return url_extension

def generate_target(delimiter, data_path, url):
    f_read = open(data_path, 'r')
    i = 0
    scores = []
    for line in f_read:
        print("getting score for sentence:" + str(i+1), end=" ")
        i+=1
        url_extension = generate_url_extension(delimiter, line)
        scores.append(get_score_on_claimbuster(url + url_extension))
    f_read.close()
    return scores

def adjust_threshold(th, score_path, class_path):
    scores = open(score_path, 'r')
    new_class = open(class_path, 'w')
    for score in scores:
        if float(score) < th:
            new_class.write('0\n')
        else:
            new_class.write('1\n')
    new_class.close()
    scores.close()


def start():

    scores = generate_target(delimiter, data_path, url)
    f_write0 = open(target_output_class_path, 'w')
    f_write1 = open(target_output_score_path, 'w')

    for score in scores:
        f_write1.write(str(score) + "\n")
        
        score_class = 0 if float(score) < threshold else 1
        f_write0.write(str(score_class) + "\n")
    f_write0.close()
    f_write1.close()

delimiter = '%20'
url = 'http://idir-server2.uta.edu:80/factchecker/score_text/'
data_path = '../data/debates/preprocessed.txt'
target_output_score_path = '../data/debates/ground_sentence_score.txt'
target_output_class_path = '../data/debates/ground_sentence_class.txt'
# threshold = 0.40
# threshold = 0.50
threshold = 0.30
adjust_threshold(threshold, target_output_score_path, target_output_class_path)
