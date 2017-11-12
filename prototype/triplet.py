import nltk
import numpy
# import os
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import RegexpTokenizer
from bllipparser import RerankingParser, Tree
import math

class TripletExtraction():    
    def getSubject(self, subjects):
        subject_tokens = []

        for subject in subjects:
            if "PRP" in subject[1] or "NN" in subject[1]:
                subject_tokens.append([subject[0].lower(), subject[1] , 1])
            
            else:
                subject_tokens.append([subject[0].lower(), subject[1], 0])
        return subject_tokens

    def getObject(self, obj):
        object_tokens = []
        if obj.label in ["NP", "PP"]:
            tag = "NN"
        else:
            tag = "JJ"

        for subtree in obj.all_subtrees():
            if subtree.is_preterminal():
                elem = [subtree.token.lower(),(subtree.tags())[0],0]
                if tag in subtree.label:
                    elem[2] = 1             
                if elem not in object_tokens:
                    object_tokens.append(elem)
        return object_tokens

    def isActive(self, svo):

        for obj in svo['object']:
            if obj[0] == "by":
                return False
        vbn_flag = False
        be_flag = False
        is_flag = False
        for verb in svo['verb']:
            if verb[1] == "VBN":
                vbn_flag = True
            if verb[0] in ["be", "been", "being"]:
                be_flag = True
            if verb[0] in ["is", "are", "was", "were"]:
                is_flag = True
        if vbn_flag and (be_flag or is_flag):
            return False
        return True

    def getSVO(self, tree):
        verb = []
        objec = []
        misc = []
        object_flag = False

        for subtree in tree:
            if "NP" in subtree.label:
                subject = self.getSubject(subtree.tokens_and_tags())
            elif subtree.label == "VP":
                vp_subtree = subtree
                break
            else:
                misc.append(subtree.tokens())

        for subtree in vp_subtree.all_subtrees(): # constructs all the subtrees in the remaining words
            if not object_flag:
                if subtree.is_preterminal(): #checks if the node is a terminal node
                    verb.append([subtree.token.lower(),(subtree.tags())[0],0])
                    if "VB" in subtree.label and subtree.token.lower() not in stopwords.words('english'):
                        verb[len(verb)-1][2] = 1
                if subtree.label in ["NP", "PP", "ADJP"]:
                    object_flag = True
            if object_flag:
                if subtree.label in ["NP", "PP", "ADJP"]:
                    objec = self.getObject(subtree)
        
        svo_inp = {'subject': subject, 'verb': verb, 'object': objec, 'misc': misc}
        
        if not self.isActive(svo_inp):
            svo_inp['subject'], svo_inp['object'] = svo_inp['object'] , svo_inp['subject'] 
        
        return svo_inp 
