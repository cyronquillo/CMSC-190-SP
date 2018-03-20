import numpy
from scipy import spatial

from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

class SemanticSimilarityAnalysis():

	def is_stopword(self, word):
		return word not in stopwords.words('english')

	def preprocess(self, word):
		'''
			removes non alpha numeric characters
		'''
		for i in word:
			if i.isdigit() == False or i.isalpha() == False:
				word.replace(i, "")
		return word.lower()

	def get_wu_palmer_similarity(self, word1, word2):
		if self.is_stopword(word1) or self.is_stopword(word2):
			return 0
		word1 = self.preprocess(word1)
		word2 = self.preprocess(word2)

		if word1 == word2:
			return 1.0
			
		max_similarity = 0

		try:
			'''
				gets the synset of each word
			'''
			synset_word1 = wn.synsets(word1)
			synset_word1 = synset_word1.lowest_common_hypernyms(synset_word1, use_min_depth=True)
			synset_word2 = wn.synsets(word2)
			synset_word2 = synset_word2.lowest_common_hypernyms(synset_word2, use_min_depth=True)

			for syn1 in synset_word1:
				for syn2 in synset_word2:
					'''
						computes for the wu-palmer similarity of each word
					'''
					similarity = wn.wup_similarity(syn1,syn2)
					if similarity == None: 
						similarity = 0
					max_similarity = similarity if similarity > max_similarity else max_similarity
			return max_similarity
		except:
			return max_similarity

	def get_numerical_similarity(self, element, wordset):
		max_similarity = 0
		for word in wordset:
			similarity = self.get_wu_palmer_similarity(element, word)
			max_similarity = similarity if similarity > max_similarity else max_similarity
			if max_similarity == 1:
				break
		return max_similarity

	def construct_vector(self, words, union_set):
		words_setify = set(words)

		vector = []
		for elem in union_set:
			sim_score = self.get_numerical_similarity(elem, words_setify)
			vector.append(sim_score)
			if sim_score == 1:
				break
		return vector

	def get_semantic_similarity(self, inp_words, data_words):
		'''
			wu-palmer similarity
		'''
		# union_set = set(inp_words).union(set(data_words))
		inp_vect = self.construct_vector(inp_words, data_words)
		return max(inp_vect)


		'''
			cosine similarity portion
		'''

		# data_vect = self.construct_vector(data_words, union_set)
		# if numpy.sum(inp_vect) == 0 or numpy.sum(data_vect) == 0:
		# 	return 0

		# cosine_similarity = 1-spatial.distance.cosine(inp_vect, data_vect)
		
		# return cosine_similarity
	def get_trunk_extras(self, words):
		trunk_list = []
		extras_list = []
		for word in words:
			if word[2] == 1:
				trunk_list.append(word[0])
			else:
				extras_list.append(word[0])
		return {'trunk' :trunk_list, 'extra' :extras_list}

	def get_similarities(self, inp, data):
		subject_similarity = -1 #initial values
		verb_similarity = -1
		object_similarity = -1

		inp_subject = self.get_trunk_extras(inp['subject']) 
		inp_verb = self.get_trunk_extras(inp['verb'])
		inp_object = self.get_trunk_extras(inp['object'])

		data_subject = self.get_trunk_extras(data['subject']) 
		data_verb = self.get_trunk_extras(data['verb'])
		data_object = self.get_trunk_extras(data['object'])

		
		# subject
		if len(inp_subject['trunk']) != 0:
			if len(data_subject['trunk']) != 0:
				subject_similarity = self.get_semantic_similarity(inp_subject['trunk'], data_subject['trunk']) 
			elif len(data_subject['extra']) != 0:
				subject_similarity = self.get_semantic_similarity(inp_subject['trunk'], data_subject['extra']) 
		elif len(inp_subject['extra']) != 0:
			if len(data_subject['trunk']) != 0:
				subject_similarity = self.get_semantic_similarity(inp_subject['extra'], data_subject['trunk']) 
			elif len(data_subject['extra']) != 0:
				subject_similarity = self.get_semantic_similarity(inp_subject['extra'], data_subject['extra']) 

		if subject_similarity < 0.90:
				return 0


		#verb
		if len(inp_verb['trunk']) != 0:
			if len(data_verb['trunk']) != 0:
				verb_similarity = self.get_semantic_similarity(inp_verb['trunk'], data_verb['trunk']) 
			elif len(data_verb['extra']) != 0:
				verb_similarity = self.get_semantic_similarity(inp_verb['trunk'], data_verb['extra']) 
		elif len(inp_verb['extra']) != 0:
			if len(data_verb['trunk']) != 0:
				verb_similarity = self.get_semantic_similarity(inp_verb['extra'], data_verb['trunk']) 
			elif len(data_verb['extra']) != 0:
				verb_similarity = self.get_semantic_similarity(inp_verb['extra'], data_verb['extra']) 
		
		#object
		if len(inp_object['trunk']) != 0:
			if len(data_object['trunk']) != 0:
				object_similarity = self.get_semantic_similarity(inp_object['trunk'], data_object['trunk']) 
			elif len(data_object['extra']) != 0:
				object_similarity = self.get_semantic_similarity(inp_object['trunk'], data_object['extra']) 
		elif len(inp_object['extra']) != 0:
			if len(data_object['trunk']) != 0:
				object_similarity = self.get_semantic_similarity(inp_object['extra'], data_object['trunk']) 
			elif len(data_object['extra']) != 0:
				object_similarity = self.get_semantic_similarity(inp_object['extra'], data_object['extra']) 
		


		'''
			custom weights of features
		'''
		feature_weight = [0.6, 0.2, 0.2]

		subject_similarity = 0 if subject_similarity == -1 else subject_similarity
		verb_similarity = 0 if verb_similarity == -1 else verb_similarity
		object_similarity = 0 if object_similarity == -1 else object_similarity
		
		
		return (subject_similarity*feature_weight[0]) + (verb_similarity*feature_weight[1]) + (object_similarity*feature_weight[2])