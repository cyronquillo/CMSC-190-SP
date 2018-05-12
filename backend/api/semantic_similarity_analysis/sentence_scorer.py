import json
import sys
from inflection import singularize
from bllipparser import RerankingParser, Tree
import sqlite3 as sql
from nltk import sent_tokenize

from test_cases import generate_test_cases
from triplet import TripletExtraction
from similarity_analysis import SemanticSimilarityAnalysis

# tokenizer for word parsing
from nltk.tokenize import RegexpTokenizer
sentence_tokenizer = RegexpTokenizer(r'\w+')

conn = sql.connect('data/news/news.db')
c = conn.cursor()

satiric_shits = [
    'Duterte Trending News:',
    'Duterte Trending News',
    'MaharlikaNews @ykhy CW051017',
    'WATCH:',
    'The Maharlika:',

]

def main(transcript):
    results = {}
    sentences = sent_tokenize(transcript)

    '''
        Declaration of constants and functions
    '''
    
    CONS_SATIRIC = 0
    CONS_RELIABLE = 1
    rrp = RerankingParser.fetch_and_load('WSJ-PTB3')
    foo = TripletExtraction()
    bar = SemanticSimilarityAnalysis()



    '''
        2 database tables for comparison of input 
    '''  
    c.execute('SELECT title FROM reliable_news')
    reliable_news = [tup[0] for tup in c.fetchall()]

    c.execute('SELECT title FROM satirical_news')
    satirical_news = [tup[0] for tup in c.fetchall()]


    t = len(sentences)
    correct_classifications = 0
    for i in range(t):
        max_similarity = 0
        classification = -1  
        max_sentence = ""

        inp = sentences[i]

        ''' 
            generates the tree and gets the SVO of the input sentence
        '''
        tree_inp = Tree(rrp.simple_parse(inp))
        svo_inp = foo.getSVO(tree_inp[0])
        
        '''
            comparison for satirical and reliable news
        '''

        for title in satirical_news:
            for subj in svo_inp['subject']:
                if subj[2] == 0:
                    continue
                words = [x.lower() for x in sentence_tokenizer.tokenize(title)]
                if subj[0] in words or singularize(subj[0]) in words:
                    tree_data = Tree(rrp.simple_parse(title))
                    svo_data = foo.getSVO(tree_data[0])

                    similarity_score1= bar.get_similarities(svo_inp, svo_data)
                    '''
                        object and subject swapped to provde more possible comparisons
                    '''
                    svo_data['subject'], svo_data['object'] = svo_data['object'], svo_data['subject']
                    similarity_score2 = bar.get_similarities(svo_inp, svo_data)
                    
                    similarity_score = similarity_score1 if similarity_score1 > similarity_score2 else similarity_score2
                    if similarity_score > max_similarity:
                        classification = 0
                        max_similarity = similarity_score
                        max_sentence = title
                    break

        for title in reliable_news:
            for sht in satiric_shits:
                title = title.replace(sht, "")
            for subj in svo_inp['subject']:
                if subj[2] == 0:
                    continue
                words = [x.lower() for x in sentence_tokenizer.tokenize(title)]
                if subj[0] in words or singularize(subj[0]) in words:
                    tree_data = Tree(rrp.simple_parse(title))
                    svo_data = foo.getSVO(tree_data[0])
                    
                    similarity_score1 = bar.get_similarities(svo_inp, svo_data)
                    '''
                        object and subject swapped to provde more possible comparisons
                    '''
                    svo_data['subject'], svo_data['object'] = svo_data['object'], svo_data['subject']
                    similarity_score2 = bar.get_similarities(svo_inp, svo_data)

                    similarity_score = similarity_score1 if similarity_score1 > similarity_score2 else similarity_score2
                    if similarity_score > max_similarity:
                        classification = 1
                        max_similarity = similarity_score
                        max_sentence = title
                    break
        if classification == CONS_RELIABLE:
            results[str(i)] = str(max_similarity)
        elif classification == CONS_SATIRIC:
            results[str(i)] = str(-max_similarity)
        else:
            results[str(i)] = "0"
    print(json.dumps(results))


main(sys.argv[1])
