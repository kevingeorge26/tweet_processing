'''
Created on Nov 11, 2012

@author: kevin
'''
import nltk;
import csv;
from string import punctuation
import re, collections
from string import maketrans


stop_words = []
stop_words_dict = {}
final_list = {}


def read_csv():   
    ifile  = open('test.csv', "rb")
    reader = csv.reader(ifile)  
    
    counter = 0
    tweets = []
        
    for row in reader:
        if(len(row) < 4):
            print len(row)
        else:
            tweets.append( clean_string(row[3] ))
            print '%d ::  %s' % (counter,tweets[counter])
            counter += 1
            
    ifile.close()   
    print final_list

# remove stop words 
# do a spell check
# return space seperated keyword

def clean_string(toClean):    
    
    with_stop_words = toClean.translate(trantab).lower()     
    without_stop_words = " ".join( filter(lambda x: x not in stop_words_dict, with_stop_words.split(" ")) )   
    s =  correct_string(without_stop_words)  
    return s

#####################################################################################
################# code for the spell checker

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    stop_words_dict = collections.defaultdict(lambda: 1)
    for f in features:
        stop_words_dict[f] += 1
    return stop_words_dict

NWORDS = train(words(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in s if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
   inserts    = [a + c + b     for a, b in s for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    kevin = max(candidates, key=NWORDS.get)
    final_list[kevin] += 1 
    return kevin

def correct_string(toCorrect):
    words = toCorrect.split()
    return ' '.join(correct(word) for word in words)

#####################################################################################
################# code for the spell checker ends here

def play_python():   
    print "this is   a         test".split()  

if __name__ == '__main__':
    
    stop_words  =  open("stop_words.txt").read().split(",")
    stop_words_dict = collections.defaultdict(lambda: 1)
    final_list = collections.defaultdict(lambda: 1);
    trantab = maketrans(punctuation, " " * len(punctuation))
        
    for temp in stop_words:
        stop_words_dict[temp] = 1
    
    read_csv()
    #play_python()
   
    pass