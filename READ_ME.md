# Deribit Order Book

[Demo Video](https://www.youtube.com/watch?v=gO-DkYLoGXw)

### What is achieved:

1. Connected to Deribit private websocket using authentication (fallback retry connection mechanism is also added).
2. On program startup fetching **open / filled / partial_filled** orders from following api's ->
   - ***private/get_open_orders_by_currency***
   - ***private/get_order_history_by_currency***
3. Subscribing to the websocket channel for ***user.order.{kind}.{currency}***
   - Reason behind this was not to do polling and instead rely on event based mechanism.
   - Made the Message Queue which manages the channel messages.
4. Maintained the Order book view in a Hash data structure which is then dumped into a JSON file for better visibility for testing the program.
   - If for any order_id, order state is changed then accordingly that order will be deleted from the previous order state and added to the new order state in the view. Example open order when cancelled or filled, it will be removed from open orders and added to corresponding state.
   - Will make the initial order view from the api's mentioned above, after that based on the websocket channel message events new order or old order modifications requests will be processed to build the updated order view.
5. Changes made to the order book view data structure are instant on the basis of websocket channel message event but pushing data to JSON file might take sometime to get reflected.

### What could have been achieved :

- Fetching the cancelled orders also during the program startup. I was not able to find the API for the same in the documentation but i am sure there would be ways to achieve the same but implementation wise it would have been similar as done for other kind of orders.
- Code could have been implemented in a more better way by use of ENUMS / constants / data type definations etc. But for simplicity sake chose to keep balance b/w readability and development speed.
- Could have maintained the database itself for the view but for simplicity i am flushing the order book data structure data to JSON file for better visibility.

