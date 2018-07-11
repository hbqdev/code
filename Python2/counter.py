import simpleguitk as simplegui

counter = 0

def increment ():
  global counter
  counter = counter + 1

def tick ():
  increment()
  print counter

def buttonpress():
  global counter
  counter = 0


frame = simplegui.create_frame("SimpleGUI Test", 500,500)
frame.add_button("click me", tick)
timer = simplegui.create_timer(10, buttonpress)

frame.start()
timer.start()

