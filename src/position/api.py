@app.get("/positions/:symbol")
def get_symobol_position():
    # Update the price store with the user provided price
    # mimics incoming price feed
    pass

@app.get("/positions")
def get_all_positions():
    pass