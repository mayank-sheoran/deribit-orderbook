import asyncio
import json

import websockets

from web_socket.message_parser import parseWsOpenOrderResponse, parseWsOrderHistoryResponse
from web_socket.messages import getAuthMessage, getOpenOrdersByCurrencyMessage, \
    getOrderForKindAndCurrencyMessage, getOrderHistoryByCurrencyMessage

webSocketURL = 'wss://test.deribit.com/ws/api/v2'

class WebSocketClient:
    def __init__(self):
        self.websocket = None
        self.reconnect_interval = 10
        self.requestId = 0
        self.messageQueue = asyncio.Queue()

    async def connect(self):
        while True:
            try:
                self.websocket = await websockets.connect(webSocketURL)
                print("-> WebSocket connected")
                await self.authenticate()
                await self.subscribeToOrderForKindAndCurrencyChannel('any', 'any')
                break
            except Exception as e:
                print(f"WebSocket connection error: {e}")
                print(f"Reconnecting in {self.reconnect_interval} seconds...")
                await asyncio.sleep(self.reconnect_interval)

    async def authenticate(self):
        self.requestId += 1
        await self.websocket.send(getAuthMessage(self.requestId))
        authResponse = json.loads(await self.websocket.recv())
        if authResponse['result']['refresh_token'] != '':
            print("-> WebSocket Authenticated")

    async def fetchOpenOrdersForCurrency(self, currency):
        self.requestId += 1
        await self.websocket.send(getOpenOrdersByCurrencyMessage(self.requestId, currency))
        openOrderWsResponse = json.loads(await self.websocket.recv())
        print('-> Fetched all open orders.')
        return parseWsOpenOrderResponse(openOrderWsResponse['result'])

    async def fetchFilledAndPartialFilledOrderHistoryForCurrency(self, currency):
        self.requestId += 1
        await self.websocket.send(getOrderHistoryByCurrencyMessage(self.requestId, currency))
        orderHistoryWsResponse = json.loads(await self.websocket.recv())
        print('-> Fetched all filled and partially filled orders.')
        return parseWsOrderHistoryResponse(orderHistoryWsResponse['result'])

    async def subscribeToOrderForKindAndCurrencyChannel(self, kind, currency):
        self.requestId += 1
        await self.websocket.send(getOrderForKindAndCurrencyMessage(self.requestId, kind, currency))
        response = json.loads(await self.websocket.recv())
        if 'result' in response and response['result'] != []:
            print('-> Subscribed to Order For Kind and Currency Channel')
        else:
            print('Failed to subscribed to Order For Kind and Currency Channel')

    async def handleWebSocketMessageQueue(self):
        while True:
            message = await self.websocket.recv()
            data = json.loads(message)
            await self.messageQueue.put(data)
            await asyncio.sleep(1)

