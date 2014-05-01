import nltk
from numpy import * 
from sympy import * 
from scipy.optimize import minimize
from subprocess import Popen, PIPE
import re
import subprocess
import os
import pickle
import xml.etree.cElementTree as ET
import GetFeatures as gf

# list of words with positive and negative scores
# word : tuple(positive,negative)
#-----------------------------------------------------------
movieName = "meinterahero"
#-----------------------------------------------------------
senti_words = {}
# This has to be updated as per the movie --- being done manually till now
list_of_related_terms = ["movie","story","script","plot","music","songs","song","lyrics","songs","direction","director","cinematography","edit","scene",'meinterahero','varun','varundhawan','dhawan','films','actors','storyline','direction','script','movie','tom', 'cruise', 'tomcruise', 'leonardo', 'dicaprio', 'leodicaprio', 'johnny', 'depp', 'johnnydepp', 'brad', 'pitt', 'bradpitt', 'matt', 'damon', 'mattdamon', 'adam', 'sandler', 'adamsandler', 'dwayne', 'johnson', 'dwanejohnson2', 'dwanejohnson', 'rock', 'ben', 'stiller', 'benstiller', 'redhourben', 'benstiller', 'sacha', 'baron', 'cohen', 'sachabaron', 'sachabaroncohen', 'will', 'smith', 'willsmith', 'mark', 'wahlberg', 'mark_wahlberg', 'markwahlberg', 'robert', 'pattinson', 'robertpattinson', 'taylorlautner', 'taylor', 'lautner', 'jude', 'law', 'judehlaw', 'bradley', 'cooper', 'bradleycooper', 'tom', 'hanks', 'tomhanks', 'chris', 'evans', 'chrisevans', 'sebastian', 'stan', 'sebastianstan', 'theo', 'james', 'theojames', 'sylvesterstallone', 'sylvester', 'stallone', 'theslystallone', 'jason', 'statham', 'jasonstatham', 'jet', 'li', 'jetli', 'russell', 'crowe', 'russellcrowe', 'anthony', 'hopkins', 'anthonyhopkins', 'patrickstewart', 'patrick', 'stewart', 'sirpatstew', 'ian', 'mckellen', 'ianmckellen', 'hugh', 'jackman', 'hugh', 'jackman', 'realhughjackman', 'ralph', 'fiennes', 'ralphfiennes', 'f. murray abraham', 'mathieu', 'amalric', 'mathieuamalric', 'andrew', 'garfield', 'andrewgarfield', 'emma', 'stone', 'emmastone', 'jamie', 'foxx', 'jamiefoxx', 'kellan', 'lutz', 'kellanlutz', 'gaia,weiss', 'gaiaweiss_', 'scott,adkins', 'thescottadkins', 'analeigh', 'tipton', 'ohanaleigh', 'morganfreeman', 'morganfreeman', 'aaron', 'paul', 'aaronpaul_8', 'jesse', 'eisenberg', 'jesseeisenberg', 'jemaine', 'clement', 'jemaineclement', 'amir', 'khan', 'amirkhan', 'salmankhan', 'salman', 'beingsalmankhan', 'shahrukhkhan', 'shahrukh', 'iamsrk', 'hrithik', 'roshan', 'ihrithik', 'abhishek', 'bacchan', 'juniorbachchan', 'ranbir', 'kapoor', 'ranbirkapoor', 'ranveer', 'singh', 'ranveerofficial', 'shahid', 'kapoor', 'shahidkapoor', 'imrankhan', 'imran', 'akshay', 'kumar', 'akshaykumar', 'ajaydevgan', 'ajay', 'devgan', 'imran', 'hashmi', 'imranhashmi', 'amitabh', 'bacchan', 'srbachchan', 'sanjay', 'dutt', 'duttsanjay', 'john', 'abraham', 'thejohnabraham', 'saif', 'ali', 'khan', 'saifalikhan', 'angelina', 'jolie', 'angelinajolie', 'juliaroberts', 'julia', 'roberts', 'jenniferlawrence', 'jennifer', 'lawrence', 'nicole', 'kidman', 'nicolekidman', 'milakunis', 'milakunis', 'jennifer', 'aniston', 'jenniferaniston', 'cameron', 'diaz', 'camerondiaz', 'anne', 'hathaway', 'annehathaway', 'scarlett', 'johansson', 'scarlettjohansson', 'jessica', 'alba', 'jessicaalba', 'kristen', 'stewart', 'kristenstewart', 'emmastone', 'emma', 'stone', 'charlize', 'theron', 'charlizetheron', 'sandrabullock', 'sandra', 'bullock', 'natalieportman', 'natalie', 'portman', 'marion', 'cotillard', 'marioncotillard', 'shailene', 'woodley', 'shailenewoodley', 'kate', 'winslet', 'katewinslet', 'jenniferconnelly', 'jenniferconnelly', 'megan', 'fox', 'meganfox', 'deepika', 'padukone', 'deepikapadukone', 'katrinakaif', 'katrina', 'kaif', 'vidhyabalan', 'vidhyabalan', 'priyanka', 'chopra', 'priyankachopra', 'parineeti', 'chopra', 'parineetichopra', 'kangana', 'ranaut', 'kanganaranaut', 'nargis', 'fakhri', 'nargisfakhri', 'shraddha', 'kapoor', 'shraddhakapoor', 'sonakshi', 'sinha', 'sonakshisinha', 'kareenakapoor', 'kareena', 'kapoor', 'alia', 'bhatt', 'aliabhatt', 'alia08', 'acting', 'act', 'actor', 'actress', 'acted', 'performance','arjun','arjunkapoor'] # list of terms related to movies
depen = {}
sentence_POS = {} # parts of speech of each word in a sentence
negations = {} # list o
cons_nodes = {} # mane : score [edges] [frequency]
incons_nodes = {} # mane : score [edges] [frequency]
list_contrasting_conjunctions = ["but","however","nonetheless","yet","even_so","nevertheless","still","notwithstanding","although","though","even_though","notwithstanding","despite","in_spite_of","for_all","regardless_of"]
list_noncontrasting_conjunctions = ["and","so"]
initial_nodes = {} # name: value = 1/variable = 0,value/variable
summing = 0

def getSimilarWords (word):
    
    f1 = open('C:\IRProject\dictionary.bat','w')
    f1.write("@ECHO OFF");
    f1.write('\n')
    f1.write("C:\IRProject\\bin\wget.exe -qO- http://dictionary.reference.com/browse/"+word+"?s=t | findstr \"data-syllable\"");
    f1.close()
    stdout = Popen('C:\IRProject\dictionary.bat', shell=True, stdout=PIPE).stdout
    output = stdout.read()

    f = open('C:\IRProject\dictionary.txt','w')
    f.write(output)
    f.close()
    f = open('C:\IRProject\dictionary.txt')
    lines = f.readlines()
    f.close()
    word_POS = {}
    #print len(lines)
    if len(lines) >= 2  :
        x = lines[1].replace(" ", "")
        s = re.split('<|>|=',x)
        count = 0
        for i in s :
            if i == "\"secondary-bf\"data-syllable" :
                word_POS[s[count+2].split(",")[0]] = s[count+7]
            count = count + 1
        return word_POS
    else :
        return word_POS

# it returns score
def getsomeadj (word):
    list_of_words = []
    if len(getSimilarWords(word)) == 0 and not (sentence_POS[word] == "NN" or sentence_POS[word] == "NNS" or sentence_POS[word] == "JJ" or sentence_POS[word] == "JJR" or sentence_POS[word] == "JJS" or sentence_POS[word] == "RB" or sentence_POS[word] == "RBR" or sentence_POS[word] == "RBS" or sentence_POS[word] == "VBP"):
    #if len(getSimilarWords(word)) == 0 and not (sentence_POS[word] == "JJ" or sentence_POS[word] == "JJR" or sentence_POS[word] == "JJS" or sentence_POS[word] == "RB" or sentence_POS[word] == "RBR" or sentence_POS[word] == "RBS" or sentence_POS[word] == "VBP"):
        return "-999"
    i = word
    if i in senti_words :
        if senti_words[i][0] == 0 and senti_words[i][1] != 0:
            senti_words[word] = (1-0.5 -(senti_words[i][1]/2.0),0.5+(senti_words[i][1]/2.0))
        if senti_words[i][1] == 0 and senti_words[i][0] != 0:
            senti_words[word] = (0.5+(senti_words[i][0]/2.0),1-0.5-(senti_words[i][0]/2.0)) 
        if senti_words[i][1] == 0 and senti_words[i][0] == 0:
            senti_words[word] = (0.5,0.5)   
        if senti_words[i][1] != 0 and senti_words[i][0] != 0:
            if senti_words[i][1] + senti_words[i][0] != 1 :
                senti_words[word] = (senti_words[i][0]/(senti_words[i][0]+senti_words[i][1]),senti_words[i][1]/(senti_words[i][0] + senti_words[i][1]))
            else :
                senti_words[word] =  senti_words[i]
        return senti_words[word]
    for i in getSimilarWords(word) :
        list_of_words.append(i)
    list_of_words.append(word)
    flag = 0
    for i in list_of_words :
        if i[0] == word[0] and not (("less" in i and "less" not in word) or ("less" in word and "less" not in i)):
            if i in senti_words :
                flag = 1
                if senti_words[i][0] == 0 and senti_words[i][1] != 0:
                    senti_words[word] = (1-senti_words[i][1],senti_words[i][1])
                if senti_words[i][1] == 0 and senti_words[i][0] != 0:
                    senti_words[word] = (senti_words[i][0],1-senti_words[i][0]) 
                if senti_words[i][1] == 0 and senti_words[i][0] == 0:
                    senti_words[word] = (0.5,0.5)   
                if senti_words[i][1] != 0 and senti_words[i][0] != 0:
                    if senti_words[i][1] + senti_words[i][0] != 1 :
                        diff = abs(senti_words[i][1] - senti_words[i][0])/2.0
                        senti_words[word] = (senti_words[i][0] + diff,senti_words[i][1] + diff)
                    else :
                        senti_words[word] =  senti_words[i]
    if flag == 1 :
        return senti_words[word]
    else :
        return "-999"
                
# word position : word, {position,word}
# based on dependencies in nlp stanford
def dependencies(sentence) :
    os.popen("echo "+sentence+" > C:\IRProject\stanfordtemp.txt")
    stdout = Popen('C:\IRProject\god.bat', shell=True, stdout=PIPE).stdout
    output = stdout.read()
    output1 = re.findall(r"[\w']+", output)
    #print output1
    sentence_split = sentence.split(".")[0].split()
    count1 = 0
    count = 0
    for s in sentence_split :
        depen[count1] = [s,{}]
        for o in range(count,len(output1)) :
            if output1[o] == s:
                break
            count = count + 1
        count1 = count1 + 1
    count = count + 1
    for o in range(0,count) :
        if output1[o] in sentence_split :
            sentence_POS[output1[o]] = output1[o-1]
    for o in xrange(count,len(output1)-1,5) :
        if output1[o] != "root" :
            if output1[o] == "neg" :
                negations[int(output1[o+2])-1] = output1[o+1]
            try :
                depen.get(int(output1[o+2])-1)[1][int(output1[o+4])-1] = output1[o+3]
                depen.get(int(output1[o+4])-1)[1][int(output1[o+2])-1] = output1[o+1]
            except :
                return {}
    return depen

def getNounAdj(noun,position) :
    setone = {}
    settwo = {}
    setthree = {}
    answer = {}
    setone[position] = noun
    settwo = depen.get(position)[1]
    for j in depen.get(position)[1] :
        if j not in setone :
            if getsomeadj(depen.get(j)[0]) != "-999" :
                answer[depen.get(j)[0]] =  getsomeadj(depen.get(j)[0])
            else :
                answer[depen.get(j)[0]] = (0.5,0.5)
    while len(settwo) != 0:
        for i in settwo:
            if i not in setone :
                setone[i] = depen.get(i)[0]
                for j in depen.get(i)[1] :
                    if j not in setone :
                        if getsomeadj(depen.get(j)[0]) != "-999" :
                            answer[depen.get(j)[0]] =  getsomeadj(depen.get(j)[0])
                        else :
                            answer[depen.get(j)[0]] = (0.5,0.5)
                        setthree[j] = depen.get(i)[1].get(j)
        settwo = setthree
        setthree = {}
    return answer
    

# returns position of a noun in a sentence and all its describing words are
# {position_noun : [name,{adj : (scores)}]}
def check_noun(sentence) :
    os.popen("echo "+sentence+" > C:\IRProject\stanfordtemp.txt")
    stdout = Popen('C:\IRProject\god.bat', shell=True, stdout=PIPE).stdout
    output = stdout.read()
    output1 = re.findall(r"[\w']+", output)
    words = sentence.split(".")[0].split() 
    count = 0
    sent_position = 0
    answer = {}
    for s in words :
        for o in range(count+1,len(output1)) :
            if output1[o] != "ROOT" and s == output1[o]:
                if output1[o-1] == "NN" or output1[o-1] == "NNS" :
                    if s in list_of_related_terms :
                        adj = getNounAdj(s,sent_position)
                        answer[sent_position] =  [s,adj]
                if output1[o-1] == "NNP" or output1[o-1] == "NNPS" :
                        adj = getNounAdj(s,sent_position)
                        answer[sent_position] =  [s,adj]
                count = count+1
                break
            count = count+1
        sent_position = sent_position + 1
     
    return answer

# dict_describing_noun is a list of dict for each sentence. position : word ,{describing word,position}
def selections(sentence) :
    for noun in sentence :
        new_dict = {}
        for adj in sentence.get(noun)[1] :
            if adj in senti_words or sentence_POS[adj] == "NN" or sentence_POS[adj] == "NNS" or sentence_POS[adj] == "JJ" or sentence_POS[adj] == "JJR" or sentence_POS[adj] == "JJS" or sentence_POS[adj] == "RB" or sentence_POS[adj] == "RBR" or sentence_POS[adj] == "RBS" or sentence_POS[adj] == "VBP":
            #if adj in senti_words or sentence_POS[adj] == "JJ" or sentence_POS[adj] == "JJR" or sentence_POS[adj] == "JJS" or sentence_POS[adj] == "RB" or sentence_POS[adj] == "RBR" or sentence_POS[adj] == "RBS" or sentence_POS[adj] == "VBP":
                new_dict[adj] = sentence.get(noun)[1][adj]
        sentence.get(noun)[1] = new_dict
    return sentence 
      
def nodeCalculations(dict_adj_scores,sentence) :
    list_of_adj = {}
    for noun in dict_adj_scores :
        for adj in dict_adj_scores.get(noun)[1] :
            list_of_adj[adj] = dict_adj_scores.get(noun)[1].get(adj)
    # adding to nodes
    for i in list_of_adj :
        if i not in cons_nodes :
            cons_nodes[i] = [list_of_adj.get(i),[],[]]
            incons_nodes[i] = [list_of_adj.get(i),[],[]]
    words = sentence.split()
    con_conjunctions = {}
    noncon_conjunctions = {}
    required_words = {}
    count = 0
    for w in words :
        if w in list_contrasting_conjunctions :
            con_conjunctions[count] = w
        if w in list_noncontrasting_conjunctions :
            noncon_conjunctions[count] = w
        if w in list_of_adj :
            required_words[count] = w
        count = count + 1
    if len(required_words) >= 2 :
        for w in noncon_conjunctions :
            for i in range(0,len(required_words)-1) :
                for j in range(i+1,len(required_words)) :
                    if required_words.keys()[i] < w and w < required_words.keys()[j] :
                        if required_words.keys()[i] not in negations and required_words.keys()[j] not in negations:
                            if required_words.get(required_words.keys()[j]) in cons_nodes.get(required_words.get(required_words.keys()[i]))[1] :
                                cons_nodes.get(required_words.get(required_words.keys()[i]))[2][cons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] = cons_nodes.get(required_words.get(required_words.keys()[i]))[2][cons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] + 1
                                cons_nodes.get(required_words.get(required_words.keys()[j]))[2][cons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] = cons_nodes.get(required_words.get(required_words.keys()[j]))[2][cons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] + 1
                            else :
                                cons_nodes.get(required_words.get(required_words.keys()[i]))[1].append(required_words.get(required_words.keys()[j]))
                                cons_nodes.get(required_words.get(required_words.keys()[i]))[2].append(1) 
                                cons_nodes.get(required_words.get(required_words.keys()[j]))[1].append(required_words.get(required_words.keys()[i]))
                                cons_nodes.get(required_words.get(required_words.keys()[j]))[2].append(1) 
                        if required_words.keys()[i] in negations and required_words.keys()[j] not in negations:
                            if required_words.get(required_words.keys()[j]) in incons_nodes.get(required_words.get(required_words.keys()[i]))[1] :
                                incons_nodes.get(required_words.get(required_words.keys()[i]))[2][incons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] = incons_nodes.get(required_words.get(required_words.keys()[i]))[2][incons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] + 1
                                incons_nodes.get(required_words.get(required_words.keys()[j]))[2][incons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] = incons_nodes.get(required_words.get(required_words.keys()[j]))[2][incons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] + 1
                            else :
                                incons_nodes.get(required_words.get(required_words.keys()[i]))[1].append(required_words.get(required_words.keys()[j]))
                                incons_nodes.get(required_words.get(required_words.keys()[i]))[2].append(1) 
                                incons_nodes.get(required_words.get(required_words.keys()[j]))[1].append(required_words.get(required_words.keys()[i]))
                                incons_nodes.get(required_words.get(required_words.keys()[j]))[2].append(1)
                        if required_words.keys()[i] not in negations and required_words.keys()[j] in negations:
                            if required_words.get(required_words.keys()[j]) in incons_nodes.get(required_words.get(required_words.keys()[i]))[1] :
                                incons_nodes.get(required_words.get(required_words.keys()[i]))[2][incons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] = incons_nodes.get(required_words.get(required_words.keys()[i]))[2][incons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] + 1
                                incons_nodes.get(required_words.get(required_words.keys()[j]))[2][incons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] = incons_nodes.get(required_words.get(required_words.keys()[j]))[2][incons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] + 1
                            else :
                                incons_nodes.get(required_words.get(required_words.keys()[i]))[1].append(required_words.get(required_words.keys()[j]))
                                incons_nodes.get(required_words.get(required_words.keys()[i]))[2].append(1) 
                                incons_nodes.get(required_words.get(required_words.keys()[j]))[1].append(required_words.get(required_words.keys()[i]))
                                incons_nodes.get(required_words.get(required_words.keys()[j]))[2].append(1)
                        if required_words.keys()[i] in negations and required_words.keys()[j] in negations:
                            if required_words.get(required_words.keys()[j]) in cons_nodes.get(required_words.get(required_words.keys()[i]))[1] :
                                cons_nodes.get(required_words.get(required_words.keys()[i]))[2][cons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] = cons_nodes.get(required_words.get(required_words.keys()[i]))[2][cons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] + 1
                                cons_nodes.get(required_words.get(required_words.keys()[j]))[2][cons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] = cons_nodes.get(required_words.get(required_words.keys()[j]))[2][cons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] + 1
                            else :
                                cons_nodes.get(required_words.get(required_words.keys()[i]))[1].append(required_words.get(required_words.keys()[j]))
                                cons_nodes.get(required_words.get(required_words.keys()[i]))[2].append(1) 
                                cons_nodes.get(required_words.get(required_words.keys()[j]))[1].append(required_words.get(required_words.keys()[i]))
                                cons_nodes.get(required_words.get(required_words.keys()[j]))[2].append(1) 
        for w in con_conjunctions :
            for i in range(0,len(required_words)-1) :
                for j in range(i+1,len(required_words)) :
                    if required_words.keys()[i] < w and w < required_words.keys()[j] :
                        if required_words.keys()[i] in negations and required_words.keys()[j] not in negations:
                            if required_words.get(required_words.keys()[j]) in cons_nodes.get(required_words.get(required_words.keys()[i]))[1] :
                                cons_nodes.get(required_words.get(required_words.keys()[i]))[2][cons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] = cons_nodes.get(required_words.get(required_words.keys()[i]))[2][cons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] + 1
                                cons_nodes.get(required_words.get(required_words.keys()[j]))[2][cons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] = cons_nodes.get(required_words.get(required_words.keys()[j]))[2][cons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] + 1
                            else :
                                cons_nodes.get(required_words.get(required_words.keys()[i]))[1].append(required_words.get(required_words.keys()[j]))
                                cons_nodes.get(required_words.get(required_words.keys()[i]))[2].append(1) 
                                cons_nodes.get(required_words.get(required_words.keys()[j]))[1].append(required_words.get(required_words.keys()[i]))
                                cons_nodes.get(required_words.get(required_words.keys()[j]))[2].append(1) 
                        if required_words.keys()[i] not in negations and required_words.keys()[j] not in negations:
                            if required_words.get(required_words.keys()[j]) in incons_nodes.get(required_words.get(required_words.keys()[i]))[1] :
                                incons_nodes.get(required_words.get(required_words.keys()[i]))[2][incons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] = incons_nodes.get(required_words.get(required_words.keys()[i]))[2][incons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] + 1
                                incons_nodes.get(required_words.get(required_words.keys()[j]))[2][incons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] = incons_nodes.get(required_words.get(required_words.keys()[j]))[2][incons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] + 1
                            else :
                                incons_nodes.get(required_words.get(required_words.keys()[i]))[1].append(required_words.get(required_words.keys()[j]))
                                incons_nodes.get(required_words.get(required_words.keys()[i]))[2].append(1) 
                                incons_nodes.get(required_words.get(required_words.keys()[j]))[1].append(required_words.get(required_words.keys()[i]))
                                incons_nodes.get(required_words.get(required_words.keys()[j]))[2].append(1)
                        if required_words.keys()[i] in negations and required_words.keys()[j] in negations:
                            if required_words.get(required_words.keys()[j]) in incons_nodes.get(required_words.get(required_words.keys()[i]))[1] :
                                incons_nodes.get(required_words.get(required_words.keys()[i]))[2][incons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] = incons_nodes.get(required_words.get(required_words.keys()[i]))[2][incons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] + 1
                                incons_nodes.get(required_words.get(required_words.keys()[j]))[2][incons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] = incons_nodes.get(required_words.get(required_words.keys()[j]))[2][incons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] + 1
                            else :
                                incons_nodes.get(required_words.get(required_words.keys()[i]))[1].append(required_words.get(required_words.keys()[j]))
                                incons_nodes.get(required_words.get(required_words.keys()[i]))[2].append(1) 
                                incons_nodes.get(required_words.get(required_words.keys()[j]))[1].append(required_words.get(required_words.keys()[i]))
                                incons_nodes.get(required_words.get(required_words.keys()[j]))[2].append(1)
                        if required_words.keys()[i] not in negations and required_words.keys()[j] in negations:
                            if required_words.get(required_words.keys()[j]) in cons_nodes.get(required_words.get(required_words.keys()[i]))[1] :
                                cons_nodes.get(required_words.get(required_words.keys()[i]))[2][cons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] = cons_nodes.get(required_words.get(required_words.keys()[i]))[2][cons_nodes.get(required_words.get(required_words.keys()[i]))[1].index(required_words.get(required_words.keys()[j]))] + 1
                                cons_nodes.get(required_words.get(required_words.keys()[j]))[2][cons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] = cons_nodes.get(required_words.get(required_words.keys()[j]))[2][cons_nodes.get(required_words.get(required_words.keys()[j]))[1].index(required_words.get(required_words.keys()[i]))] + 1
                            else :
                                cons_nodes.get(required_words.get(required_words.keys()[i]))[1].append(required_words.get(required_words.keys()[j]))
                                cons_nodes.get(required_words.get(required_words.keys()[i]))[2].append(1) 
                                cons_nodes.get(required_words.get(required_words.keys()[j]))[1].append(required_words.get(required_words.keys()[i]))
                                cons_nodes.get(required_words.get(required_words.keys()[j]))[2].append(1)
                              
def func(x) :
    count = 0
    for n in initial_nodes :
       if initial_nodes.get(n)[0] == 0 :
           initial_nodes.get(n)[1] = (x[count])
           count = count + 1
    summing = 0
    for i in cons_nodes :
        for j in cons_nodes.get(i)[1] :
            try :
                summing = summing + cons_nodes.get(i)[2][cons_nodes.get(i)[1].index(j)]*(initial_nodes.get(i)[1] + initial_nodes.get(j)[1] + 2*initial_nodes.get(i)[1]*initial_nodes.get(j)[1])*(initial_nodes.get(i)[1] + initial_nodes.get(j)[1] + 2*initial_nodes.get(i)[1]*initial_nodes.get(j)[1])
            except :
                summing = summing + 0
    for i in incons_nodes :
        for j in incons_nodes.get(i)[1] :
            try :
                summing = summing + incons_nodes.get(i)[2][incons_nodes.get(i)[1].index(j)]*(1-initial_nodes.get(i)[1] - initial_nodes.get(j)[1] + 2*initial_nodes.get(i)[1]*initial_nodes.get(j)[1])*(1 - initial_nodes.get(i)[1] - initial_nodes.get(j)[1] + 2*initial_nodes.get(i)[1]*initial_nodes.get(j)[1])
            except :
                summing = summing + 0
    #func(x)
    return summing/2.0
    
def initialization() :
    count = 0
    for n in cons_nodes :
        if cons_nodes.get(n)[0][0] > 0.7 or (cons_nodes.get(n)[0][0] < 0.3 and cons_nodes.get(n)[0][0] > 0):
            initial_nodes[n] = [1,cons_nodes.get(n)[0][0]]
        else :
            initial_nodes[n] = [0,0]
            count = count + 1
    x = [Symbol('x[%d]'%n) for n in range(count)] 
#     count = 0
#     for n in initial_nodes :
#         if initial_nodes.get(n)[0] == 0 :
#             initial_nodes.get(n).append(x[count])
#             count = count + 1
#     print initial_nodes
    bounds1 = []
    initial = []
    for i in x :
        bounds1.append((0,1))
        initial.append(0.5)
    bounds1 = tuple(bounds1)
    initial = tuple(initial)
    global summing
    summing = 0
#     for i in cons_nodes :
#         for j in cons_nodes.get(i)[1] :
#             summing = summing + cons_nodes.get(i)[2][cons_nodes.get(i)[1].index(j)]*(initial_nodes.get(i)[1] + initial_nodes.get(j)[1] + 2*initial_nodes.get(i)[1]*initial_nodes.get(j)[1])*(initial_nodes.get(i)[1] + initial_nodes.get(j)[1] + 2*initial_nodes.get(i)[1]*initial_nodes.get(j)[1])
#     for i in incons_nodes :
#         for j in incons_nodes.get(i)[1] :
#             summing = summing + incons_nodes.get(i)[2][incons_nodes.get(i)[1].index(j)]*(1-initial_nodes.get(i)[1] - initial_nodes.get(j)[1] + 2*initial_nodes.get(i)[1]*initial_nodes.get(j)[1])*(1 - initial_nodes.get(i)[1] - initial_nodes.get(j)[1] + 2*initial_nodes.get(i)[1]*initial_nodes.get(j)[1])
#     #func(x)
    return [bounds1,initial]
    
def optimization(a):
    res = minimize(func, a[1] , method='SLSQP', bounds = a[0])
    #res = minimize(func, a[1] , method='BFGS', bounds = a[0])
    #print res.x
    return res.x

def updateValues(new_values) :
    count = 0
    for i in initial_nodes :
        if initial_nodes.get(i)[0] == 0 :
            initial_nodes.get(i)[1] = new_values[count]
            count = count + 1
    #print "----------------------------------------"
    #print initial_nodes
    
# ---------------------------- MAIN FUNCTION----------------------------------------------

# List of processed tweets about a movies
tweetstrings = []
for line in open('C:\\IRProject\\pptres.txt','r').read().splitlines():
    tweetstrings.append(line)

# twitter_id : id : [tweet text,[each sentence {noun position :noun,{position : adjective}}]]
twitter_id = {}
negation_list = {}
count = 0

# loading senti words from dictionary
with open('C:\IRProject\senti_word_final.txt', 'rb') as f:
    senti_words = pickle.load(f)

for t in tweetstrings :
    twitter_id[count] = []
    twitter_id.get(count).append(t)
    sentences = t.split(".")
    sentences_list = []
    for s in sentences :
        try :
            if len(s) != 0 :
                depen = {}
                sentence_POS = {} 
                result = {}
                negations = {}
                depen = dependencies(s)
                result = selections(check_noun(s))
                nodeCalculations(result,s)
                sentences_list.append(result)
        except :
            continue
    twitter_id.get(count).append(sentences_list)
    count = count + 1
    #print count
    negation_list[count] = negations;
a=initialization()
new_values = optimization(a)
updateValues(new_values)

#print twitter_id


# word : [(possum,negsum),(poscount,negcount),(posavg,negavg),(max_values),(id),(maxvalues neg),(id)]
# categorization - word : [[all positive ids],[all negative ids]]
imp_words = {}
categorization = {}
highest_scores = {}
for i in twitter_id :
    highest_scores[i] = {}
    for j in twitter_id.get(i)[1] :
        for k in j :
            sump = 0
            sumn = 0
            for l in j.get(k)[1] :
                try :
                    
                    sump = sump + initial_nodes[l][1]
                    sumn = sumn + 1 - initial_nodes[l][1]
                except :
                    continue
            if j.get(k)[0] in imp_words :
                imp_words.get(j.get(k)[0])[0][0] = imp_words.get(j.get(k)[0])[0][0] + sump
                imp_words.get(j.get(k)[0])[0][1] = imp_words.get(j.get(k)[0])[0][1] + sumn
                imp_words.get(j.get(k)[0])[1][0] = imp_words.get(j.get(k)[0])[1][0] + 1
                imp_words.get(j.get(k)[0])[1][1] = imp_words.get(j.get(k)[0])[1][1] + 1
                if sump > max(imp_words.get(j.get(k)[0])[3][0],imp_words.get(j.get(k)[0])[3][1]) :
                    imp_words.get(j.get(k)[0])[4][imp_words.get(j.get(k)[0])[3].index(min(imp_words.get(j.get(k)[0])[3][0],imp_words.get(j.get(k)[0])[3][1]) )] = i
                    imp_words.get(j.get(k)[0])[3][imp_words.get(j.get(k)[0])[3].index(min(imp_words.get(j.get(k)[0])[3][0],imp_words.get(j.get(k)[0])[3][1]) )] = sump
                if sumn > max(imp_words.get(j.get(k)[0])[5][0],imp_words.get(j.get(k)[0])[5][1]) :
                    imp_words.get(j.get(k)[0])[6][imp_words.get(j.get(k)[0])[5].index(min(imp_words.get(j.get(k)[0])[5][0],imp_words.get(j.get(k)[0])[5][1]) )] = i
                    imp_words.get(j.get(k)[0])[5][imp_words.get(j.get(k)[0])[5].index(min(imp_words.get(j.get(k)[0])[5][0],imp_words.get(j.get(k)[0])[5][1]) )] = sumn
            else :
                imp_words[j.get(k)[0]] = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
                imp_words.get(j.get(k)[0])[0][0] = imp_words.get(j.get(k)[0])[0][0] + sump
                imp_words.get(j.get(k)[0])[0][1] = imp_words.get(j.get(k)[0])[0][1] + sumn
                imp_words.get(j.get(k)[0])[1][0] = imp_words.get(j.get(k)[0])[1][0] + 1
                imp_words.get(j.get(k)[0])[1][1] = imp_words.get(j.get(k)[0])[1][1] + 1
                if sump > max(imp_words.get(j.get(k)[0])[3][0],imp_words.get(j.get(k)[0])[3][1]) :
                    imp_words.get(j.get(k)[0])[4][imp_words.get(j.get(k)[0])[3].index(min(imp_words.get(j.get(k)[0])[3][0],imp_words.get(j.get(k)[0])[3][1]) )] = i
                    imp_words.get(j.get(k)[0])[3][imp_words.get(j.get(k)[0])[3].index(min(imp_words.get(j.get(k)[0])[3][0],imp_words.get(j.get(k)[0])[3][1]) )] = sump
                if sumn > max(imp_words.get(j.get(k)[0])[5][0],imp_words.get(j.get(k)[0])[5][1]) :
                    imp_words.get(j.get(k)[0])[6][imp_words.get(j.get(k)[0])[5].index(min(imp_words.get(j.get(k)[0])[5][0],imp_words.get(j.get(k)[0])[5][1]) )] = i
                    imp_words.get(j.get(k)[0])[5][imp_words.get(j.get(k)[0])[5].index(min(imp_words.get(j.get(k)[0])[5][0],imp_words.get(j.get(k)[0])[5][1]) )] = sumn
            if j.get(k)[0] in categorization :    
                if sump > sumn :
                    categorization.get(j.get(k)[0])[0].append(i)
                else :
                    categorization.get(j.get(k)[0])[1].append(i)
            else :
                categorization[j.get(k)[0]] = [[],[]]
                if sump > sumn :
                    categorization.get(j.get(k)[0])[0].append(i)
                else :
                    categorization.get(j.get(k)[0])[1].append(i)
#print imp_words
#print categorization
imp_word_results = {}
imp_word_results1 = {}
for i in imp_words :
    imp_word_results[i] = []
    imp_word_results1[i] = []
    imp_word_results1.get(i).append(imp_words.get(i)[0][0])
    imp_word_results1.get(i).append(imp_words.get(i)[0][1])
    imp_word_results.get(i).append(twitter_id.get(imp_words.get(i)[4][0])[0])
    imp_word_results.get(i).append(twitter_id.get(imp_words.get(i)[4][1])[0])
    imp_word_results.get(i).append(twitter_id.get(imp_words.get(i)[6][0])[0])
    imp_word_results.get(i).append(twitter_id.get(imp_words.get(i)[6][1])[0])
    #print i 
    #print twitter_id.get(imp_words.get(i)[4][0])[0]
    #print twitter_id.get(imp_words.get(i)[4][1])[0]
    #print twitter_id.get(imp_words.get(i)[6][0])[0]
    #print twitter_id.get(imp_words.get(i)[6][1])[0]
    
# This is being done for testing purposes
f = open('C:\IRProject\senti_words1.txt', 'wb')
for i in categorization : 
    f.write("\n")
    f.write(i+" : ")
    for j in categorization.get(i)[0] :
        f.write("\n")
        f.write("positive:" + str(j) + " ")
    for j in categorization.get(i)[1] :
        f.write("\n")
        f.write("negative:" + str(j) + " ")
        
print imp_word_results
print imp_word_results1
# This will retu        
def outputToPHPone() :
    return imp_word_results
def outputToPHPtwo() :
    return imp_word_results1

pos,neg = gf.getFeatures(imp_word_results1,movieName)
