
from data_details import DataDetails

from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
sentence_tokenizer = RegexpTokenizer(r'\w+')
MIN_WORDS = 5


def process_data():
    sentence_counter = 0
    
    output = ""
    '''
        opening each raw files
    '''
    for filename in filenames.keys():
        f_read = open( "../data/debates/raw/"+filename+".txt", "r")
        
        '''
            for each line read in file
        '''
        speaker_name = "MODERATOR"
        for line in f_read:
            speaker = line[0:25].find(":")
            if  speaker != -1:
                for new_speaker  in filenames[filename]['candidates']:
                    if new_speaker in line[0:speaker]:
                        speaker_name = new_speaker
                        break 
                else:
                    speaker_name = "MODERATOR"
                
                '''
                    store sentences said by the candidates only
                '''
                if speaker_name != "MODERATOR":
                    sentences = sent_tokenize(line[speaker+1:])
                    for sentence in sentences:
                        words = sentence_tokenizer.tokenize(sentence)

                        '''
                            sentences with less than 5 words are not included
                        '''
                        if len(words) < MIN_WORDS:
                            continue

                        '''
                            interrogative sentences are not included
                        '''
                        if sentence[-1] == '?':
                            continue

                        sentence_counter = sentence_counter + 1
                        output = output + sentence + "\n" 


        f_read.close()
    return output, sentence_counter
    
# raw files written in one sentence per line
# f_write = open("../data/debates/others/sentences_with_moderators.txt", "w")

# moderator scripts are removed
# f_write = open("../data/debates/others/sentences_without_moderators.txt", "w")

# moderator scripts and sentences with less than five words are removed
# f_write = open("../data/debates/others/sentences_five_words_more.txt", "w")

# moderator scripts, sentences with less than five words, and questions are removed
# f_write = open("../data/debates/others/sentences_non_interrogative.txt", "w")

'''
    final filtering
'''
f_write = open("../data/debates/preprocessed.txt", "w")

foo = DataDetails()

'''
    files to be preprocessed including candidate names
'''
filenames = foo.filenames

'''
    words that are actions written in the transcript
'''
extras = foo.extras

processed_text, sentence_counter = process_data()
f_write.write(processed_text)
# f_write.write("TOTAL # OF SENTENCES: " + str(sentence_counter) + "\n")
f_write.close()






