import asyncio
import json
from collections import defaultdict

from web_socket.message_parser import parseUserOrderChannelMessageForKindAndCurrency

class OrderService:
    ORDER_ID = 'order_id'
    ORDER_STATE = 'order_state'

    def __init__(self):
        self.orderBookView = defaultdict(lambda: defaultdict(dict))
        with open('order_book_view.JSON', 'w') as json_file:
            json.dump(self.orderBookView, json_file, indent=2)

    def updateOrderBookView(self, orderDetails, isInitialFill = False):
        if not isInitialFill:
            newOrderDetail = self.checkAndChangeStateForPartiallyFilledOrders(orderDetails)
            self.orderBookView[newOrderDetail[self.ORDER_STATE]][newOrderDetail[self.ORDER_ID]] = newOrderDetail
            for orderState in self.orderBookView.keys():
                if orderState != newOrderDetail[self.ORDER_STATE] and newOrderDetail[self.ORDER_ID] in self.orderBookView[orderState]:
                    del self.orderBookView[orderState][newOrderDetail[self.ORDER_ID]]
        else:
            for order in orderDetails:
                order = self.checkAndChangeStateForPartiallyFilledOrders(order)
                self.orderBookView[order[self.ORDER_STATE]][order[self.ORDER_ID]] = order
        self.printNumberOfOrdersOfEachOrderType()
        with open('order_book_view.JSON', 'w') as json_file:
            json.dump(self.orderBookView, json_file, indent=2)

    def checkAndChangeStateForPartiallyFilledOrders(self, orderDetails):
        if orderDetails['order_state'] == 'cancelled' and int(orderDetails['filled_amount']) > 0:
            orderDetails['order_state'] = 'partially_filled'
        return orderDetails

    # async def printOrderBookViewAtIntervals(self):
    #     while True:
    #         await self.printNumberOfOrdersOfEachOrderType()
    #         await asyncio.sleep(10)

    def printNumberOfOrdersOfEachOrderType(self):
        numberOfOpenOrders = len(self.orderBookView['open'].keys())
        numberOfFilledOrders = len(self.orderBookView['filled'].keys())
        numberOfPartiallyFilledOrders = len(self.orderBookView['partially_filled'].keys())
        numberOfCancelledOrders = len(self.orderBookView['cancelled'].keys())
        print(
            f'---> Order book view -> OPEN: {numberOfOpenOrders} | FILLED: {numberOfFilledOrders} | PARTIALLY_FILLED: {numberOfPartiallyFilledOrders} | CANCELLED: {numberOfCancelledOrders}')

    async def processWebSocketMessageUpdates(self, messageQueue):
        while True:
            message = await messageQueue.get()
            if 'method' in message and message['method'] == 'subscription':
                if 'channel' in message['params'] and message['params']['channel'] == 'user.orders.any.any.raw':
                    parsedMessage = parseUserOrderChannelMessageForKindAndCurrency(message['params']['data'])
                    self.updateOrderBookView(parsedMessage, False)