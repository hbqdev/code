import simpleguitk as simplegui

#initialize globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20

ball_pos = [WIDTH/2, HEIGHT/2]
velocity = [0 , 0]

def draw(canvas):
  ball_pos[0] += velocity[0]
  ball_pos[1] += velocity[1]
  canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "red", "white")
#define event handler

def keydown(key):
  vel = 4
  if key == simplegui.KEY_MAP["left"]:
    velocity[0] -= vel
  elif key == simplegui.KEY_MAP["right"]:
    velocity[0] += vel
  elif key == simplegui.KEY_MAP["up"]:
    velocity[1] -= vel
  elif key == simplegui.KEY_MAP["down"]:
    velocity[1] += vel

#create frame
frame = simplegui.create_frame("Position ball control", WIDTH, HEIGHT)

#Register event handler
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)

#start frame
frame.start()
