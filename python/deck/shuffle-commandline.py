#!/usr/bin/python
__author__ = "Tin Tran"

import sys

def shuffle(n):
  #initialize deck
  deck = range(1,n+1)
  #make original deck
  deckoriginal = []
  deckoriginal.extend(deck) 
  #initialize table
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
  return nrounds

def main():
  n = int(sys.argv[1])
  print "The number of rounds is", shuffle(n)

if __name__ == '__main__':
  main()
