from nltk import sent_tokenize
import sys
import json

def main(transcript):
    sentences = sent_tokenize(transcript)

    dic_sentences = {}
    for i in range(len(sentences)):
        dic_sentences[str(i)] = sentences[i]
    print(json.dumps(dic_sentences))







# print(sys.argv[1])
main(sys.argv[1])