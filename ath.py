import webapp2
import logging
import json
import requests
import sys
import traceback
from google.appengine.ext import ndb

class testATH(webapp2.RequestHandler):
    def get(self):
        getATH(self, 'BTC', 1512280800)
        getSpotPrice(self, 'BTC', 1512280800)

# Get ATH for symbol and end timestamp
#  - Uses Bittrex exchange as default
def getATH(self, symbol, endTimestamp):

    # Get the ATH of each hour
    durationEndpoint = 'histohour'

    # We need a timestamp (10 digits) to mark the end date
    #  By default, "histhour" will get the ATH, every hour, for the last 7 days from
    #  the "end" timestamp - 1512280800 = e.g. Sunday, December 3, 2017 6:00:00 AM GMT
    end = str(endTimestamp)

    # Querying crypto compare requires a GET request
    url = "https://min-api.cryptocompare.com/data/" + durationEndpoint + "?e=Bittrex&fsym="+ symbol + "&tsym=USD&aggregate=1&toTs="+ end + ""

    try:
        resp = requests.get(url)
        data = resp.json()['Data']

        #  Sort the data in reverse order, based on ATH so that first result IS the All-time high
        sortedList = sorted(data, key=lambda x: x['high'], reverse=True)
        self.response.write(json.dumps(sortedList[0]))
    except Exception as inst:
        self.response.write("Request Failed. " + "{0}".format(sys.exc_info()[0]) + " {0}".format(traceback.format_exc()))


#  Get spot price for a symbol
#  - Uses Bittrex exchange as default
def getSpotPrice(self, symbol, timestamp):
    url = "https://min-api.cryptocompare.com/data/pricehistorical?markets=Bittrex&fsym="+ symbol +"&tsyms=BTC,USD&ts="+ str(timestamp) +""

    # Try the request. If it fails, throw exception
    try:
        resp = requests.get(url)
        data = resp.json()

        self.response.write(json.dumps(data))
    except Exception as inst:
        self.response.write("Request Failed. " + "{0}".format(sys.exc_info()[0]) + " {0}".format(traceback.format_exc()))


# Associate this particular script with this route
app = webapp2.WSGIApplication([
    ('/ath', testATH),
], debug=True)


