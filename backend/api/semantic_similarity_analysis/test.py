''' 
	computes for the wu-palmer similarity of two words
'''

from nltk.corpus import wordnet as wn
s1 = wn.synsets('lizard')
s2 = wn.synsets('reptile')
print(s1)
print(s2)
max_similarity = 0
for synset1 in s1:
	synset_word1 = synset1.lowest_common_hypernyms(synset1, use_min_depth=False)
	for synset2 in s2:
		synset_word2 = synset1.lowest_common_hypernyms(synset2, use_min_depth=False)
		for syn1 in synset_word1:
			for syn2 in synset_word2:
				similarity = wn.wup_similarity(syn1,syn2)
				if similarity == None: 
					similarity = 0
				max_similarity = similarity if similarity > max_similarity else max_similarity
print(max_similarity)

