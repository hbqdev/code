# template for "Stopwatch: The Game"
import simpleguitk as simplegui
# define global variables
timer=None
time=0
message="0:00.0"
attempts=0
success=0
started=False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global message, D, b, A, BC
    D=t%10
    b=t/10
    A=int(b/60)
    BC=int(b%60)    
    message =str(A)+":"+('%02d' % BC)+"."+str(D)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    global started
    started=True

def stop():
    timer.stop()
    global attempts
    global success
    global label
    global started
    if started:
        if time%10==0:
            success=success+1
        started=False
        attempts=attempts+1
        
def reset():
    global time
    global started
    global attempts
    global success
    #started=0
    attempts=0
    success=0
    timer.stop()
    time=0
    format(time)

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time=time+1
    format(time)

# define draw handler
def draw(canvas):
    canvas.draw_text(message, [60,90], 30, "Black")
    canvas.draw_text(str(success)+"/"+str(attempts), [150,30], 20, "Blue")
    
# create frame
frame = simplegui.create_frame("Home", 200, 150)
frame.set_canvas_background("White")

# register event handlers
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, timer_handler)
# start frame
frame.start()
#timer.start()
# Please remember to review the grading rubric


