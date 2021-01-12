import argparse 

def StockCal(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a+b
    return a

def Main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action = "store_true")
    parser.add_argument("num", help = "The number to calculate the stocks stop loss", type = int)
    parser.add_argument("-o", "--output", help = "output stocks to a file", action = "store_true")

    args = parser.parse_args()
    result = StockCal(args.num)
    if args.verbose:
        print("The stock bought at " + str(args.num) +  " and stop loss is " + str(result)) 
    elif args.quiet:
        print(result)
    else:
        print("Stock(" + str(args.num) + ") = " + str(result))

    if args.output:
        f = open("stockstowatch", "a")
        f.write(str(result)+'\n')
        f.close()


if __name__ == '__main__':
    Main()
