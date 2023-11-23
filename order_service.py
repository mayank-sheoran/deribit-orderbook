import asyncio
import json

from web_socket.message_parser import parseWsOpenOrderResponse, parseUserOrderChannelMessageForKindAndCurrency


class OrderService:
    def __init__(self):
        self.orderBookView = {}
        with open('order_book_view.JSON', 'w') as json_file:
            json.dump(self.orderBookView, json_file, indent=2)

    def updateOrderBookView(self, orderDetails, isInitialFill = False):
        if not isInitialFill:
            orderDetails = self.checkAndChangeStateForPartiallyFilledOrders(orderDetails)
            isNewOrder = True
            if orderDetails['order_state'] not in self.orderBookView:
                self.orderBookView[orderDetails['order_state']] = []
            for idx, existingOrder in enumerate(self.orderBookView[orderDetails['order_state']]):
                if existingOrder['order_id'] == orderDetails['order_id']:
                    isNewOrder = False
                    self.orderBookView[idx] = orderDetails
            if isNewOrder:
                self.orderBookView[orderDetails['order_state']].append(orderDetails)
                self.manageOrderStateChangeInOrderBookView(orderDetails['order_id'], orderDetails['order_state'])
        else:
            for order in orderDetails:
                order = self.checkAndChangeStateForPartiallyFilledOrders(order)
                if order['order_state'] not in self.orderBookView:
                    self.orderBookView[order['order_state']] = []
                self.orderBookView[order['order_state']].append(order)
        self.sortOrderViewByTimeStamp()
        with open('order_book_view.JSON', 'w') as json_file:
            json.dump(self.orderBookView, json_file, indent=2)

    def checkAndChangeStateForPartiallyFilledOrders(self, orderDetails):
        if orderDetails['order_state'] == 'cancelled' and int(orderDetails['filled_amount']) > 0:
            orderDetails['order_state'] = 'partially_filled'
        return orderDetails

    def manageOrderStateChangeInOrderBookView(self, orderId, newOrderState):
        for orderState in self.orderBookView.keys():
            if orderState == newOrderState:
                continue
            filteredExistingOrders = []
            for idx, existingOrder in enumerate(self.orderBookView[orderState]):
                if existingOrder['order_id'] == orderId:
                    continue
                filteredExistingOrders.append(existingOrder)
            self.orderBookView[orderState] = filteredExistingOrders

    def sortOrderViewByTimeStamp(self):
        for orderState in self.orderBookView.keys():
            existingOrders = self.orderBookView[orderState]
            self.orderBookView[orderState] = sorted(existingOrders, key=lambda x: x['creation_timestamp'],
                                                    reverse=True)

    async def printOrderBookViewAtIntervals(self):
        while True:
            print("ORDER BOOK VIEW", self.orderBookView)
            await asyncio.sleep(20)

    async def processWebSocketMessageUpdates(self, messageQueue):
        while True:
            message = await messageQueue.get()
            if 'method' in message and message['method'] == 'subscription':
                if 'channel' in message['params'] and message['params']['channel'] == 'user.orders.any.any.raw':
                    parsedMessage = parseUserOrderChannelMessageForKindAndCurrency(message['params']['data'])
                    self.updateOrderBookView(parsedMessage)
