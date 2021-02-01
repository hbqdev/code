import yahoo_fin.stock_info as si
from finvizfinance.quote import finvizfinance as ff

def CheckStock(price, capital, pr, rps):
    shares = ((float(capital)*pr)/0.70)
    print(capital)
    print(float(capital)*pr)
    print("Number of shares to buy: " + str(shares))
    pt2 = rps * 2 + price
    pt3 = rps * 3 + price
    pt4 = rps * 4 + price
    print("Profit target 2x is : \n" + str(pt2))
    print("Profit target 3x is : \n" + str(pt3))
    print("Profit target 4x is : \n" + str(pt4))



def Main():
    ticker = input("enter the Ticker: \n")
    price = si.get_live_price(ticker)
    print("Current price of " + ticker + "is : " + str(price))
    capital = input("enter capital: \n")

    pcr = input("Enter your percentage risk : \n")
    pr = float(pcr)/100.0

    stoploss = input("enter stop loss: \n")

    rps = price - float(stoploss)

    CheckStock(price, capital, pr, rps)

        
if __name__ == '__main__' :
    Main()