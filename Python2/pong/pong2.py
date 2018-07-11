#works in codeskulptor.org

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 1000
HEIGHT = 500      
BALL_RADIUS = 20
PAD_WIDTH = 20
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
face_off_circle_radius = 110
face_off_dot_radius = 15
paddle1_pos = [0, (HEIGHT/2) - 30]
paddle2_pos = [0, (HEIGHT/2) - 30]
paddle1_vel = [0,0]
paddle2_vel = [0,0]
player_right_score = 0
player_left_score = 0

# helper function that spawns a ball, returns a position vector and a velocity vector
def helper():
    global start_movement
    start_movement = random.randrange(1,3)
   
    ball_init(start_movement)
   
# if right is True, spawn to the right, else spawn to the left
def ball_init(start_movement):
    global ball_pos, ball_vel # these are vectors stored as lists
       
    # initally ball moves Right
    if start_movement == 1:
        x_ball_vel = random.randrange(1, 5)
        y_ball_vel = random.randrange(1, 5)
        ball_vel = [x_ball_vel, y_ball_vel]
       
       
    # initally ball moves left
    if start_movement == 2:
        x_ball_vel = random.randrange(-5, -1)
        y_ball_vel = random.randrange(-5, -1)
        ball_vel = [x_ball_vel, y_ball_vel]
       
       
# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    pass

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel
    global player_right_score, player_left_score
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[0] += paddle1_vel[0]
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[0] += paddle2_vel[0]
    paddle2_pos[1] += paddle2_vel[1]
   
    if paddle1_pos[1] > HEIGHT - PAD_HEIGHT:
        paddle1_vel[1] = 0
    if paddle1_pos[1] < 0:
        paddle1_vel[1] = 0
    if paddle2_pos[1] > HEIGHT - PAD_HEIGHT:
        paddle2_vel[1] = 0
    if paddle2_pos[1] < 0:
        paddle2_vel[1] = 0   
    # draw mid line, gutters, blue lines, face off circles
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 2, "red")
    c.draw_line([WIDTH / 2 + 125, 0],[WIDTH / 2 + 125, HEIGHT], 2, "blue") #blue line right
    c.draw_line([WIDTH / 2 - 125, 0],[WIDTH / 2 - 125, HEIGHT], 2, "blue") #blue line left
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "red") # gutter left
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "red") #gutter right
    c.draw_circle([WIDTH/2, HEIGHT/2], face_off_circle_radius, 1, 'red') #middle circle
    c.draw_circle([WIDTH/2, HEIGHT/2], face_off_dot_radius, 1, 'red', 'red') #middle circle dot
    c.draw_circle([WIDTH/4 -100, HEIGHT/4], face_off_circle_radius, 1, 'red') #faceoff circle left top
    c.draw_circle([WIDTH/4 -100, HEIGHT/4], face_off_dot_radius, 1, 'red', 'red') #faceoff dot left top
    c.draw_circle([WIDTH/4 -100, (HEIGHT/4)*3], face_off_circle_radius, 1, 'red') #faceoff circle left bottom
    c.draw_circle([WIDTH/4 -100, (HEIGHT/4)*3], face_off_dot_radius, 1, 'red', 'red') #faceoff dot left bottom
    c.draw_circle([(WIDTH/4)*3 +100, HEIGHT/4], face_off_circle_radius, 1, 'red') #faceoff circle right top
    c.draw_circle([(WIDTH/4)*3 +100, HEIGHT/4], face_off_dot_radius, 1, 'red', 'red') #faceoff dot right top
    c.draw_circle([(WIDTH/4)*3 +100, (HEIGHT/4)*3], face_off_circle_radius, 1, 'red') #faceoff circle right bottom
    c.draw_circle([(WIDTH/4)*3 +100, (HEIGHT/4)*3], face_off_dot_radius, 1, 'red', 'red') #faceoff dot right bottom
    c.draw_text((str(player_left_score)), [(WIDTH/3), HEIGHT/6], 40, 'green')
    c.draw_text((str(player_right_score)), [(WIDTH/3)*2, HEIGHT/6], 40, 'green')
    c.draw_text('Pong was built by Samantha Taffer March 10th 2013', [50, HEIGHT - 10], 15, 'black')
   
    # draw paddles
    c.draw_polygon([[0, paddle1_pos[1]], [0, paddle1_pos[1] + PAD_HEIGHT],[PAD_WIDTH, paddle1_pos[1] + PAD_HEIGHT], [PAD_WIDTH, paddle1_pos[1]]], 2, 'black', 'black') #left paddle
    c.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos[1] ], [WIDTH - PAD_WIDTH, paddle2_pos[1] + PAD_HEIGHT],[WIDTH, paddle2_pos[1] + PAD_HEIGHT], [WIDTH, paddle2_pos[1]]], 2, 'black', 'black') #Right paddle
   
    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
   
    # collide off of right gutter
    if ball_pos[0] >= WIDTH - PAD_WIDTH:
        # hitting paddle 2 (right paddle)
        if ball_pos[1] >= paddle2_pos[1] and ball_pos[1] <= (paddle2_pos[1] + PAD_HEIGHT):
            ball_vel[0] = - ball_vel[0] - 1
        else:
            ball_vel = [0, 0]
            ball_pos = [WIDTH / 2, HEIGHT / 2]
            player_left_score = player_left_score + 1
            print 'player_left_score: ', player_left_score
            helper()
       
    # collide off of left gutter
   
    if ball_pos[0] <= PAD_WIDTH:
        # hitting paddle 1 (left paddle)
        if ball_pos[1] >= paddle1_pos[1] and ball_pos[1] <= (paddle1_pos[1] + PAD_HEIGHT):
            ball_vel[0] = - ball_vel[0]    + 1
           
        else:
            ball_vel = [0, 0]
            ball_pos = [WIDTH / 2, HEIGHT / 2]
            player_right_score = player_right_score + 1
           
            helper()
           
      
    # collide and reflect off of top of canvas
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
       
    # collide and reflect off of bottom of canvas
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    # update ball
           
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 2, 'black', 'black')
       
def keydown(key):
  
    global paddle1_vel, paddle2_vel
    current_key = chr(key)
   
    if key == simplegui.KEY_MAP['down']: # right paddle up
        paddle2_vel[1] = 0
        paddle2_vel[1] = paddle2_vel[1] + 3
    elif key == simplegui.KEY_MAP['up']: # right paddle down
        paddle2_vel[1] = 0
        paddle2_vel[1] = paddle2_vel[1] - 3
   
    elif key == simplegui.KEY_MAP['W']: #left paddle up
        paddle1_vel[1] = 0
        paddle1_vel[1] = paddle1_vel[1] - 3
    elif key == simplegui.KEY_MAP['S']: # left paddle down
        paddle1_vel[1] = 0
        paddle1_vel[1] = paddle1_vel[1] + 3

def keyup(key):
    global paddle1_vel, paddle2_vel
    current_key = chr(key)
    if key == simplegui.KEY_MAP['down']: # right paddle up
        paddle2_vel[1] = 0
    elif key == simplegui.KEY_MAP['up']: # right paddle down
        paddle2_vel[1] = 0
   
    elif key == simplegui.KEY_MAP['W']: #left paddle up
        paddle1_vel[1] = 0
    elif key == simplegui.KEY_MAP['S']: # left paddle down
        paddle1_vel[1] = 0



# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)
frame.add_button('start', helper, 100)
frame.set_canvas_background('silver')

# start frame


frame.start()
