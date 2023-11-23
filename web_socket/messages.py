import json
import os


def getAuthMessage(requestId):
    clientId = os.environ.get("CLIENT_ID")
    clientSecret = os.environ.get("CLIENT_SECRET")
    return json.dumps({
        "jsonrpc": "2.0",
        "id": requestId,
        "method": "public/auth",
        "params": {
            "grant_type": "client_credentials",
            "client_id": clientId,
            "client_secret": clientSecret
        }
    })

def getOpenOrdersByCurrencyMessage(requestId, currency):
    return json.dumps({
      "jsonrpc" : "2.0",
      "id" : requestId,
      "method" : "private/get_open_orders_by_currency",
      "params" : {
        "currency" : currency
      }
    })

def getOrderHistoryByCurrencyMessage(requestId, currency, kind = 'any', count = 100):
    return json.dumps({
      "jsonrpc" : "2.0",
      "id" : requestId,
      "method" : "private/get_order_history_by_currency",
      "params" : {
        "currency" : currency,
        "kind" : kind,
        "count" : count
      }
    })

def getOrderForKindAndCurrencyMessage(requestId, kind, currency):
    return json.dumps({
        "jsonrpc": "2.0",
         "method": "private/subscribe",
         "id": requestId,
         "params": {
            "channels": ["user.orders." + kind + "." + currency + ".raw"]}
        })
