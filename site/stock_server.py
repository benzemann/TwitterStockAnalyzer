import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
import os
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
class User():
    def __init__(self, id):
        self.id = id
        pass

class StockAnalyzer(object):
    def __init__(self):
        self.auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.api = tweepy.API(auth)

    @cherrypy.expose
    def index(self):
        tmpl = lookup.get_template("index.html")
        return tmpl.render()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stock(self, symbol):
        data = stock_data_helpers.get_dates_price_volume_tweetcount_lists(self.api, symbol)
        data[0].insert(0,'x')
        data[1].insert(0,'price')
        data[2].insert(0,'stock volume')
        data[3].insert(0,'tweet volume')
        return {'data': data}

if __name__ == '__main__':
    static_dir = os.path.dirname(os.path.abspath(__file__))
    cherrypy.quickstart(StockAnalyzer(), '/', 'app.conf')