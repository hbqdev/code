import yahoo_fin.stock_info as si
from finvizfinance.quote import finvizfinance as ff

def CheckStock():

    while True:
        ticker = input("Please enter the Ticker's name or q || quit to quit: " )
        if str.casefold(ticker) == ('q' or 'quit'):
            break
        try:
            print("Current price of " + ff(ticker).TickerFundament().get("Company") + "is " + str(si.get_live_price(ticker)))
            #print("Ticker's current price is \n " )
            #print(si.get_quote_table(ticker))
        except:
            print("Ticker doesn't exists or cannot be found, please try a different Ticker")

def buildWatchList():

    while True:
         typeofwatch = input("Long or Short? \n")
         if str.casefold(typeofwatch) == ("long" or "l"):
             longfile = 'LongWatch.txt'
             with open(file, 'w') as writetofile:
                 writetofile.write()

def Main():
    while True:
        print("Please choose from the options below: \n")
        print("'chst || checkstock' - Check current stock price of a Ticker \n")
        print("'cal || calculations' - Calculate how many stocks to buy \n")
        print("'bwl || buildwatchlist' - Build Stocks Watchlist \n")
        ip = input("Enter your option or quit: \n")

        if str.casefold(ip) == ('q' or 'quit'):
            break

        elif str.casefold(ip) == ('chst' or 'checkstock'):
            CheckStock()
        
if __name__ == '__main__' :
    Main()