import requests
import json
import datetime
import time

def sleep_until(wake_up_time, max_sleep_interval=60):
	"""
........The program will sleep until the time reaches a given time stamp.
........Input is the wake up time and the maximum sleep interval.
........"""
	wake_up_datetime = datetime.datetime.fromtimestamp(wake_up_time)
	while True:
		# Calculate the seconds until wake up plus a 4 second
		# buffer for security
		seconds_until_wake = (wake_up_datetime - datetime.datetime.now())\
								.total_seconds()+4

		if seconds_until_wake < 0.0:
			break

		sleep_seconds = min(seconds_until_wake, max_sleep_interval)

		print "  {}s until wakeup, sleeping for another {}s"\
				.format(seconds_until_wake, sleep_seconds)

		time.sleep(sleep_seconds)
	
	print "  Waking up"

def download_twits_from_symbol(symbol, start_id=0, iteration=0, stock_twits=[]):
	url = 'https://api.stocktwits.com/api/2/streams/symbol/' + symbol + '.json'
	
	r = requests.get(url)
	
	next_id = start_id
	if r.json().keys()[0] == 'errors':
		for error in r.json()['errors']:
			print error['message']
	else:	
		twits_json = r.json()
		for twit in twits_json['messages']:
			stock_twits.append(twit)
		next_id = twits_json['messages'][-1]['id']
	rate_limit = r.headers['x-ratelimit-remaining']
	print 'You have ' + str(rate_limit) + ' requests left'
	if(rate_limit == '0'):
		wake_up_time = r.headers['x-ratelimit-reset']
		sleep_until(float(wake_up_time))
		download_twits_from_symbol(symbol, start_id=next_id, iteration=iteration+1, stock_twits=stock_twits)
	
	if(iteration+1 <= 2):
		download_twits_from_symbol(symbol, start_id=next_id, iteration=iteration+1, stock_twits=stock_twits)
# Get the stock symbols
stock_symbols = []

with open('list_of_stocks.txt', 'r') as f:
	stocks = f.read()
f.close()

stock_symbols = stocks.split('\n')

stock_twits = []

for symbol in stock_symbols[0]:
	download_twits_from_symbol(symbol,stock_twits=stock_twits)
		
print stock_twits[0]
	
with open('test.json', 'w') as f:
	json.dumps(['asd', 'asd', 's'], f)
f.close()
	
	
