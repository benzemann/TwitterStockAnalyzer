"""
Functions to classify a set of tweets based on a dictionary of positive and negative words
"""

import pickle
def pickle_load(path):		
    with open(path,"r") as f:
        return pickle.load(f)
		
def pickle_dump(p, path):
    with open(path,"w") as f:
        pickle.dump(p,f)
		
def csv_dump(word_dict, file_name):
    with open("./classifier/"+file_name+".csv","w") as f:
        for (w,s) in word_dict.iteritems():
            f.write(w.encode('utf-8')+';'+s+'\n')

# --------------------------------------------------------------------------------- #

word_dict = pickle_load("./classifier/word_dict.pickle")
all_tweets = pickle_load("./random_stock_tweets/all_stock_tweets.pickle")

def tweet_score(document):
# Scores a tweet counting how many bearish/bullish words it has
# Returns its class
    document_words = set(document.split(' '))
    score = 0
    word_dict_keys = set(word_dict.keys())
    for word in document_words:
        if word in word_dict_keys:
            score = score + int(word_dict[word])
    if score>0:
        return "Bullish"
    if score == 0:
        return "Neutral"
    if score <0:
       return "Bearish"
	   
import re
def score_tweets(all_tweets):
# Classifies a list of tweets
# Returns dictionary with results
    all_tweets = set(all_tweets)
    classified_tweets = {}
    for tweet in all_tweets:
        tweet = re.sub('[\n;]','',tweet)
        classified_tweets[tweet] = tweet_score(tweet)
    #csv_dump(classified_tweets, "classified_tweets")
    pickle_dump(classified_tweets, "./classifier/classified_tweets.pickle")
    return classified_tweets

def get_bear_bull(classified_tweets):
#gets all bearish and bullish tweets in two separate lists
    bearish = []
    bullish = []
    for tweet in classified_tweets.keys():
        if classified_tweets[tweet] == 'Bullish':
            bullish.append(tweet)
        if classified_tweets[tweet] == 'Bearish':
            bearish.append(tweet)
			
    # with open("./classifier/bearish_tweets.csv","w") as f:
        # for t in bearish:
            # f.write(t.encode('utf-8')+'\n')
    # with open("./classifier/bullish_tweets.csv","w") as f:
        # for t in bullish:
            # f.write(t.encode('utf-8')+'\n')
			
    return [bullish, bearish]
	

