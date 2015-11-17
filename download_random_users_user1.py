import twitter_account as ta
import pickle
from os import listdir, rename
from os.path import isfile, join
import tweepy
import warnings
import random

warnings.filterwarnings('ignore')
CONSUMER_KEY = 'Hn0iMOMPedfHJCW1BNKUcqWuQ'
CONSUMER_SECRET = 'xZQPkeNXylBO9ACnfYF9CQUmYbqJFzN7EOlsoHRATOY76ycCoW'
OAUTH_TOKEN = '839939725-zqkCf8B0PIxMP9BdMsmGdGvWMirJ2S76V0DokguG'
OAUTH_TOKEN_SECRET = 'pzLREI6VXAECXWgych06PQ4rgTO96pPJSNBFKIktLilgy'
screen_name1 = 'benzemann'
PROCESSED_PATH = "random_stock_tweets/processed/"
UNPROCESSED_PATH = "random_stock_tweets/unprocessed/"
PROCESSING_PATH = "random_stock_tweets/processing/"
USER_PATH = "random_stock_users/"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def load_stock(stock):
	with open(UNPROCESSED_PATH+stock, 'r') as f:
		return pickle.load(f)
def load_user(user):
	with open(USER_PATH+user, 'r') as f:
		return pickle.load(f)


while len([f for f in listdir(UNPROCESSED_PATH) if isfile(join(UNPROCESSED_PATH, f))]) > 0:
	# Create an object for storing the relations between users and stock tweets
	stock_user_followers = {}
	# Get the names of all the pickled stocks
	stocks = {f: load_stock(f) for f in listdir(UNPROCESSED_PATH) if isfile(join(UNPROCESSED_PATH,f))}
	symbol = random.sample(stocks, 1)[0]
	rename(UNPROCESSED_PATH + symbol, PROCESSING_PATH + symbol)
	stock_tweets = stocks[symbol]
	print "Remaining stocks: {}".format(len(stocks))
	stock_user_followers[symbol] = {}
	# Get the unique users that tweeted about a stock, small io overhead that can be ignored for now
	downloaded_users = [f for f in listdir(USER_PATH) if isfile(join(USER_PATH, f))]
	user_ids = set([tweet.author.id_str for tweet in stock_tweets])
	# Make sure we're not downloading any users we've already downloaded once
	user_ids = user_ids.difference(set(downloaded_users))
	# In case we already downloaded all the users for this tweet, continue
	if len(user_ids) is 0:
		rename(PROCESSING_PATH + symbol, PROCESSED_PATH + symbol)
		continue
	try:
		# Get the user object from their ID's
		# TODO: paginate if there are more than 100 ID's
		users = api.lookup_users(user_ids)
		stock_user_followers[symbol]['users'] = {user.id_str: {'obj': user, 'followers': [], 'following': []} for user in users}
		user_count = 0.0
		for user in users:
			user_count = user_count + 1.0
			user_progress = user_count / len(users)*100
			print "Remaining stocks: {}, User progress: {:.2f} %".format(len(stocks), user_progress)
			# Get the people following the user
			for user_followers in tweepy.Cursor(api.followers_ids, user.id_str).pages():
				print "Fetched {} followers".format(len(user_followers))
				stock_user_followers[symbol]['users'][user.id_str]['followers'].append(user_followers)
			# Get the people the user is following
			for user_following in tweepy.Cursor(api.friends_ids, user.id_str).pages():
				print "Fetched {} following".format(len(user_following))
				stock_user_followers[symbol]['users'][user.id_str]['following'].append(user_following)
			with open(USER_PATH+user.id_str, 'w') as f:
				pickle.dump(stock_user_followers[symbol]['users'][user.id_str], f)
	except tweepy.TweepError as e:
		print e
		pass
	finally:
		rename(PROCESSING_PATH + symbol, PROCESSED_PATH + symbol)