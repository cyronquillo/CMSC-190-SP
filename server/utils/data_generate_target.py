import requests


def get_scores_on_claimbuster(url):
    scores = []
    
    print("processing")
    req = requests.get(url)
    req_json = req.json()
    for result in req_json['results']:
        scores.append(result['score'])
    return scores

def generate_url_extension(delimiter, data_path):
    url_extension = ""
    f_read = open(data_path, 'r')
    i = 0
    for line in f_read:
        print("adding sentence:", i+1)
        i+=1
        # words = line.split()
        # for word in words:
            # url_extension += (word + delimiter)
        url_extension += line
    f_read.close()

    return url_extension


threshold = 0.40
# threshold = 0.50
# threshold = 0.30
delimiter = '%20'
url = 'http://idir-server2.uta.edu:80/factchecker/score_text/'
data_path = '../data/debates/preprocessed.txt'
target_output_score_path = '../data/debates/ground_sentence_score.txt'
target_output_class_path = '../data/debates/ground_sentence_class.txt'
url_extension = generate_url_extension(delimiter, data_path)

scores = get_scores_on_claimbuster(url+url_extension)
f_write0 = open(target_output_class_path, 'w')
f_write1 = open(target_output_score_path, 'w')

for score in scores:
    f_write1.write(str(score) + "\n")
    
    score_class = 0 if score < threshold else 1
    f_write0.write(str(score_class) + "\n")
f_write0.close()
f_write1.close()
