import cherrypy
import pickle
from mako.template import Template
from mako.lookup import TemplateLookup
import os
import networkx as nx
import tweepy
import stock_data_helpers

lookup = TemplateLookup(directories=['static/html'])
CONSUMER_KEY = 'Hn0iMOMPedfHJCW1BNKUcqWuQ'
CONSUMER_SECRET = 'xZQPkeNXylBO9ACnfYF9CQUmYbqJFzN7EOlsoHRATOY76ycCoW'
OAUTH_TOKEN = '839939725-zqkCf8B0PIxMP9BdMsmGdGvWMirJ2S76V0DokguG'
OAUTH_TOKEN_SECRET = 'pzLREI6VXAECXWgych06PQ4rgTO96pPJSNBFKIktLilgy'
screen_name1 = 'benzemann'

auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class StockAnalyzer(object):
    def __init__(self):
        self.auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.api = tweepy.API(auth)
        self.graph = pickle.load(open('static/data/community_graph.pickle', 'r'))
        self.inverse_communities = pickle.load(open('static/data/inverse_com.pickle', 'r'))

    @cherrypy.expose
    def index(self):
        tmpl = lookup.get_template("index.html")
        return tmpl.render()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stock(self, symbol):
        try:

            response = stock_data_helpers.get_dates_price_volume_tweetcount_lists(self.api, symbol)

            users = response[6]
            active_communities = set([com for com, members in self.inverse_communities.iteritems() for user in members if user in users])
            response[0].insert(0,'x')
            response[1].insert(0,'price')
            response[2].insert(0,'volume')
            response[3].insert(0,'tweet_vol')
            response[4].insert(0, 'bullish')
            response[5].insert(0, 'bearish')
            response[6] = list(active_communities)

            return {'data': response}
        except:
            return {'status': 500}

if __name__ == '__main__':
    static_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {
        '/': {'tools.staticdir.root': static_dir},
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "static"
        }
    }
    cherrypy.quickstart(StockAnalyzer(), '/', conf)