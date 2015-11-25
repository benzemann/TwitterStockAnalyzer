from os import listdir, rename
from os.path import isfile, join
import tweepy
import pickle

# Downloads 1000 tweets about every stock from a list of stocks

CONSUMER_KEY = 'Hn0iMOMPedfHJCW1BNKUcqWuQ'
CONSUMER_SECRET = 'xZQPkeNXylBO9ACnfYF9CQUmYbqJFzN7EOlsoHRATOY76ycCoW'
OAUTH_TOKEN = '839939725-zqkCf8B0PIxMP9BdMsmGdGvWMirJ2S76V0DokguG'
OAUTH_TOKEN_SECRET = 'pzLREI6VXAECXWgych06PQ4rgTO96pPJSNBFKIktLilgy'
PROCESSED_PATH = "random_stock_tweets/processed/"
UNPROCESSED_PATH = "random_stock_tweets/unprocessed/"
STOCK_PATH = "random_stock_tweets/"
PROCESSING_PATH = "random_stock_tweets/processing/"
USER_PATH = "random_stock_users/"
LIST_OF_STOCKS = "NYSE_all_stocks.txt"

def load_stock(stock):
    with open(UNPROCESSED_PATH+stock, 'r') as f:
        return pickle.load(f)
def load_user(user):
    with open(USER_PATH+user, 'r') as f:
        return pickle.load(f)

with open(LIST_OF_STOCKS) as f:
    to_be_downloaded = set(f.read().split('\n'))

already_downloaded = set([f for f in listdir(STOCK_PATH) if isfile(join(STOCK_PATH,f))])
to_be_downloaded = list(to_be_downloaded-already_downloaded)

auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

for symbol in to_be_downloaded:
    downloaded_users = set([f for f in listdir(USER_PATH) if isfile(join(USER_PATH, f))])
    try:
        tweets = api.search("${}".format(symbol), count=100)
        with open(STOCK_PATH + symbol, 'w') as f:
            pickle.dump(tweets, f)
        user_ids = set([tweet.author.id_str for tweet in tweets]).difference(downloaded_users)
        users = api.lookup_users(user_ids)
        for user in users:
            with open(USER_PATH + user.id_str, 'w') as f:
                pickle.dump(user, f)
    except tweepy.TweepError as e:
        print e
        pass