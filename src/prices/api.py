@app.post("/price/:symbol")
def update_price():
    # Update the price store with the user provided price
    # mimics incoming price feed
    pass


@app.get("/price/:symbol")
def get_price():
    # Gets the price of the given symbol
    pass
