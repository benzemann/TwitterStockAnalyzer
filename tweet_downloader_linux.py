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
	print stock
	with open(cwd + '/random_stock_tweets/' + stock, 'r') as f:
		try:
			all_stock_tweets = pickle.load(f)
			for tweet in all_stock_tweets:
				tweets.append(tweet)
		except:
			print 'error'
		
	f.close()
	
user_ids = []
for tweet in tweets:
	user = tweet.user
	user_ids.append(user.id)

CONSUMER_KEY = 'Kfn5jzo4oEOthNVXsHXOiM9d5'
CONSUMER_SECRET = 'wsxon5zr2aoheV2DeQq1dcZBba0HFXLLAds3C4U7i7yxjABkAZ'
OAUTH_TOKEN = '94603287-cEGmUZY7zpsMiQbbHGfXJWiQRsg0gBhpmIYBSQF8N'
OAUTH_TOKEN_SECRET = 'IgEPDbSDWAtw9sx8EgmTOq2uXCBE6dobYCeBCgAy0GoIp'
screen_name = 'simon'
	
twitter_acc = ta.TwitterAccount(CONSUMER_KEY, 
								CONSUMER_SECRET, 
								OAUTH_TOKEN,
								OAUTH_TOKEN_SECRET, 
								screen_name)

							
all_tweets = []
c = 0
for user in user_ids[999:1010]:
	tweets_from_user = twitter_acc.get_tweets_from_user(user, 100)
	for tweet in tweets_from_user:
		all_tweets.append(tweet)
	c += 1
	if(c == 10):
		with open('all_tweets_1000_to_5000', 'wb') as f:
			pickle.dump(all_tweets ,f)
		f.close()
with open('all_tweets_1000_to_5000', 'wb') as f:
	pickle.dump(all_tweets ,f)
f.close()