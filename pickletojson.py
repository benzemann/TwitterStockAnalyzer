import pickle 
import json

stock_symbols = []

with open('list_of_stocks.txt', 'r') as f:
	stocks = f.read()
f.close()
stock_symbols = stocks.split('\n')

for stock in stock_symbols:
	print stock
	with open('.\\random_stock_tweets\\' + stock, 'r') as f:
		all_stock_tweets = pickle.load(f)
	f.close()
	tmp = []
	for tw in all_stock_tweets:
		tmp.append(tw)
	#with open('.\\random_stock_tweets_json\\' + stock, 'w') as f:
	json.dump(tmp, stock)
	f.close()