import twitter_account as ta
import pickle
from os import listdir
from os.path import isfile, join
import tweepy
import warnings
import random

warnings.filterwarnings('ignore')
CONSUMER_KEY1 = 'Hn0iMOMPedfHJCW1BNKUcqWuQ'
CONSUMER_SECRET1 = 'xZQPkeNXylBO9ACnfYF9CQUmYbqJFzN7EOlsoHRATOY76ycCoW'
OAUTH_TOKEN = '839939725-zqkCf8B0PIxMP9BdMsmGdGvWMirJ2S76V0DokguG'
OAUTH_TOKEN_SECRET = 'pzLREI6VXAECXWgych06PQ4rgTO96pPJSNBFKIktLilgy'
screen_name1 = 'benzemann'
PROCESSED_PATH = "random_stock_tweets/processed/"
UNPROCESSED_PATH = "random_stock_tweets/unprocessed/"
USER_PATH = "random_stock_users/"
auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
uauth1 = tweepy.OAuthHandler(CONSUMER_KEY1, CONSUMER_SECRET1)
api1 = tweepy.API(uath1, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def load_stock(stock):
	with open(PATH+stock, 'r') as f:
		return pickle.load(f)
def load_user(user):
	with open(USER_PATH+user, 'r') as f:
		return pickle.load(f)


# Get the names of all the pickled stocks
stocks = {f: load_stock(f) for f in listdir(PATH) if isfile(join(PATH,f))}
# Create an object for storing the relations between users and stock tweets
stock_user_followers = {}
stock_counter = 0.0
for (symbol, stock_tweets) in stocks.iteritems():
	stock_counter = stock_counter + 1.0
	stock_progress = stock_counter / len(stocks)*100
	print "Stock progress: {:.2f}%".format(stock_progress)
	stock_user_followers[symbol] = {}
	# Get the unique users that tweeted about a stock, small io overhead that can be ignored for now
	downloaded_users = [f for f in listdir(USER_PATH) if isfile(join(USER_PATH, f))]
	user_ids = set([tweet.author.id_str for tweet in stock_tweets])
	# Make sure we're not downloading any users we've already downloaded once
	user_ids = user_ids.difference(set(downloaded_users))
	# In case we already downloaded all the users for this tweet, continue
	if len(user_ids) is 0:
		continue
	# Get the user object from their ID's
	# TODO: paginate if there are more than 100 ID's
	try:
		users = api.lookup_users(user_ids)
		stock_user_followers[symbol]['users'] = {user.id_str: {'obj': user, 'followers': [], 'following': []} for user in users}
		user_count = 0.0
		for user in users:
			user_count = user_count + 1.0
			user_progress = user_count / len(users)*100
			print "Stock progress: {:.2f} %, User progress: {:.2f} %".format(stock_progress, user_progress)
			for user_followers in tweepy.Cursor(api.followers_ids, user.id_str).pages():
				print "Fetched {} followers".format(len(user_followers))
				stock_user_followers[symbol]['users'][user.id_str]['followers'].append(user_followers)
			for user_following in tweepy.Cursor(api.friends_ids, user.id_str).pages():
				print "Fetched {} following".format(len(user_following))
				stock_user_followers[symbol]['users'][user.id_str]['following'].append(user_following)
			with open(USER_PATH+user.id_str, 'w') as f:
				pickle.dump(stock_user_followers[symbol]['users'][user.id_str], f)
	except tweepy.TweepError as e:
		print e
		pass