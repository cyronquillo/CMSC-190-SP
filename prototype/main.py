from triplet import TripletExtraction
from similarity_analysis import SemanticSimilarityAnalysis
from bllipparser import RerankingParser, Tree

def main():
    rrp = RerankingParser.fetch_and_load('WSJ-PTB3')
    foo = TripletExtraction()
    bar = SemanticSimilarityAnalysis()


    t = int(input())
    for i in range(t):    
        inp = input()
        data = input()
        tree_inp = Tree(rrp.simple_parse(inp))
        tree_data = Tree(rrp.simple_parse(data))
        svo_data = foo.getSVO(tree_data[0])
        svo_inp = foo.getSVO(tree_inp[0])
        similarity_score = bar.get_similarities(svo_inp, svo_data)
        print("\nSentence Similarity Score:",similarity_score)

if __name__ == "__main__":
    main()