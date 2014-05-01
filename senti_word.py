import string
from nltk.stem.wordnet import WordNetLemmatizer
import pickle
import urllib2
import json
import re
from nltk.corpus import words as nltk_words
import pickle
from multiprocessing import Pool

emoticon_dict = dict()
senti_word_dict = dict()
### Here the file_name is the name of the file for which you want to run the preprocessing.
### file_name is the raw tweet file captures.
#file_name = raw_input('Enter filename: ')
#file_name = 'Divergent.txt'
#file_name = 'zanjeer.txt'
#file_name = 'DIv_new.txt'
#file_name = 'highway_tweets.txt'
#file_name = 'rockstar_tweets.txt'
file_name = 'dark_knight_rises_tweets.txt'
lmtzr = WordNetLemmatizer()
#senti_word_dict = dict()
result_list = []
processed_text =''
def initialize():
    for line in open('emoticon.txt').read().splitlines():
        fields = line.split(' - ')
        emoticon_dict[fields[0]] = fields[1]
    global senti_word_dict
    with open('senti_word_final.txt', 'rb') as f:
        senti_word_dict= pickle.load(f)

def process_emoticon(line):
    words = line.split()
    new_list = []
    for word in words:
        if word in emoticon_dict:
            new_word = emoticon_dict[word]
            new_list.append(new_word)
        else:
            new_list.append(word)
    new_line = ' '.join(new_list)
    return new_line


def get_slang_equivalent(query):
    urbandictionary = 'http://api.urbandictionary.com/v0/define?term='
    url = urbandictionary+query
    try:
        r = urllib2.urlopen(url)
        if r:
            data = json.loads(r.read())
            if data['tags']:
                return data['tags']
    except:
        return []


def process_slangs(line):
    line = process_emoticon(line)
    line = re.sub('\.+', '.', line )
    line = re.sub('(\w+:\/\/\S+)', '', line)
    #words = re.findall('[a-zA-Z._]+', line.lower())
    new_word_list = []
    '''
    for word in words:
        word = re.sub(r'(.)\1+', r'\1\1\1',word)
        word = lmtzr.lemmatize(word, 'v')
        new_word_list.append(word)
    #print ' '.join(new_word_list)
    '''

    global full_stop
    #global question
    #full_stop = 0
    question= 0
    words = re.findall('[a-zA-Z.@#_]+', line.lower())
    new_list = []
    for word in words:
        full_stop = 0
        end = ''
        #print word
        if word.find('@') != -1 or word.find('#') != -1 or word == '.':
            new_word = word
        else:
            if word.find('.') != -1:
                word = word.split('.')[0]
                full_stop = 1
                end = '.'
            '''
        elif word.find('?') != -1:
            word = word.split('?')[0]
            question = 1
            end = '?'
            '''
            word = lmtzr.lemmatize(word, 'v')
            if word not in nltk_words.words() and word not in senti_word_dict:
                #print word
                word = re.sub(r'(.)\1+', r'\1\1\1',word)
                equiv_list = get_slang_equivalent(word)
                #print equiv_list
                if not equiv_list:
                    new_word = word + end
                    #continue
                else:
                    new_word = equiv_list[0] + end

                '''
                for each_word in equiv_list:
                    #print each_word
                    if each_word in senti_word_dict:
                        new_word = each_word + end
                        break
                '''

            else:
                new_word = word + end
        new_list.append(new_word)
        #print new_list
    #result_list.append(' '.join(new_list))
    global processed_text
    processed_text += ' '.join(new_list) + '\n'
    print ' '.join(new_list)
        #return ' '.join(new_list)


def process_lematization(line):
    new_line = ' '
    for word in line.split():
        print word
        new_line += ' ' + lmtzr.lemmatize(word)
    print new_line

if __name__ == "__main__":
    initialize()
    #pool = Pool(4)
    #with open(file_name) as source_file:
        # chunk the work into batches of 4 lines at a time
        #results = pool.map(process_slangs, source_file, 4)

        #print results
    for line in open(file_name).read().splitlines():
        process_slangs(line)
    print processed_text
    with open('processed.txt', 'wb') as f:
        pickle.dump(processed_text, f)
        ## Dumping the content




