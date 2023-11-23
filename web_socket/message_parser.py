# {"is_rebalance": false, "risk_reducing": false, "order_type": "limit", "contracts": 1.0,
#  "creation_timestamp": 1700710198916, "order_state": "open", "average_price": 0.0,
#  "time_in_force": "good_til_cancelled", "filled_amount": 0.0, "max_show": 0.0001, "order_id": "BTC_USDT-3673018",
#  "post_only": false, "last_update_timestamp": 1700710198916, "replaced": false, "web": true, "api": false,
#  "direction": "buy", "mmp": false, "instrument_name": "BTC_USDT", "amount": 0.0001, "price": 33000.4945, "label": ""}
def parseWsOpenOrderResponse(orders):
    parsedOrders = []
    for order in orders:
        parsedOrders.append({
            "instrument_name": order['instrument_name'],
            "amount": order['amount'],
            "price": order['price'],
            "order_id": order['order_id'],
            "filled_amount": order['filled_amount'],
            "order_state": order['order_state'],
            "creation_timestamp": order['creation_timestamp'],
        })
    return parsedOrders


# {'is_rebalance': False, 'risk_reducing': False, 'order_type': 'market', 'contracts': 1.0,
#  'creation_timestamp': 1700720094893, 'order_state': 'filled', 'average_price': 33601.1452,
#  'time_in_force': 'good_til_cancelled', 'filled_amount': 0.0001, 'max_show': 0.0001, 'order_id': 'BTC_USDT-3677714',
#  'post_only': False, 'last_update_timestamp': 1700720094893, 'replaced': False, 'web': True, 'api': False,
#  'direction': 'buy', 'mmp': False, 'instrument_name': 'BTC_USDT', 'amount': 0.0001, 'price': 41018.445, 'label': ''}
#

def parseUserOrderChannelMessageForKindAndCurrency(data):
    return {
        "instrument_name": data['instrument_name'],
        "amount": data['amount'],
        "price": data['price'],
        "order_id": data['order_id'],
        "filled_amount": data['filled_amount'],
        "order_state": data['order_state'],
        "creation_timestamp": data['creation_timestamp'],
    }


# {'jsonrpc': '2.0', 'id': 4, 'result': [
#     {'is_rebalance': False, 'risk_reducing': False, 'order_type': 'market', 'contracts': 1.0,
#      'creation_timestamp': 1700720094893, 'order_state': 'filled', 'average_price': 33601.1452,
#      'time_in_force': 'good_til_cancelled', 'filled_amount': 0.0001, 'max_show': 0.0001, 'order_id': 'BTC_USDT-3677714',
#      'post_only': False, 'last_update_timestamp': 1700720094893, 'replaced': False, 'web': True, 'api': False,
#      'direction': 'buy', 'mmp': False, 'instrument_name': 'BTC_USDT', 'amount': 0.0001, 'price': 41018.445,
#      'label': ''}, {'is_rebalance': False, 'risk_reducing': False, 'order_type': 'limit', 'contracts': 1.0,
#                     'creation_timestamp': 1700710189273, 'order_state': 'filled', 'average_price': 33601.1452,
#                     'time_in_force': 'good_til_cancelled', 'filled_amount': 0.0001, 'max_show': 0.0001,
#                     'order_id': 'BTC_USDT-3673013', 'post_only': False, 'last_update_timestamp': 1700710189273,
#                     'replaced': False, 'web': True, 'api': False, 'direction': 'buy', 'mmp': False,
#                     'instrument_name': 'BTC_USDT', 'amount': 0.0001, 'price': 34000.4945, 'label': ''}],
#  'usIn': 1700754599041877, 'usOut': 1700754599042838, 'usDiff': 961, 'testnet': True}


def parseWsOrderHistoryResponse(orders):
    parsedOrders = []
    for order in orders:
        parsedOrders.append({
            "instrument_name": order['instrument_name'],
            "amount": order['amount'],
            "price": order['price'],
            "order_id": order['order_id'],
            "filled_amount": order['filled_amount'],
            "order_state": order['order_state'],
            "creation_timestamp": order['creation_timestamp'],
        })
    return parsedOrders
