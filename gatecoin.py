# available apis action
# GET Balance/Balances
# POST Trade/Orders

import time
import base64
import hmac
import urllib
import requests
import hashlib
import json

debug = False

class Gatecoin:
  def __init__(self):
      self.key = ""
      self.secret = ""
      self.apiUrl = "https://api.gatecoin.com/"
      
  
  def _send_request(self, command, httpMethod, params={}):          
      now = str(time.time())
      contentType = "" if httpMethod == "GET" else "application/json"
  
      if command == "MarketDepth":
          url = self.apiUrl + "Public/" + command + "/" + self.market
      else:
          url = self.apiUrl + command
  
      message = httpMethod + url + contentType + now
      message = message.lower()
  
      signature = hmac.new(self.secret.encode(), msg=message.encode(), digestmod=hashlib.sha256).digest()
      hashInBase64 = base64.b64encode(signature, altchars=None)

      headers = {
      'API_PUBLIC_KEY': self.key,
      'API_REQUEST_SIGNATURE': hashInBase64,
      'API_REQUEST_DATE': now,
      'Content-Type':'application/json'
      }

      data = None

      if httpMethod == "DELETE":
          R = requests.delete
      elif httpMethod == "GET":
          R = requests.get
      elif httpMethod == "POST":
          R = requests.post          
      data = json.dumps(params)
      if(debug == True):
        print("command: %r" % command)
        print("url: %r" % url)
        print("headers: %r" % headers)
        print("params: %r" % params)
        print("message: %r" % message)
        print("data: %r\n" % data)

      response = R(url, data=data, headers=headers)
      if(debug == True):
        print("response: %r\n" % response.content)

      return response.json()


  def buy(self, amount, price):
      return self.place_order(str(amount), str(price), "BID")


  def sell(self, amount, price):
      return self.place_order(str(amount), str(price), "ASK")


  def place_order(self, amount, price, type):
      data = {'Code': 'BTCUSD', 'Way': type, 'Amount': amount, 'Price': price}
      return self._send_request("Trade/Orders", "POST", data)


  def get_balance(self, currency):
      return self._send_request("Balance/Balances/"+currency, "GET")


  def get_order(self):
      return self._send_request("Trade/Orders", "GET")


