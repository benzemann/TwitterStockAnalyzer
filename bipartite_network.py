import networkx as nx
from networkx.algorithms import bipartite
import pickle
from os import listdir
from os.path import isfile, join
from collections import *

PROCESSED_PATH = "random_stock_tweets/processed/"
USER_PATH = "random_stock_users/"


def load_stock(stock):
	with open(PROCESSED_PATH+stock, 'r') as f:
		return pickle.load(f)
def load_user(user):
	with open(USER_PATH+user, 'r') as f:
		return pickle.load(f)

stocks = {f: load_stock(f) for f in listdir(PROCESSED_PATH) if isfile(join(PROCESSED_PATH,f))}
users = {f: load_user(f) for f in listdir(USER_PATH) if isfile(join(USER_PATH, f))}

# Bipartite graphs in networkx are implemented using a normal graph where nodes have an attribute
# value of either 0 or 1 depending on which graph it belongs to

G = nx.Graph()
# Add all stocks
G.add_nodes_from(stocks.keys(), bipartite=0)
# Add all users
G.add_nodes_from(users.keys(), bipartite=1)
for (symbol, stock_tweets) in stocks.iteritems():
	# Find the users that tweeted about this stock
	user_ids = set([tweet.author.id_str for tweet in stock_tweets])
	G.add_edges_from([(symbol, user) for user in user_ids if user in users.keys()])

# Create the user network from the bipartite network
stock_nodes = set(n for n,d in G.nodes(data=True) if d['bipartite']==0)
user_nodes = set(G) - stock_nodes
U = bipartite.projected_graph(G, user_nodes)

