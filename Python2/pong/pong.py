# Implementation of classic arcade game Pong

import simpleguitk as simplegui
import random
# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 1200
HEIGHT = 600       
BALL_RADIUS = 15
PAD_WIDTH = 6
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
score1 = 0
score2 = 0
ball_pos = [WIDTH/2, HEIGHT/2]
 # pixel per tick
pad1_pos = HEIGHT/2
pad2_pos = HEIGHT/2
vel = [1,random.randrange(60, 180)/60]

background = simplegui.load_image("http://wonderfulengineering.com/wp-content/uploads/2013/12/metal-wallpapers-1.jpg")
paddle_img = simplegui.load_image("https://dl.dropboxusercontent.com/u/8367729/codeskulptor/pong/paddle.png")
#hit_sound = simplegui.load_sound("http://rpg.hamsterrepublic.com/wiki-images/d/d7/Oddbounce.ogg")
#sound_border = simplegui.load_sound('http://rpg.hamsterrepublic.com/wiki-images/2/21/Collision8-Bit.ogg')

# initialize ball_pos and ball_vel for new bal in middle of table
def ball(direction):
  global ball_pos # these are vectors stored as lists
  ball_pos = [WIDTH/2, HEIGHT/2]
  pad1_pos = HEIGHT/2
  pad2_pos = HEIGHT/2
  if direction == 1:
    vel[0] = -random.randrange(120, 240)/60
  elif direction == 0 :
    vel[0] = random.randrange(120, 240)/60

# define event handlers
def reset():
    global pad1_pos, pad2_pos, pad1_vel, pad2_vel  # these are numbers
    global score1, score2  # these are ints
    pad1_pos = HEIGHT/2
    pad2_pos = HEIGHT/2
    pad1_vel = 0
    pad2_vel = 0
    ball(random.randrange(0,2))
    pass
    
def draw(canvas):
  global score1, score2, pad1_pos, pad2_pos, ball_vel, pad1_vel, pad2_vel
  canvas.draw_image(background, (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT), 
                     (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT))
  #update paddles
  if pad1_pos < (HALF_PAD_HEIGHT) and pad1_vel < 0:
      pad1_vel = 0
  if pad2_pos < (HALF_PAD_HEIGHT) and pad2_vel < 0:
      pad2_vel = 0
  if pad1_pos > (HEIGHT - (HALF_PAD_HEIGHT)) and pad1_vel > 0:
      pad1_vel = 0
  if pad2_pos > (HEIGHT - (HALF_PAD_HEIGHT)) and pad2_vel > 0:
      pad2_vel = 0    
  pad1_pos += pad1_vel
  pad2_pos += pad2_vel
        
  # draw mid line and gutters
  canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
  #canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
  #canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
       
  # update ball
  if ball_pos[1] >= (HEIGHT - BALL_RADIUS) or ball_pos[1] <= (BALL_RADIUS):
      vel[1] = -vel[1]
      #sound_border.play()
            
  if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
    if ball_pos[1] <= pad1_pos + HALF_PAD_HEIGHT and ball_pos[1] >= pad1_pos-HALF_PAD_HEIGHT:
      vel[0] = -vel[0]*1.1
      #hit_sound.rewind()
      #hit_sound.play()
    else:
      ball(random.randrange(0,2))
      score2 +=1
  elif ball_pos[0] >= (WIDTH) - BALL_RADIUS-PAD_WIDTH:
    if ball_pos[1]<=pad2_pos + HALF_PAD_HEIGHT and ball_pos[1] >= pad2_pos-HALF_PAD_HEIGHT:
      vel[0] = -vel[0]*1.1
      #hit_sound.rewind()
      #hit_sound.play()
    else:
      ball(random.randrange(0,2))
      score1+=1
            
  ball_pos[0] +=  vel[0]
  ball_pos[1] +=  vel[1]

  # draw ball
  canvas.draw_circle(ball_pos,BALL_RADIUS, 1, ball_image(), ball_image())
  # update paddle's vertical position, keep paddle on the screen
    

  # draw paddles
  canvas.draw_polygon([(0, pad1_pos-HALF_PAD_HEIGHT), (0, pad1_pos+HALF_PAD_HEIGHT), (PAD_WIDTH, pad1_pos+HALF_PAD_HEIGHT),
                     (PAD_WIDTH,pad1_pos-HALF_PAD_HEIGHT)], 1, "red","red")
  canvas.draw_polygon([(WIDTH, pad2_pos-HALF_PAD_HEIGHT), (WIDTH, pad2_pos+HALF_PAD_HEIGHT), 
                     (WIDTH-PAD_WIDTH, pad2_pos+HALF_PAD_HEIGHT),(WIDTH-PAD_WIDTH,pad2_pos-HALF_PAD_HEIGHT)], 1, "red","red")
  
  #canvas.draw_image(paddle_img, 
  #                  (HALF_PAD_WIDTH, HALF_PAD_HEIGHT), (PAD_WIDTH, PAD_HEIGHT), 
  #                  (HALF_PAD_WIDTH, pad1_pos), (PAD_WIDTH, PAD_HEIGHT))
  #canvas.draw_image(paddle_img, 
  #                   (HALF_PAD_WIDTH, HALF_PAD_HEIGHT), (PAD_WIDTH, PAD_HEIGHT), 
  #                   (WIDTH - HALF_PAD_WIDTH, pad2_pos), (PAD_WIDTH, PAD_HEIGHT))  
  # draw scores
  canvas.draw_text(str(score1), [WIDTH/4,50], 30, "White")
  canvas.draw_text(str(score2), [WIDTH*0.75,50], 30, "White")
    
def ball_image():
  colors = ["Aqua","Blue","Fuchsia", "Gray", "Green" , "Lime", 
            "Maroon", "Navy", "Olive", "Orange",
            "Purple", "Red","Silver", "Teal","White", "Yellow"]
  i = random.randrange(0,len(colors))
  return colors[i]

def keydown(key):
  global pad1_vel, pad2_vel
  if key == simplegui.KEY_MAP['w']:
      pad1_vel = -5
  elif key == simplegui.KEY_MAP['s']:
      pad1_vel = 5
  elif key == simplegui.KEY_MAP['up']:
      pad2_vel = -5
  elif key == simplegui.KEY_MAP['down']:
      pad2_vel = 5
                    
def keyup(key):
  global pad1_vel, pad2_vel
  if key == simplegui.KEY_MAP['w']:
      pad1_vel = 0
  elif key == simplegui.KEY_MAP['s']:
      pad1_vel = 0
  elif key == simplegui.KEY_MAP['up']:
      pad2_vel = 0
  elif key == simplegui.KEY_MAP['down']:
      pad2_vel = 0 

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", reset, 100)

# start frame
reset()
frame.start()

