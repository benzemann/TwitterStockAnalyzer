from yahoo_finance import Share
import matplotlib.pyplot as plt

def get_historical_data(symbol, start_date, end_date):
	share = Share(symbol)
	return share.get_historical(start_date,end_date)

def plot_stock_date(data):
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
	
	

data = get_historical_data('AAPL', '2015-11-02', '2015-11-06')
plot_stock_date(data)