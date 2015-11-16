import twitter_account as ta
import pickle
from os import listdir
from os.path import isfile, join
import tweepy

CONSUMER_KEY = 'Hn0iMOMPedfHJCW1BNKUcqWuQ'
CONSUMER_SECRET = 'xZQPkeNXylBO9ACnfYF9CQUmYbqJFzN7EOlsoHRATOY76ycCoW'
OAUTH_TOKEN = '839939725-zqkCf8B0PIxMP9BdMsmGdGvWMirJ2S76V0DokguG'
OAUTH_TOKEN_SECRET = 'pzLREI6VXAECXWgych06PQ4rgTO96pPJSNBFKIktLilgy'
screen_name = 'benzemann'
PATH = "random_stock_tweets/"
auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def load_stock(stock):
	with open(PATH+stock, 'r') as f:
		return pickle.load(f)

# Get the names of all the pickled stocks
stocks = {f: load_stock(f) for f in listdir(PATH) if isfile(join(PATH,f))}
stock_user_followers = {}
count = 0
for (symbol, stock_tweets) in stocks.iteritems():
	stock_user_followers[symbol] = {}
	u_count = 0
	user_ids = set([tweet.author.id_str for tweet in stock_tweets])
	users = api.lookup_users(user_ids)
	stock_user_followers[symbol]['users'] = {user.id_str: {'obj': user, 'followers': []} for user in users}
	for user in users:
		print "Downloading followers for user id {}".format(user.id_str)
		for user_followers in tweepy.Cursor(api.followers_ids, user.id_str).pages():
			stock_user_followers[symbol]['users'][user.id_str]['followers'].append(user_followers)
		u_count = u_count + 1
		if u_count > 5:
			break
	count = count + 1
	if count > 3:
		break