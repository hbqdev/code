import simpleguitk as  simplegui

store = 0
operand = 0

def output():
  print "Store = ", store
  print "Operand = ", operand

def swap():
  global store, operand
  store, operand = operand, store

def add():
  global store, operand
  store = store + operand
  output()

def substract():
  global store, operand
  store = store - operand
  output()

def multiply():
  global store, operand
  store = store * operand
  output()

def divide():
  global store, operand
  store = store / operand
  output()

def input(inp):
  global operand
  operand = float(inp)
  output()
  
frame = simplegui.create_frame("Calculator", 200, 200)
frame.add_button("Print", output, 100)
frame.add_button("Swap", swap, 100)
frame.add_button("Add", add, 100)
frame.add_button("Sub", substract, 100)
frame.add_button("Multiply", multiply, 100)
frame.add_button("divide", divide, 100)
frame.add_input("Enter value", input, 100)
frame.start()
