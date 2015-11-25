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


def plot_stock_date(symbol, start_date, end_date, tweet_volume):
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
	ax = plt.subplot(311)
	ax2 = plt.subplot(312)
	ax3 = plt.subplot(313)
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
	ax3.xaxis_date()
	ax3.autoscale_view()
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
	# Plot tweet volume
	tweet_volume = np.asarray(tweet_volume)
	dates = []
	for x in range(0, len(tweet_volume)):
		dates.append(ds[0] + x)
	ax3.bar(dates, tweet_volume, width=1.0, align='center')
	# Show figure
	plt.show()
	
def get_tweets_from_symbol(api, symbol, number_of_tweets=100000):
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
	
# Returns a list of lists with price and volume of the stock,
# The parameter dates should be a list of dates in the format
# 'year-month-day', same format for start_date and end_date
def get_stock_price_and_volume(symbol, start_date, end_date, dates):
	share = Share(symbol)
	hist_data = share.get_historical(start_date, end_date)
	hist_data.reverse()
	volume = []
	price = []
	i = 0
	for d in dates:
		if i < len(hist_data):
			if (hist_data[i]['Date'] == d):
				# Weekday
				price.append(hist_data[i]['Close'])
				volume.append(hist_data[i]['Volume'])
				i += 1
			else:
				# Weekend
				price.append(0)
				volume.append(0)
		else:
			# Get the current price and volume instead from historical data
			price.append(share.get_price())
			volume.append(share.get_volume())
	if len(dates) != len(volume) and len(dates) != len(price):
		print 'Dates and volume and/or price lists are not of same lenght!'
	return [price, volume]
# Returns a list of dates from the given tweets, the format
# will be 'year-month-day'
def get_dates_from_tweets(tweets):
	dates = []
	old_day = 0
	for tweet in reversed(tweets):
		tweet_date = str(tweet.created_at).split(' ')[0]
		day = int(tweet_date.split('-')[2])
		if (old_day == 0):
			old_day = day
		if (old_day > day or old_day < day):
			dates.append(tweet_date)
			old_day = day
	return dates
# Returns a list of tweet count per day 
def get_tweet_volume(tweets):
	tweet_volume = []
	old_date = (0,0,0)
	tweet_count = 0
	for tweet in reversed(tweets):
		tweet_date = str(tweet.created_at).split(' ')[0].split('-')
		tweet_date = ( int(tweet_date[0]) ,  int(tweet_date[1])  , int(tweet_date[2])) 
		tweet_count += 1
		if (old_date[2] == 0):
			old_date = tweet_date
		if (old_date[2] > tweet_date[2] or old_date[2] < tweet_date[2]):
			tweet_volume.append(tweet_count)
			tweet_count = 0
			old_date = tweet_date
	return tweet_volume

def get_dates_price_volume_tweetcount_lists(api, symbol):
	tweets = get_tweets_from_symbol(api, '$' + symbol, 100000)

	tweet_dates = get_dates_from_tweets(tweets)

	stock_data = get_stock_price_and_volume(symbol, 
											tweet_dates[0], 
											tweet_dates[-1], 
											tweet_dates)
	
	tweet_volume = get_tweet_volume(tweets)
	if (len(tweet_dates) != len(stock_data[0]) or 
		len(tweet_dates) != len(stock_data[1]) or 
		len(tweet_dates) != len(tweet_volume)
		):
		print 'Some of the lists are not of the same length!'
	return [tweet_dates, stock_data[0], stock_data[1], tweet_volume]

def get_tweet_text_list(tweets):
	tweet_text = []
	for tweet in tweets:
		tweet_text.append(tweet.text)
	return tweet_text
CONSUMER_KEY = 'Hn0iMOMPedfHJCW1BNKUcqWuQ'
CONSUMER_SECRET = 'xZQPkeNXylBO9ACnfYF9CQUmYbqJFzN7EOlsoHRATOY76ycCoW'
OAUTH_TOKEN = '839939725-zqkCf8B0PIxMP9BdMsmGdGvWMirJ2S76V0DokguG'
OAUTH_TOKEN_SECRET = 'pzLREI6VXAECXWgych06PQ4rgTO96pPJSNBFKIktLilgy'
screen_name1 = 'benzemann'

auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#data = get_dates_price_volume_tweetcount_lists(api, 'ALKS')
tweets = get_tweets_from_symbol(api, '$' + 'ALKS')
print get_tweet_text_list(tweets)[1]



# start_date = str(tweets[0].created_at).split(' ')[0].split('-')
# end_date = str(tweets[-1].created_at).split(' ')[0].split('-')

# tweet_volume = []
# old_date = (0,0,0)
# tweet_count = 0
# for tweet in reversed(tweets):
	# tweet_date = str(tweet.created_at).split(' ')[0].split('-')
	# tweet_date = ( int(tweet_date[0]) ,  int(tweet_date[1])  , int(tweet_date[2])) 
	# tweet_count += 1
	# if (old_date[2] == 0):
		# old_date = tweet_date
	# if (old_date[2] > tweet_date[2] or old_date[2] < tweet_date[2]):
		# tweet_volume.append(tweet_count)
		# tweet_count = 0
		# old_date = tweet_date
# #print tweet_volume	
# start_date = ( int(start_date[0]) ,  int(start_date[1])  , int(start_date[2])) 
# end_date =  ( int(end_date[0]) , int(end_date[1]) , int(end_date[2]) )

# plot_stock_date('GOOGL',end_date, start_date, tweet_volume)
