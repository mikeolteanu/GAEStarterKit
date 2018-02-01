import webapp2
import logging
import json
import requests
import sys
import traceback

class testPyWaves(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        payload = {"asset2": "WAVES", "asset1": "AnERqFRffNVrCbviXbDEdzrU6ipXCP5Y1PKpFdRnyQAy","privateKey": "2ekkyJmCKagiaFBJ94cuP3pn8oHJPAytMuCJGgSpxxdM"}
        url = "ec2-52-36-3-139.us-west-2.compute.amazonaws.com:3000/api/waves/assetpairs/all"
        headers = {'content-type': 'application/json'}
        logging.info("sending pywaves test:")
        logging.info(payload)
        try:
            resp = requests.post(url, data=json.dumps(payload), headers=headers)
            self.response.write(resp.text)
        except Exception as inst:
            self.response.write("Request Failed. " + "{0}".format(sys.exc_info()[0]) + " {0}".format(traceback.format_exc()))

app = webapp2.WSGIApplication([
    ('/pywaves', testPyWaves),
], debug=True)


