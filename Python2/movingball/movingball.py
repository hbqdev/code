import simpleguitk as simplegui

#Init globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20

start_pos = [WIDTH/2, HEIGHT/2]
vel = [0,3] # pixel per tick
time = 0

#Define timer
def tick():
  global time
  time = time + 1


def draw(canvas):
  #Create a list to  hold position
  ball_pos = [0,0]
  
  #calculate ball position
  ball_pos[0] = start_pos[0] + time + vel[0]
  ball_pos[1] = start_pos[1] + time + vel[1]
  

  #collide and reflect off of left hand side of canvas
  if ball_pos[0] <= BALL_RADIUS:
    vel[0] = -vel[0]
  #draw ball
  canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "white")

#create frame
frame = simplegui.create_frame("Moving ball", WIDTH, HEIGHT)

#Register event handler
frame.set_draw_handler(draw)

timer = simplegui.create_timer(100, tick)

frame.start()
timer.start()
