import yahoo_fin.stock_info as si

apl = si.get_quote_table("aapl")
amd = si.get_stats_valuation("amd")

print("This is Apple's Stock price: " + str(apl))
print("This is AMD's analyst's info: \n") 
print(amd)

