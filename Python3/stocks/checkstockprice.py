import yahoo_fin.stock_info as si

class stock:

    def getCurrentPrice(self, ticker):
        price = si.get_live_price(ticker)
        return price

    def getQuoteTable(ticket):
        qt = si.get_quote_table(ticker)
        return qt


