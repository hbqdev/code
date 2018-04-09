import simpleguitk as simplegui

# define draw handler
def draw(canvas):
  canvas.draw_text("Hello World!", [100, 100], 12, "red")
  canvas.draw_circle([100,100],2,2,"red")
#make a frame
frame = simplegui.create_frame("My Frame", 300, 300)

#register draw handler
frame.set_draw_handler(draw)


frame.start()
