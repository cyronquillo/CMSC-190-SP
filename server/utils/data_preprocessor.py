
from config import DataDetails

from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
sentence_tokenizer = RegexpTokenizer(r'\w+')
foo = DataDetails()
MIN_WORDS = foo.min_words


def process_data():
    # raw files written in one sentence per line and extra words are removed
    # f_write = open("../data/debates/others/sentences_with_moderators.txt", "w")

    # moderator scripts and extra words are removed
    # f_write = open("../data/debates/others/sentences_without_moderators.txt", "w")

    # moderator scripts, extra words, and sentences with less than five words are removed
    # f_write = open("../data/debates/others/sentences_five_words_more.txt", "w")

    # moderator scripts, extra words, sentences with less than five words, and questions are removed
    # f_write = open("../data/debates/others/sentences_non_interrogative.txt", "w")


    '''
        final filtering (included sentences with > 5 words)
    '''
    f_write = open("../data/debates/preprocessed.txt", "w")

    

    '''
        files to be preprocessed including candidate names
    '''
    filenames = foo.filenames

    '''
        words that are actions written in the transcript
    '''
    extras = foo.extras
    sentence_counter = 0
    
    output = ""
    '''
        opening each raw files
    '''
    for filename in filenames.keys():
        f_read = open( "../data/debates/raw/"+filename+".txt", "r")
        print("file:", filename)
        '''
            for each line read in file
        '''
        speaker_name = "MODERATOR"
        for line in f_read:

            speaker = line[0:25].find(":")

            '''
                checks for change in speaker
            '''
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
                '''
                    removes the crowd reactions and other extra words enclosed in [], ()
                '''
                for extra in extras:
                    line = line.replace(extra, '')
                sentences = sent_tokenize(line[speaker+1:])
                for sentence in sentences:
                    words = sentence_tokenizer.tokenize(sentence)

                    '''
                        sentences with less than 5 words are not included
                    '''
                    if len(words) <= MIN_WORDS:
                        continue

                    '''
                        interrogative sentences are not included
                    '''
                    if sentence[-1] == '?':
                        continue

                    sentence_counter = sentence_counter + 1

                    if sentence[-1] not in ['.', '!']:
                        sentence = sentence + '.'
                    output = output + sentence + "\n" 

        f_read.close()
    f_write.write(output)
    f_write.write("TOTAL # OF SENTENCES: " + str(sentence_counter) + "\n")
    f_write.close()


process_data()
