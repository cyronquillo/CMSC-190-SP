from triplet import TripletExtraction
from similarity_analysis import SemanticSimilarityAnalysis
from bllipparser import RerankingParser, Tree

def main():
    CONS_MYTH = 0
    CONS_FACT = 1
    rrp = RerankingParser.fetch_and_load('WSJ-PTB3')
    foo = TripletExtraction()
    bar = SemanticSimilarityAnalysis()
    results = open('./results/result.txt', 'w')

    t = int(input())
    for i in range(t):  
        f_fact = open('./test-data/fact.txt', 'r')
        f_myth = open('./test-data/myth.txt', 'r')
        max_similarity = -1
        classification = -1  
        max_sentence = ""
        inp = input()
        tree_inp = Tree(rrp.simple_parse(inp))
        svo_inp = foo.getSVO(tree_inp[0])
        for line in f_myth:
            print(line)
            tree_data = Tree(rrp.simple_parse(line))
            svo_data = foo.getSVO(tree_data[0])
            similarity_score = bar.get_similarities(svo_inp, svo_data)
            if similarity_score > max_similarity:
                classification = 0
                max_similarity = similarity_score
                max_sentence = line

        for line in f_fact:
            print(line)    
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
        else:
            results.write("classification: MYTH -" + str(max_similarity) + "\n")
        results.write("In File: " + max_sentence + "\n\n")
        f_fact.close()
        f_myth.close()
    results.close()
if __name__ == "__main__":
    main()