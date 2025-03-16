import time
import rpi_gpio as GPIO

import curses


# Set up GPIO mode
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

def arm_up():
    pwm1.ChangeDutyCycle(11)
    
def arm_down():
    pwm1.ChangeDutyCycle(7)
    
    
def grab():
    pwm2.ChangeDutyCycle(11.5)
    
    
def release():
    pwm2.ChangeDutyCycle(7)

key_actions = {
    ord('u'): arm_up,
    ord('j'): arm_down,
    ord('o'): release,
    ord('l'): grab,
}

def perform_action(key):
    key_actions[key]()
        
    
def key_listener(stdscr):
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.keypad(True)   # Enables special keys

    while True:
        # Get the currently pressed key
        key = stdscr.getch()

        if key in key_actions:
            perform_action(key)
        
        elif key == ord('x'):
            pwm1.stop()
            pwm2.stop()
        elif key == -1:
            pass
        else:
            print("Unknown key:", key)
            
            
if __name__ == "__main__":
    print("start")
    curses.wrapper(key_listener)
    
    GPIO.cleanup()