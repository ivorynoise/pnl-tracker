# PNL Tracker
\
I implemented average-cost as the primary PnL method for simplicity and clarity, and included a FIFO alternative for use cases requiring tax-accurate lot tracking



I used Average Cost (Weighted Average) method.

Here's how it works in the code:

When adding to a position:

# Adding to long position - update avg price
total_cost = (position.quantity * position.avg_price) + (trade.quantity * trade.price)
position.quantity += trade.quantity
position.avg_price = total_cost / position.quantity

The average price is recalculated as a weighted average each time you add to the position.


-----

The floating point precision issue is a classic problem. For financial calculations, you should use Decimal instead of float


--
mention about tests and 

--- 
I did not consider any push based updates like Real time pnl over websocket. The design and engineering decisions will change if we have to incorporate such features. 