''' 
	computes for the wu-palmer similarity of two words
'''

from nltk.corpus import wordnet as wn
s1 = wn.synsets('love')
s2 = wn.synsets('like')
s1 = s1[0]
s2 = s2[0]
synset_word1  = s1
synset_word2  = s2
synset_word1 = synset_word1.lowest_common_hypernyms(synset_word1, use_min_depth=False)
synset_word2 = synset_word2.lowest_common_hypernyms(synset_word2, use_min_depth=False)

max_similarity = 0
for syn1 in synset_word1:
	for syn2 in synset_word2:
		similarity = wn.wup_similarity(syn1,syn2)
		if similarity == None: 
			similarity = 0
		max_similarity = similarity if similarity > max_similarity else max_similarity
print(max_similarity)