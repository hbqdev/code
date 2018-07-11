# Implementation of classic arcade game Pong

import simplegui
import random
import math

#########################
# globals
#########################

WIDTH = 600
HEIGHT = 480       
BALL_RADIUS = 20
PAD_WIDTH = 20
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
PAD_SPEED = 4
MAX_BALL_SPEED = 600
SPEED_INCREASE = 0.1
MAX_PARTICLES = 10
LOADING_TEXT = "loading images..."
BALL_EFFECT1_WIDTH = 1
BALL_EFFECT1_HEIGHT = 1
BALL_EFFECT2_WIDTH = 1
BALL_EFFECT2_HEIGHT = 1

computer_AI = False
gutter_count = 0


trail = []

#########################
# load images
#########################

background_img = simplegui.load_image("https://dl.dropboxusercontent.com/u/8367729/codeskulptor/pong/background.png")
paddle_img = simplegui.load_image("https://dl.dropboxusercontent.com/u/8367729/codeskulptor/pong/paddle.png")
ball_img = simplegui.load_image("https://dl.dropboxusercontent.com/u/8367729/codeskulptor/pong/ball.png")
ball_effect1_img = simplegui.load_image("https://dl.dropboxusercontent.com/u/8367729/codeskulptor/pong/ball_effect1.png")
ball_effect2_img = simplegui.load_image("https://dl.dropboxusercontent.com/u/8367729/codeskulptor/pong/ball_effect2.png")

images = [background_img, paddle_img, ball_img, ball_effect1_img, ball_effect2_img]
images_loaded = False


#########################
# sounds
#########################

electric_snd = simplegui.load_sound("https://dl.dropboxusercontent.com/u/8367729/codeskulptor/pong/zap.ogg")
beep_snd = simplegui.load_sound("https://dl.dropboxusercontent.com/u/8367729/codeskulptor/pong/beep.ogg")
beep_snd.set_volume(0.5)

#########################
# helper functions
#########################

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
# also resets the paddle positions
def ball_init(right):
    global ball_pos, ball_vel, paddle1_pos, paddle2_pos # these are vectors stored as lists
    global trail
    trail = []
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.randrange(120, 240) / 60.0, -random.randrange(60, 180) / 60.0]
    if not right:
        ball_vel[0] = -ball_vel[0]

    paddle1_pos = HEIGHT / 2.0
    paddle2_pos = HEIGHT / 2.0
    
    beep_snd.play()

# start a new game resetting the paddle speeds and scores
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    
    score1 = 0
    score2 = 0
    
    ball_init(random.choice([True, False]))
    trail_timer.start()
    
    
# start the electric collision effect
def start_electric_effect():
    collision_effect_timer.start()
    electric_snd.rewind()
    electric_snd.play()

# clamp a value between a minimum and maximum
def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

# return the magnitude of a vector
def magnitude(vel):
    return math.sqrt(vel[0] ** 2 + vel[1] ** 2)

# return the angle between two points
def angle(x1, y1, x2, y2):
    return math.atan2(y2-y1, x2-x1)

# set the ball's angle    
def set_ball_angle(angle):
    global ball_vel
    speed = magnitude(ball_vel)
    ball_vel[0] = speed * math.cos(angle)
    ball_vel[1] = speed * math.sin(angle)

# speed up ball
def speed_up_ball():
    ball_vel[0] = clamp(ball_vel[0] + ball_vel[0] * SPEED_INCREASE, 
                        -MAX_BALL_SPEED, MAX_BALL_SPEED)
    ball_vel[1] = clamp(ball_vel[1] + ball_vel[1] * SPEED_INCREASE, 
                        -MAX_BALL_SPEED, MAX_BALL_SPEED)
            
# move the ball and check for collisions
def update_ball():
    global ball_pos, ball_vel, score1, score2, has_collision_effect
    
    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # check for top or bottom collision
    if ball_pos[1] < BALL_RADIUS:
        ball_pos[1] = BALL_RADIUS 
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] > HEIGHT - BALL_RADIUS:
        ball_pos[1] = HEIGHT - BALL_RADIUS 
        ball_vel[1] = -ball_vel[1]
        
    # check left gutter
    if ball_pos[0] < PAD_WIDTH + BALL_RADIUS:
        # check for paddle
        if paddle1_pos - HALF_PAD_HEIGHT - BALL_RADIUS <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT + BALL_RADIUS:
            # bounce
            ball_pos[0] = PAD_WIDTH + BALL_RADIUS 
            speed_up_ball()
            # set ball angle equal to the angle from the paddle to the ball
            # if the ball is nearer the edge of the paddle it gets deflected at a greater angle
            set_ball_angle(angle(HALF_PAD_WIDTH, paddle1_pos, ball_pos[0], ball_pos[1]))
            start_electric_effect()
        else:
            # p2 score
            score2 += 1
            ball_init(ball_pos[0] < WIDTH / 2)
            
    # check right gutter  
    elif ball_pos[0] > WIDTH - PAD_WIDTH - BALL_RADIUS:
        # check for paddle
        if paddle2_pos - HALF_PAD_HEIGHT - BALL_RADIUS <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT + BALL_RADIUS:
            # bounce
            ball_pos[0] = WIDTH - PAD_WIDTH - BALL_RADIUS
            speed_up_ball()
            set_ball_angle(angle(WIDTH - HALF_PAD_WIDTH, paddle2_pos, ball_pos[0], ball_pos[1]))
            start_electric_effect()
        else:
            # p1 score
            score1 += 1
            ball_init(ball_pos[0] < WIDTH / 2)

# update paddle positions and keep them on-screen
def update_paddles():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    
    # computer AI
    # only moves when ball on his side
    if computer_AI:# and ball_pos[0] < WIDTH / 2:
        if paddle1_pos + HALF_PAD_HEIGHT < ball_pos[1]:
            paddle1_vel = PAD_SPEED
        elif paddle1_pos - HALF_PAD_HEIGHT > ball_pos[1]:
            paddle1_vel = -PAD_SPEED
        else:
            paddle1_vel = 0
                
    # paddle 1
    paddle1_pos += paddle1_vel
    if paddle1_pos < HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    
    # paddle 2
    paddle2_pos += paddle2_vel
    if paddle2_pos < HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
   
#########################
# drawing
#########################

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, gutter_count
    if images_loaded:
        # draw background
        c.draw_image(background_img, 
                     (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT), 
                     (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT))
        
        # update paddle's vertical position, keep paddle on the screen
        update_paddles()
        
        # draw mid line and gutters
        # mid line
        c.draw_line([WIDTH / 2, gutter_count],[WIDTH / 2, gutter_count+10], 1, "Red")
        c.draw_line([WIDTH / 2, HEIGHT - gutter_count],[WIDTH / 2, HEIGHT - gutter_count-10], 1, "Red")
        # gutter left
        c.draw_line([PAD_WIDTH, gutter_count],[PAD_WIDTH, gutter_count+10], 1, "Red")
        c.draw_line([WIDTH - PAD_WIDTH, gutter_count],[WIDTH - PAD_WIDTH, gutter_count+10], 1, "Red")
        # gutter right
        c.draw_line([PAD_WIDTH, HEIGHT - gutter_count],[PAD_WIDTH, HEIGHT - gutter_count-10], 1, "Red")
        c.draw_line([WIDTH - PAD_WIDTH, HEIGHT - gutter_count],[WIDTH - PAD_WIDTH, HEIGHT - gutter_count-10], 1, "Red")
        gutter_count = (gutter_count + 10) % HEIGHT
        
        # draw paddles
        """
        c.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], 
                    [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], 
                    PAD_WIDTH, "Red")
        c.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], 
                    [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], 
                    PAD_WIDTH, "Green")
        """
        c.draw_image(paddle_img, 
                     (HALF_PAD_WIDTH, HALF_PAD_HEIGHT), (PAD_WIDTH, PAD_HEIGHT), 
                     (HALF_PAD_WIDTH, paddle1_pos), (PAD_WIDTH, PAD_HEIGHT))
        c.draw_image(paddle_img, 
                     (HALF_PAD_WIDTH, HALF_PAD_HEIGHT), (PAD_WIDTH, PAD_HEIGHT), 
                     (WIDTH - HALF_PAD_WIDTH, paddle2_pos), (PAD_WIDTH, PAD_HEIGHT), math.pi)
        
        
        # update ball
        update_ball()
        
        # draw trail
        for item in trail:
            c.draw_image(ball_effect1_img, 
                     (BALL_EFFECT1_WIDTH/2, BALL_EFFECT1_HEIGHT/2), (BALL_EFFECT1_WIDTH, BALL_EFFECT1_HEIGHT), 
                     item, (BALL_EFFECT1_WIDTH/2, BALL_EFFECT1_HEIGHT/2))
            c.draw_image(ball_img, 
                     (BALL_RADIUS, BALL_RADIUS), (BALL_RADIUS*2, BALL_RADIUS*2), 
                     item, (BALL_RADIUS, BALL_RADIUS), math.radians(random.randrange(360)))
                   
        # draw ball
        #c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
        if collision_effect_timer.is_running():
            c.draw_image(ball_effect2_img, 
                        (BALL_EFFECT2_WIDTH/2, BALL_EFFECT2_HEIGHT/2), (BALL_EFFECT2_WIDTH, BALL_EFFECT2_HEIGHT), 
                        ball_pos, (BALL_EFFECT2_WIDTH, BALL_EFFECT2_HEIGHT), 
                        math.radians(random.randrange(360)))
        c.draw_image(ball_effect1_img, 
                     (BALL_EFFECT1_WIDTH/2, BALL_EFFECT1_HEIGHT/2), (BALL_EFFECT1_WIDTH, BALL_EFFECT1_HEIGHT), 
                     ball_pos, (BALL_EFFECT1_WIDTH, BALL_EFFECT1_HEIGHT))
        c.draw_image(ball_img, 
                     (BALL_RADIUS, BALL_RADIUS), (BALL_RADIUS*2, BALL_RADIUS*2), 
                     ball_pos, (BALL_RADIUS*2, BALL_RADIUS*2), math.radians(random.randrange(360)))
        
        
        # draw scores
        c.draw_text(str(score1), (WIDTH / 4, 50), 48, "#CCCCCC", "monospace")
        c.draw_text(str(score2), ((WIDTH / 4) * 3, 50), 48, "#CCCCCC", "monospace")
    
    else:
        c.draw_text(LOADING_TEXT, 
                    (WIDTH/2 - frame.get_canvas_textwidth(LOADING_TEXT, 48, "monospace")/2, HEIGHT/2), 
                    48, "#CCCCCC", "monospace") 

#########################
# key handlers
#########################

# handle key presses
def keydown(key):
    global paddle1_vel, paddle2_vel
    # paddle 1
    if not computer_AI:
        if key == simplegui.KEY_MAP["w"]:
            paddle1_vel = -PAD_SPEED
        elif key == simplegui.KEY_MAP["s"]:
            paddle1_vel = PAD_SPEED
    # paddle 2
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PAD_SPEED
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PAD_SPEED
        
# handle key releases   
def keyup(key):
    global paddle1_vel, paddle2_vel
    # paddle 1
    if not computer_AI:
        if key == simplegui.KEY_MAP["w"]:
            paddle1_vel = 0
        elif key == simplegui.KEY_MAP["s"]:
            paddle1_vel = 0
    # paddle 2
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

#########################
# buttons
#########################

# restart button handler
def restart():
    new_game()

# toggle computer AI and restart game
def toggle_ai():
    global computer_AI, ai_label
    computer_AI = not computer_AI
    if computer_AI:
        ai_label.set_text("Computer AI: ON")
    else:
        ai_label.set_text("Computer AI: OFF")
    new_game()
    
#########################
# timers
#########################

# end the collision effect
def collision_effect_tick():
    collision_effect_timer.stop()

# create random trail of particles
def trail_timer_tick():
    random_value = random.randrange(5)
    if random_value < 3:
        if len(trail) < MAX_PARTICLES:
            trail.append(list(ball_pos))
    elif len(trail) > 0:
            trail.pop(random.randrange(len(trail)))

# check if the images have loaded
def check_images_loaded():
    global images_loaded
    global BALL_EFFECT1_WIDTH, BALL_EFFECT1_HEIGHT, BALL_EFFECT2_WIDTH, BALL_EFFECT2_HEIGHT,\
            BALL_RADIUS, PAD_WIDTH, PAD_HEIGHT, HALF_PAD_WIDTH, HALF_PAD_HEIGHT
    
    for image in images:
        if image.get_width() == 0:
            return
    
    BALL_RADIUS = ball_img.get_width() / 2
    PAD_WIDTH = paddle_img.get_width()
    PAD_HEIGHT = paddle_img.get_height()
    HALF_PAD_WIDTH = PAD_WIDTH / 2
    HALF_PAD_HEIGHT = PAD_HEIGHT / 2
    BALL_EFFECT1_WIDTH = ball_effect1_img.get_width()
    BALL_EFFECT1_HEIGHT = ball_effect1_img.get_height()
    BALL_EFFECT2_WIDTH = ball_effect2_img.get_width()
    BALL_EFFECT2_HEIGHT = ball_effect2_img.get_height()
    
    images_loaded = True
    image_load_timer.stop()
    
    
#########################
# create frame
#########################
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT, 150)
frame.set_canvas_background("Black")
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart, 150)
frame.add_label("")
ai_label = frame.add_label("Computer AI: OFF")
frame.add_button("Toggle AI", toggle_ai, 150)

collision_effect_timer = simplegui.create_timer(200, collision_effect_tick)
trail_timer = simplegui.create_timer(500, trail_timer_tick)
image_load_timer = simplegui.create_timer(100, check_images_loaded)

# start a new game
image_load_timer.start()
new_game()

# start frame
frame.start()

