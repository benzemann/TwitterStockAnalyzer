import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
import os
lookup = TemplateLookup(directories=['static/html'])

class Stock():
    def __init__(self, symbol):
        self.symbol = symbol
        pass

class User():
    def __init__(self, id):
        self.id = id
        pass

class StockAnalyzer(object):
    @cherrypy.expose
    def index(self):
        tmpl = lookup.get_template("index.html")
        return tmpl.render()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stock(self):
        return {"key1": 1234, "key2":"This is valid json", "key3":[1,2,3,"more json"]}

def setup():
    pass


if __name__ == '__main__':
    static_dir = os.path.dirname(os.path.abspath(__file__))
    cherrypy.quickstart(StockAnalyzer(), '/', 'app.conf')

    users = [{"id": 1, "tweetedAbout": ["GOOG","ABCO"]}]