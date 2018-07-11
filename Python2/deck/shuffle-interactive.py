#!/usr/bin/python
__author__ = "Tin Tran"

def shuffle(n):
  deck = range(1,n+1)
  #store the deck
  deckoriginal = []
  #copy the deck
  deckoriginal.extend(deck) 
  table =[]
  nrounds = 0
  while 1: 
    while len(deck) != 0:
      table.append(deck.pop(0))
      if len(deck) == 0:
        break
      deck.append(deck.pop(0))
    table.reverse() 
    deck = table
    table = []
    nrounds += 1
    if deck == deckoriginal:
      break
  return str(nrounds)

def main():
  n = raw_input("Enter the number of cards, enter Q to quit: ")
  while n.lower() != "q":
    n = int(n)
    print "The number of rounds is " + shuffle(n)
    n = raw_input("Enter the number of cards, enter Q to quit: ")

if __name__ == '__main__':
  main()
