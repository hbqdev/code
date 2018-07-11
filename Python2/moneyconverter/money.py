"""
Interative application of money conversion from float to string"
"""
import simpleguitk as simplegui

#define global value
value = 3.12

#Handle single quantity
def convert_unit(val, name):
  money = str(val) + " " + name
  if val > 1:
    money = money + "s"
  return money

#convert xx.yy to xx dollars and yy cents
def convert(val):
  dollars = int(val)
  cents = round (100* (val-dollars))
  
  #convert to strings
  dollars_string = convert_unit(dollars, "dollar")
  cents_string = convert_unit(cents, "cent")
  
  # return the total string
  if dollars == 0 and cents == 0:
     return "Sorry you're broke!"
  elif dollars == 0:
     return cents_string
  elif cents == 0:
     return dollars_string
  else:
     return dollars_string + " and " + cents_string

# define draw handler
def draw(canvas):
  canvas.draw_text(convert(value), [60,100], 24, "white")

# define an input field handler
def input_handler(text):
  global value
  value = float(text)

# create frame

frame = simplegui.create_frame("Converter", 600, 600)
frame.set_draw_handler(draw)
frame.add_input("Enter value", input_handler, 100)

# start frame
frame.start()
