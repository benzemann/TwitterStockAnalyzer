# Analysis of stock prices and networks of stock advertisers in Twitter
##



### Goal
We would then like to look at specific cases of stocks that have been advertised on Twitter and see if negative or positive tweets have an effect on the stock price.

### Subgoals
* Create a network of stock advertisers based on a sample of random stock symbols
* Connect the nodes in the network either through followers or through common mentions of stocks
* Classify a tweet as negative / positive
* Correlate tweets with stock price

### Requirements
* Need to be able to search for a stock (request per stock, will get us users)
* Fetch users that have mentioned a stock
* Fetch their followers
* Construct network where stock mentioners are nodes / follows are edges
* Construct network where stock mentioners are nodes and edges are based on whether they mention the same stock (bi-partite network)
* Fetch tweets of users
* Do sentiment analysis on tweets (requires analysis of stock terminology)