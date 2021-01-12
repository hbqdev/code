from string import Template

class myStock(Template):
    delimiter = '#'

def Main():
    cart = []
    cart.append(dict(item="Ticker", price=8,qty=2))
    cart.append(dict(item="Volumes",price=9,qty=3))
    cart.append(dict(item="Trend",price=32,qty=5))

    tmpl = myStock("#qty x #item = #price")
    total = 0

    print("Stocks to buy:")
    for data in cart:
        print(tmpl.safe_substitute(data))
        total += data["price"]

    print("Price to buy: " +str(total))

if __name__ == '__main__' :
    Main()
