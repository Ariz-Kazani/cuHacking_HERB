import time
import rpi_gpio as GPIO

import curses

LMF = 23
LMB = 24
RMF = 6
RMB = 5

curr_key = None

def set_pins():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LMF, GPIO.OUT)
    GPIO.setup(LMB, GPIO.OUT)
    GPIO.setup(RMF, GPIO.OUT)
    GPIO.setup(RMB, GPIO.OUT)

set_pins()

def front():
    GPIO.output(LMF, GPIO.HIGH)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMF, GPIO.HIGH)
    GPIO.output(RMB, GPIO.LOW)
    
def back():
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(LMB, GPIO.HIGH)
    GPIO.output(RMF, GPIO.LOW)
    GPIO.output(RMB, GPIO.HIGH)
    
    
def left():
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMF, GPIO.HIGH)
    GPIO.output(RMB, GPIO.LOW)
    
def right():
    GPIO.output(LMF, GPIO.HIGH)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMF, GPIO.LOW)
    GPIO.output(RMB, GPIO.LOW)
    
def stop():
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMF, GPIO.LOW)
    GPIO.output(RMB, GPIO.LOW)

key_actions = {
    ord('w'): front,
    ord('a'): left,
    ord('s'): back,
    ord('d'): right,
}

def perform_action(key):
    global curr_key 
    
    if key == curr_key:
        key_actions[key]()
    else:
        stop()
        curr_key = key
        
    
def key_listener(stdscr):
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.keypad(True)   # Enables special keys

    stop()  # Ensure motors are stopped initially

    while True:
        # Get the currently pressed key
        key = stdscr.getch()

        if key in key_actions:
            perform_action(key)
        
        elif key == ord('x'):
            break
            stop()
        elif key == -1:
            pass
        else:
            print("Unknown key:", key)
            stop()
        
        
        
        

         
    
if __name__ == "__main__":
    print("start")
    curses.wrapper(key_listener)
    
    GPIO.cleanup()
    
    
    
    

