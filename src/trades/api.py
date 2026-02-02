
@app.post("/trades")
def on_trade(trade: Trade):
    # Update the trade store with the new trade
    # update the position Store accordingly
    pass

@app.get("/trades")
def get_trades():
    # Update the trade store with the new trade
    # update the position Store accordingly
    pass

@app.get("/price/:symbol")
def get_symbol_trades():
    pass