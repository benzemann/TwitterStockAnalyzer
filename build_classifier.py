"""
Functions to build the classifier from collected tweet data
"""

import pickle
import re

tweets_doc_name = "all_tweets"
def get_word_frequencies(tweets_doc_name):
    with open(tweets_doc_name,"r") as f:
	    all_tweets = pickle.load(f)

    # Join all tweets in one string
    all_tweets_string = ' '.join(all_tweets).lower()

    # Set of unprocessed words - just for result analysis purposes
    original = set(all_tweets_string.split(' '))

    # Processed words
    [all_words, removed] = get_words(all_tweets_string)

    # Word Count
    word_count = Counter(all_words)
    del word_count['']
	# dump in csv file in order
    csv_dump(word_count.most_common(len(word_count)))

# Feature extractor: counting of words from the word table and sum the scores. Simple.

csv_file = "./classifier/word_dict.csv"
def get_word_dictionary(csv_file):
    with open(csv_file,"r") as f:
	    words = f.read().split('\n')
    word_dict = {}
    for w in words:
        ws = w.split(';')
    	if len(ws)>1 and int(ws[1]) != 0:
            word_dict[ws[0]] = ws[1]
    return word_dict
    
def count_classes(word_dict):
    positive = []
    negative = []
    for (w,s) in word_dict.iteritems():
        if int(s) > 0:
            positive.append(w)
        else:
            negative.append(w)
    return (positive, negative)


import string
def csv_dump(word_count):
# save resulting words in a csv document

	with open("./classifier/word_count.csv","w") as f:
		for (w,c) in word_count:
			f.write(w.encode('utf-8')+';'+str(c)+'\n')

def csv_dump_dict(word_dict, file_name):
    with open("./classifier/"+file_name+".csv","w") as f:
        for (w,s) in word_dict.iteritems():
            f.write(w.encode('utf-8')+';'+str(s)+'\n')
	

def pickle_dump(p, name):
    with open("./classifier/"+name+".pickle","w") as f:
        pickle.dump(p,f)

def pickle_load(name):		
    with open("./classifier/"+name+".pickle","r") as f:
        return pickle.load(f)



