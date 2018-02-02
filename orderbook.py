import webapp2
import logging
import json
import requests
import sys
import traceback
from bittrex.bittrex import Bittrex

from google.appengine.ext import ndb


# Model: Order Book
class OrderBook(ndb.Model):
    OrderbookJson = ndb.JsonProperty(compressed=True)
    RetrievedAt = ndb.DateTimeProperty(auto_now_add=True)
    AssetId1 = ndb.StringProperty()
    AssetId2 = ndb.StringProperty()

# Model: Waves Pairing
class WavesMarketConfig(ndb.Model):
    AssetId1 = ndb.StringProperty()
    AssetId2 = ndb.StringProperty()

#
# Order book
#
class testOrderbook(webapp2.RequestHandler):
    def get(self):

        # Get the Bittrex Order book
        # self.response.write(json.dumps(getBittrexOrderBook(marketPair='BTC-LTC', orderType="both")))
        self.response.write(json.dumps(getBittrexOrderBookHistory(marketPair='BTC-LTC')))

        # Create some pairings in the DB
        createPairings()

        # Specify some headers for proper API call
        self.response.headers['Content-Type'] = 'application/json'

        # Get the results from the Wave pairings data entity
        db_results = WavesMarketConfig.query()

        # Iterate through the pairings and call Waves API to get data about them
        for db_result in db_results:

            payload = {"asset2": db_result.AssetId2, "asset1": db_result.AssetId1}
            url = "http://ec2-34-217-82-62.us-west-2.compute.amazonaws.com:3000/api/waves/assetpairs/all"

            headers = {'content-type': 'application/json'}
            logging.info("sending pywaves test:")
            logging.info(payload)

            # Let's try running the API call to see if we get a response
            try:
                resp = requests.post(url, data=json.dumps(payload), headers=headers)

                # Create an entity object for storing the data
                ent = OrderBook(OrderbookJson=json.loads(resp.text), AssetId1=db_result.AssetId1, AssetId2=db_result.AssetId2)

                # Shove that data into a datastore and get the key that gets returned
                key = ent.put()

                # Print out the response via text
                self.response.write(resp.text)

            # Throw exception if things fail
            except Exception as inst:
                self.response.write("Request Failed. " + "{0}".format(sys.exc_info()[0]) + " {0}".format(traceback.format_exc()))

#
def createPairings():
    db_results = WavesMarketConfig.query()

    if db_results.get() == None:
        ent = WavesMarketConfig(AssetId1='474jTeYx2r2Va35794tCScAXWJG9hU2HcgxzMowaZUnu', AssetId2='8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS')
        ent.put()


# Get the Bittrex order book for a specific Pairing
def getBittrexOrderBook(marketPair, orderType):

    my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)
    return my_bittrex.get_orderbook(marketPair, orderType)


# Get the Bittrex order book history for a specific Pairing
def getBittrexOrderBookHistory(marketPair):

    my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)
    return my_bittrex.get_market_history(marketPair)





app = webapp2.WSGIApplication([
    ('/cron/orderbook', testOrderbook),
], debug=True)


