import asyncio
from order_service import OrderService
from web_socket.index import WebSocketClient
from dotenv import load_dotenv

async def main():
    # Load ENV variables
    load_dotenv()

    # WebSocket connection
    websocketClient = WebSocketClient()
    await websocketClient.connect()

    # Fetch and update existing orders in the view
    orderService = OrderService()
    orderService.updateOrderBookView(await websocketClient.fetchOpenOrdersForCurrency('BTC'), True)
    orderService.updateOrderBookView(
        await websocketClient.fetchFilledAndPartialFilledOrderHistoryForCurrency('BTC'), True)

    # Handle processing of message queue
    asyncio.create_task(websocketClient.handleWebSocketMessageQueue())
    asyncio.create_task(orderService.processWebSocketMessageUpdates(websocketClient.messageQueue))

    # Print view at intervals
    asyncio.create_task(orderService.printOrderBookViewAtIntervals())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()



