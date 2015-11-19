
import pickle
import re


with open("all_tweets","r") as f:
	all_tweets = pickle.load(f)

	
# Join all tweets in one string
all_tweets_string = ' '.join(all_tweets).lower()

# Set of unprocessed words
original = set(all_tweets_string.split(' '))

# Processed words
[all_words, removed] = get_words(all_tweets_string)




# Most common words in all tweets!
word_count = Counter(all_words)
del word_count['']
# dump in csv file in order
csv_dump(word_count.most_common(len(word_count)))

#print word_count.most_common(50)


	

