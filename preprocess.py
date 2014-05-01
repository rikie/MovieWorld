__author__ = 'Arijit'

import string
import pickle
import urllib2
import json

emoticon_dict = dict()
senti_word_dict = dict()

def initialize():
    for line in open('emoticon.txt').read().splitlines():
        fields = line.split(' - ')
        emoticon_dict[fields[0]] = fields[1]


def process_emoticon(line):
    for emoticon in emoticon_dict:
        line = string.replace(line, emoticon, emoticon_dict[emoticon])
    print line
    return line


def process_senti():
    word_count = dict()
    for line in open('sentiword.txt').read().splitlines():
        fields = line.split()
        #print fields
        pos_score = float(fields[2])
        neg_score = float(fields[3])
        for field in fields:
            if '#' in field:
                word = field.split('#')[0]
                if word not in senti_word_dict:
                    senti_word_dict[word] = (pos_score, neg_score)
                    word_count[word] = 1
                else:
                    senti_word_dict[word] = ((senti_word_dict[word][0] + pos_score), (senti_word_dict[word][1] + neg_score))
                    word_count[word] += 1


    for word in senti_word_dict:
        senti_word_dict[word] = (senti_word_dict[word][0]/word_count[word], senti_word_dict[word][1]/word_count[word])

    #print 'cool', senti_word_dict['cool']
def search_urbandictionary(query):
    #query = '\"' + query + '\"'
    query = query.replace(' ', '%20')
    print query
    urbandictionary = 'http://api.urbandictionary.com/v0/define?term='
    url = urbandictionary+query
    #print url
    r = urllib2.urlopen(url)
    if r:
        data = json.loads(r.read())
        if data['tags']:
            #print 'tags', data['tags'][0:5]
            return data['tags']
            #return data['tags'][0:5]


def process_slangs():

    with open('root_seed.txt', 'rb') as f:
        root_seed = pickle.load(f)
    processed_words = list()

    #root_seed = ['yolo']
    #root_seed = ['13th floor']

    while root_seed:
        word_to_process = root_seed.pop()
        if word_to_process not in senti_word_dict:
            word_to_process = word_to_process.encode('utf-8')
            tags = search_urbandictionary(word_to_process)
            if not tags:
                continue
            print tags
            pos_score = 0.0
            neg_score = 0.0
            count = 0
            for tag in tags:
                if tag in senti_word_dict:
                    print tag
                    pos_score += senti_word_dict[tag][0]
                    neg_score += senti_word_dict[tag][1]
                    count += 1
                if tag not in processed_words and tag not in root_seed:
                    root_seed.append(tag)
            senti_word_dict[word_to_process] = (pos_score/count, neg_score/count)
            #print pos_score
            processed_words.append(word_to_process)
            #print root_seed
    #print processed_words
    #req_pos = sorted(senti_word_dict.iteritems(), key=lambda (k, v): (-v, k))[:2]
    #print 'hello'




initialize()
process_senti()
process_slangs()
with open('senti_word_final.txt', 'wb') as f:
    pickle.dump(senti_word_dict, f)


#process_emoticon('hello :(')
#print emoticon_dict
