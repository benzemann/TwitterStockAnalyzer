import twitter_account as ta
import pickle
import os 

cwd = os.getcwd()
tweets = []
stock_symbols = []

with open('list_of_stocks.txt', 'r') as f:
	stocks = f.read()
f.close()

stock_symbols = stocks.split('\n')

for stock in stock_symbols:
	with open(cwd + '/random_stock_tweets/' + stock, 'r') as f:
		all_stock_tweets = pickle.load(f)
		for tweet in all_stock_tweets:
			tweets.append(tweet)
	f.close()
	
user_ids = []
for tweet in tweets:
	user = tweet.user
	user_ids.append(user.id)

CONSUMER_KEY = 'Hn0iMOMPedfHJCW1BNKUcqWuQ'
CONSUMER_SECRET = 'xZQPkeNXylBO9ACnfYF9CQUmYbqJFzN7EOlsoHRATOY76ycCoW'
OAUTH_TOKEN = '839939725-zqkCf8B0PIxMP9BdMsmGdGvWMirJ2S76V0DokguG'
OAUTH_TOKEN_SECRET = 'pzLREI6VXAECXWgych06PQ4rgTO96pPJSNBFKIktLilgy'
screen_name = 'benzemann'
	
twitter_acc = ta.TwitterAccount(CONSUMER_KEY, 
								CONSUMER_SECRET, 
								OAUTH_TOKEN,
								OAUTH_TOKEN_SECRET, 
								screen_name)

							
all_tweets = []
c = 0
for user in user_ids[:100]:
	tweets_from_user = twitter_acc.get_tweets_from_user(user, 100)
	for tweet in tweets_from_user:
		all_tweets.append(tweet)
	c += 1
	if(c == 10):
		with open('all_tweets', 'wb') as f:
			pickle.dump(all_tweets ,f)
		f.close()
with open('all_tweets', 'wb') as f:
	pickle.dump(all_tweets ,f)
f.close()