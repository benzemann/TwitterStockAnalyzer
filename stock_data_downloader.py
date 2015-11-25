from yahoo_finance import Share
import tweepy
import matplotlib.pyplot as plt
import matplotlib.finance as pltf
import numpy as np
import json
import requests
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, YearLocator, MonthLocator

def get_historical_data(symbol, start_date, end_date):
	share = Share(symbol)
	return share.get_historical(start_date,end_date)

def old_plot_stock_date(data):
	price = []
	volume = []
	dates = []
	x = []
	c = 0
	for d in data:
		x.append(c)
		c += 1
		price.append(d['Close'])
		volume.append(d['Volume'])
		dates.append(d['Date'])
	plt.figure(1)
	plt.subplot(211)
	plt.xticks(x,dates)
	plt.ylabel('Price')
	plt.plot(x,price, 'b')
	plt.subplot(212)
	plt.xticks(x,dates)
	plt.ylabel('Volume')
	plt.plot(x,volume, 'r')
	plt.show()


def plot_stock_date(symbol, start_date, end_date):
	# Get the quote data from the symbol and unpack it
	quotes = pltf.quotes_historical_yahoo_ohlc(symbol, start_date, end_date)
	ds, open, highs, lows,close,  volumes = zip(*quotes)
	# Scale the labels with the amount of quotes
	if len(quotes) < 31:
		locator = DayLocator()
		weekFormatter = DateFormatter('%b %d')
	elif len(quotes) >=31 and len(quotes) < 500:
		locator = MonthLocator()
		weekFormatter = DateFormatter('%y %b')
	elif len(quotes) >= 500 and len(quotes) < 600:
		locator = MonthLocator()
		weekFormatter = DateFormatter('%b')
	else:
		locator = YearLocator()
		weekFormatter = DateFormatter('%y')
	alldays = WeekdayLocator()
	# Create the figure, axis, and locators
	fig = plt.figure(1)
	ax = plt.subplot(211)
	ax2 = plt.subplot(212)
	fig.subplots_adjust(bottom=0.2)
	ax.xaxis.set_major_locator(locator)
	ax.xaxis.set_minor_locator(alldays)
	ax.xaxis.set_major_formatter(weekFormatter)
	# Plot candlestick
	pltf.candlestick_ohlc(ax, quotes, width=0.6, colorup='g')
	# Set date and autoscale
	ax.xaxis_date()
	ax.autoscale_view()
	plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
	ax2.xaxis_date()
	ax2.autoscale_view()
	# Extract the volume and calculate the color for each bar
	vol = [v for v in volumes]
	vol = np.asarray(vol)
	dates = [d for d in ds]
	op = [o for o in open]
	cl = [c for c in close]
	cols = []
	for x in range(0, len(op)):
		if op[x] - cl[x] < 0:
			cols.append('g')
		else:
			cols.append('r')
	# Plot volume as red and green bars
	ax2.bar(dates, vol, width=1.0,align='center', color=cols)
	# Show figure
	plt.show()
	
def get_tweets_from_symbol(api, symbol, number_of_tweets=1000):
	tweets = []
	try:
		for fetched_tweets in tweepy.Cursor(api.search, symbol, count=100).pages():
			print "Fetched {} tweets".format(len(fetched_tweets))
			for tweet in fetched_tweets:
				tweets.append(tweet)
			if(len(tweets) >= number_of_tweets):
				break
	except tweepy.TweepError as e:
		print e
		pass
	return tweets
def get_tweets_from_symbol_topsy(symbol):
	url = 'http://api.topsy.com/v2/content/tweets.json?'
	
	r = requests.post(url, params={'q':'$APPL', 'apikey':'NZ4ODKQKMKT2DCTGFUNAAAAAADSYUXASO5LAAAAAAAAFQGYA'})
	
	res = r.json()
	
	print res['response']['error']

	
CONSUMER_KEY = 'Hn0iMOMPedfHJCW1BNKUcqWuQ'
CONSUMER_SECRET = 'xZQPkeNXylBO9ACnfYF9CQUmYbqJFzN7EOlsoHRATOY76ycCoW'
OAUTH_TOKEN = '839939725-zqkCf8B0PIxMP9BdMsmGdGvWMirJ2S76V0DokguG'
OAUTH_TOKEN_SECRET = 'pzLREI6VXAECXWgych06PQ4rgTO96pPJSNBFKIktLilgy'
screen_name1 = 'benzemann'
auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweets = get_tweets_from_symbol(api, '$ALKS')

start_date = str(tweets[0].created_at).split(' ')[0].split('-')
end_date = str(tweets[-1].created_at).split(' ')[0].split('-')

start_date = ( int(start_date[0]) ,  int(start_date[1])  , int(start_date[2])) 
end_date =  ( int(end_date[0]) , int(end_date[1]) , int(end_date[2]) )

plot_stock_date('ALKS',end_date, start_date)
