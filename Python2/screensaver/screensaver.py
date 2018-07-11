import simpleguitk as simplegui
import random

message = "Python is awesome!"
position = [50,50]
width = 500
height = 500
interval = 1000

def update(text):
  global message
  message = text

def tick():
  global position 
  x = random.randrange(0, width)
  y = random.randrange(0, height)
  position[0] = x
  position[1] = y

def draw(canvas):
  canvas.draw_text(message, position, 36, "red")

frame = simplegui.create_frame("Home", width, height)

text = frame.add_input("Mesage:", update, 150)
frame.set_draw_handler(draw)
frame.add_button("Click me", tick)
timer = simplegui.create_timer(interval, tick)

frame.start()
timer.start()
