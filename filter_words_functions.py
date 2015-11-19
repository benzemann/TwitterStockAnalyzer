import types
import collections
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

def is_wanted_token(token):
    # exclude punctuation and numbers
    
    regexes = []
    regexes.append(r"^[@$#&]") # removes stock symbols and twitter usernames
    regexes.append(r'[0-9]+') # removes numbers and punctuation
    regexes.append(r'http') # removes websites
    regexes.append(r'^\W+$') # removes tokens that are only punctuation

    for regex in regexes:
        if re.search(regex, token):
             #print "removed %s because of %s" %(token, regex)
             return 0
    return 1
	
	# -------------------- remove punctuation by substituting



from nltk.corpus import stopwords

	
def get_words(text):

    tokens = text.split(' ')
    wanted_tokens = []
    removed = []
	
    _stopwords = stopwords.words('english')
    # Remove irrelevant tokens (punctuation, numbers, etc)
    #wanted_tokens = [token for token in tokens if is_wanted_token(token) and token not in _stopwords]
	
    for token in tokens:
        if is_wanted_token(token) and token not in _stopwords:
            wanted_tokens.append(token)
        else:
            removed.append(token)
	
	all_words = remove_punctuation(all_words)
    # Lemmatizing
    lemmatizer = nltk.WordNetLemmatizer()
    wanted_tokens = [lemmatizer.lemmatize(token) for token in wanted_tokens]
        
    return [wanted_tokens,removed]

def remove_punctuation(all_words):
    regex = r"[:,.';?!\"\(\)]"
    for i in range(0,len(all_words)):
        if re.search(regex, all_words[i]):
		    re.sub(regex,'',all_words[i])
    return all_words	 

# dumps a list into a file
def file_dump(l):
    with open('test_file.txt','w') as f:
	    for w in l:
		    f.write(w.encode('utf-8')+'\n')
    return


import string
def csv_dump(word_count):
# save resulting words in a csv document

	with open("./classifier/word_count.csv","w") as f:
		for (w,c) in word_count:
			f.write(w.encode('utf-8')+';'+str(c)+'\n')
	