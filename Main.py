'''
Created on Nov 11, 2012

@author: kevin
'''
import nltk;
import csv;
import sqlite3
from string import punctuation
import re, collections
from string import maketrans
from collections import *


stop_words = []
stop_words_dict = {}
final_list = {}


def read_csv():   
    ifile  = open('test.csv', "rb")
    reader = csv.reader(ifile)
    writer = csv.writer(open("processed.csv", "wb"))
   
    for row in reader:
        if(len(row) < 4):
            print row
        else:
            row[3] = clean_string(row[3] )
            writer.writerow(row)
            #print '%d ::  %s' % (counter,tweets[counter])
            
            
    ifile.close()
    fo = open("result.txt", "w")
       
    for temp in sorted(final_list, key=final_list.get, reverse=True):         
        fo.write( temp + " = " + str(final_list[temp]) + "\n" )
    
    fo.close()
           

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
   
    if NWORDS[kevin] == 1:
        return ""
        
    final_list[kevin] += 1 
    return kevin

def correct_string(toCorrect):
    words = toCorrect.split()
    return ' '.join(correct(word) for word in words)

#####################################################################################
################# code for the spell checker ends here

def play_python():   
    d = {'banana': 3, 'apple':4, 'pear': 1, 'orange': 2}    
    print sorted(d, key=d.get, reverse=True)

# load filter and put only those lines in the database
# that has the keyword

def load_result():
    lst =  map(lambda x:x.strip().split(" = "),open("filters.txt").readlines())
    t = {}
   
    for r in lst:      
        t[r[0]] = int(r[1])
        
    conn = sqlite3.connect('example.db')
    conn.text_factory = str
    
    ifile  = open('test.csv', "rb")
    reader = csv.reader(ifile)
    counter = 0  
    for row in reader:
        for keyword in row[3].split(" "):
            if keyword in t:
                counter +=1
                val = [ (counter,row[0], row[1], row[2].split(" ")[0], row[2].split(" ")[1] ,row[3]) ]
                print row
                conn.executemany("INSERT INTO tweet (id,userid, datetime,lat,long,keywords) VALUES (?,?,?,?,?,?)",val);
               
                break;
    
    conn.commit()
    conn.close()

    
    
    
def create_table():
    conn = sqlite3.connect('example.db')
    val = (1,"5/18/2011 13:26",10,12,"keywordsssss")
    conn.executemany("INSERT INTO tweet VALUES (?,?,?,?,?)",[val]);
    conn.commit()
    conn.close()


if __name__ == '__main__':
    
    stop_words  =  open("stop_words.txt").read().split(",")
    stop_words_dict = collections.defaultdict(lambda: 1)
    final_list = collections.defaultdict(lambda: 1);
    trantab = maketrans(punctuation, " " * len(punctuation))
        
    for temp in stop_words:
        stop_words_dict[temp] = 1
    
    #read_csv()
    #play_python()
    load_result()
    #create_table()
   
    pass