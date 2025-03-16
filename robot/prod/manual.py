import time
import rpi_gpio as GPIO
import curses

# This file is used for manual control of the robot using the keyboard
# The robot is connected to via ssh

LMF = 23
LMB = 24
RMF = 6
RMB = 5

curr_key = None

GPIO.setmode(GPIO.BCM)

# Define the servo control pins
servo_pin1 = 13  # First servo pin
servo_pin2 = 12  # Second servo pin

# Set both GPIO pins as output
GPIO.setup(servo_pin1, GPIO.OUT)
GPIO.setup(servo_pin2, GPIO.OUT)

# Set up PWM on both GPIO pins with a frequency of 50Hz
pwm1 = GPIO.PWM(servo_pin1, 50)  # 50Hz for first servo
pwm2 = GPIO.PWM(servo_pin2, 50)  # 50Hz for second servo

# Start PWM with a 0% duty cycle (stopped position)
pwm1.start(0)
pwm2.start(0)


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
    
def arm_up():
    pwm1.ChangeDutyCycle(11)
    
def arm_down():
    pwm1.ChangeDutyCycle(7)
    
    
def grab():
    pwm2.ChangeDutyCycle(11.5)
    
    
def release():
    pwm2.ChangeDutyCycle(7)

key_actions = {
    ord('w'): front,
    ord('a'): left,
    ord('s'): back,
    ord('d'): right,
}

arm_actions = {
    ord('u'): arm_up,
    ord('j'): arm_down,
    ord('o'): release,
    ord('l'): grab,
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
            
        elif key in arm_actions:
            arm_actions[key]()
        
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
    
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
    
    pwm1.stop()
    pwm2.stop()
    
    GPIO.cleanup()
