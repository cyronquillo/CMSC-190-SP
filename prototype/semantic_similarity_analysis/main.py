from triplet import TripletExtraction
from similarity_analysis import SemanticSimilarityAnalysis
from bllipparser import RerankingParser, Tree

def main():
    
    '''
        Declaration of constants and functions
    '''
    CONS_MYTH = 0
    CONS_FACT = 1
    rrp = RerankingParser.fetch_and_load('WSJ-PTB3')
    foo = TripletExtraction()
    bar = SemanticSimilarityAnalysis()


    results = open('./results/result.txt', 'w')

    t = int(input("Enter number of sentences: "))
    for i in range(t):
        max_similarity = 0
        classification = -1  
        max_sentence = ""

        '''
            2 files for comparison of input 
        '''  
        f_fact = open('./test-data/fact.txt', 'r')
        f_myth = open('./test-data/myth.txt', 'r')

        inp = input("Enter a sentence: ")

        ''' 
            generates the tree and gets the SVO of the sentence
        '''
        tree_inp = Tree(rrp.simple_parse(inp))
        svo_inp = foo.getSVO(tree_inp[0])

        '''
            comparison for f_myth and f_fact
        '''

        for line in f_myth:
            tree_data = Tree(rrp.simple_parse(line))
            svo_data = foo.getSVO(tree_data[0])
            similarity_score = bar.get_similarities(svo_inp, svo_data)
            if similarity_score > max_similarity:
                classification = 0
                max_similarity = similarity_score
                max_sentence = line

        for line in f_fact:
            tree_data = Tree(rrp.simple_parse(line))
            svo_data = foo.getSVO(tree_data[0])
            similarity_score = bar.get_similarities(svo_inp, svo_data)
            if similarity_score > max_similarity:
                classification = 1
                max_similarity = similarity_score
                max_sentence = line



        results.write("Sentence: " + inp + "\n")
        if classification == CONS_FACT:
            results.write("classification: FACT -" + str(max_similarity) + "\n")
            results.write("In File: " + max_sentence + "\n\n")
        elif classification == CONS_MYTH:
            results.write("classification: MYTH - " + str(max_similarity) + "\n")
            results.write("In File: " + max_sentence + "\n\n")
        else:
            results.write("classification: INSUFFICIENT DATA \n")
        f_fact.close()
        f_myth.close()
    results.close()
if __name__ == "__main__":
    main()