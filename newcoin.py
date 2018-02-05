import webapp2
import logging
import json
import requests
import sys
import traceback
from bittrex.bittrex import Bittrex
from google.appengine.ext import ndb
# from binance.client import Client
from google.appengine.api import mail


# Model: All Coin Markets
class CoinListings(ndb.Model):
    BittrexJson = ndb.JsonProperty(compressed=True)
    # BinanceJson = ndb.JsonProperty(compressed=True)
    RetrievedAt = ndb.DateTimeProperty(auto_now_add=True)

#
# Coin Listings
#
class testCoinListings(webapp2.RequestHandler):
    def get(self):
       checkNewCoins(self)

# Compare All Markets (Binance/Bittrex)
def checkNewCoins(self):

    # binance = Client('3QwoWiwJhgY1yW1XLx2cSdu9FPP5YlG6Jw9oQNTwJWdqmRJGdasDRktEIOzFuWNc', 'vWOASkjOXFrN4GwpbprclAz8hYk87vZ48J7L3AJ4xitllXJtPstdmwbrhJfC191B')
    bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)

    # Get all tradable currencies on Bittrex
    bittrexCurrencies = bittrex.get_currencies()['result']

    # Filter the result to contain only data we care about: name & symbol
    bittrexFilteredResult = list(map((lambda currency: { "name": currency['CurrencyLong'], "symbol": currency['Currency']}), bittrexCurrencies))

    # To-do: Get all tradable currencies on Binance
    # binance = Client('3QwoWiwJhgY1yW1XLx2cSdu9FPP5YlG6Jw9oQNTwJWdqmRJGdasDRktEIOzFuWNc', 'vWOASkjOXFrN4GwpbprclAz8hYk87vZ48J7L3AJ4xitllXJtPstdmwbrhJfC191B')

    # markets = binance.get_all_tickers()

    # # Create array of symbols
    # coins = [];
    # for market in markets:
    #   coins.append(market['symbol'])

    # # Filter out the excessive market strings
    # filteredSet = []
    # for coin in coins:
    #   filteredSet.append(coin.replace('BTC', '').replace('ETH', '').replace('BNB', '').replace('USDT', ''))

    # # print filteredSet
    # seen = set()
    # uniqueCoins = [marketCoin for marketCoin in filteredSet if marketCoin not in seen and not seen.add(marketCoin)]

    # uniqueCoins = filter(None, uniqueCoins) # fastest

    # # Since we removed BTC, ETH, BNB, USDT from the list, we need to add them again
    # uniqueCoins.append('BTC')
    # uniqueCoins.append('ETH')
    # uniqueCoins.append('BNB')
    # uniqueCoins.append('USDT')

    # print len(uniqueCoins)

    # Get the result from datastore for coin listings (will return one big blob of binance and bittrex coins)

    qry = CoinListings.query()

    if qry.get() == None:
      ent = CoinListings(BittrexJson=json.dumps(bittrexFilteredResult))

      # Update the entry in the datastore
      ent.put()
    else:
      # Get only the first result
      coinListings = qry.fetch(1)

      #  Iterate through the q
      coinListingId = coinListings[0].key.id()

      # Check for any differences
      if json.dumps(bittrexFilteredResult) == coinListings[0].BittrexJson:
        self.response.write('no new coins')
        message = mail.EmailMessage(
          sender="snstarosciak@gmail.com",
          subject="No new coins")

        message.to = "Stevie Starosciak <snstarosciak@gmail.com>"
        message.html = """<!DOCTYPE html>
                          <html>

                          <head>
                            <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
                            <meta content="width=device-width, initial-scale=1.0" name="viewport">
                            <title>LearnLoop - Added to a list</title>
                            <!--[if gte mso 10]>
                                <style>
                                  body, table, td { font-family: Arial, Helvetica, sans-serif !important;}
                                </style>
                              <![endif]-->
                            <style>
                              /* Client reset */
                                #outlook a{padding:0;}
                                .ReadMsgBody{width:100%;} .ExternalClass{width:100%;}
                                .ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div {line-height: 100%!important;}
                                body, table, td, p, a, li, blockquote{-webkit-text-size-adjust:100%; -ms-text-size-adjust:100%;}
                                table, td{mso-table-lspace:0pt; mso-table-rspace:0pt;}
                                img{-ms-interpolation-mode:bicubic;}
                                /* bring inline */
                                img {display: block; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;}
                                a img {border: none;}
                                a {text-decoration: none; color: #0DDDC2;} /* text link */

                                /* Responsive */
                                @media only screen and (max-device-width: 450px) {
                                  #content-wrapper, #body-wrapper {
                                    width: 100%!important;
                                  }
                                  .c-responsive-container {
                                    display: inline-block;
                                    width: 100%
                                    padding: 0 16px;
                                  }
                                  .c-table-responsive {
                                    width: 100%;
                                  }
                                  .button {
                                    width: 100%!important;
                                    max-width: 300px;
                                  }
                                }
                            </style>
                          </head>

                          <body style="font-family:'Helvetica Neue', 'Arial', sans-serif;width:100%;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;margin:0;padding:0;font-size:16px;line-height:24px">
                            <table cellspacing="0" cellpadding="0" border="0" width="100%" class="table" id="body-wrapper" style="border-collapse:collapse;table-layout:fixed;margin:0 auto;min-width:100% !important;width:100% !important">
                              <tr>
                                <td style="border-collapse:collapse">
                                  <table cellspacing="0" cellpadding="16px" border="0" width="100%" style="border-collapse:collapse;min-width:100% !important;width:100% !important">
                                    <tr>
                                      <td style="border-collapse:collapse">
                                        <table cellspacing="0" cellpadding="0" border="0" width="450" id="content-wrapper" align="center" style="border-collapse:collapse;table-layout:fixed;margin:0 auto">
                                          <tr>
                                            <td style="border-collapse:collapse;text-align:center;">
                                              <div>

                                                <h1 style="margin:0;font-size:18px;line-height:48px;color:#333333;font-weight:200;text-align:center;"><span style="font-weight:400">It looks there are some new coins available</h1>
                                                  <a target="_blank" style="color:#03A9F4;border-radius:3px;display:inline-block;font-size:16px;line-height:50px;height:50px;text-align:center;text-decoration:none;-webkit-text-size-adjust:none;mso-hide:all;color:#fefefe;width:250px;background-color: #38A883; color: #ffffff; width: 240px; height: 48px; line-height: 48px"
                                                    href="#">View list of coins</a>
                                              </div>
                                              <div>
                                            </div>
                                            </td>
                                          </tr>
                                        </table>
                                      </td>
                                    </tr>
                                  </table>
                                </td>
                              </tr>
                            </table>

                          </body>

                          </html>
          """

        message.send()
      else:
        self.response.write('a new coin emerges!')

      # To-do:Compare this result with the latest coin listings from Bittrex/Binance

      # To-do: Build a new entry that contains both Bittrex and Binance listings and store them in the datastore

      # Create an entity object for storing the data
      ent = CoinListings(id=coinListingId, BittrexJson=json.dumps(bittrexFilteredResult))

      # Update the entry in the datastore
      ent.put()


app = webapp2.WSGIApplication([
    ('/cron/newcoin', testCoinListings),
], debug=True)


