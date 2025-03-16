
import rpi_gpio as GPIO
import time
import curses

#file that contains all the functions for the robot

# Define Motor Pins
LMF = 23    #Left Forward
LMB = 24    #Left Backward
RMF = 6     #Right Forward
RMB = 5     #Right Backward
# Define IR Sensor Pins
IR_L = 16   #Left
IR_C = 26   #Center
IR_R = 21   #Right
# Define GPIO pins for Ultrasonic
TRIG = 27   # Trigger pin
ECHO = 22   # Echo pin
# Define the servo control pins
servo_pin1 = 13     # First servo pin
servo_pin2 = 12     # Second servo pin



# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
# Set Motors as output
GPIO.setup(LMF, GPIO.OUT)
GPIO.setup(LMB, GPIO.OUT)
GPIO.setup(RMF, GPIO.OUT)
GPIO.setup(RMB, GPIO.OUT)
# Set IR sensors as input
GPIO.setup(IR_L, GPIO.IN)  
GPIO.setup(IR_C, GPIO.IN)
GPIO.setup(IR_R, GPIO.IN)
# GPIO setup for Ultrasonic
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


# Set up PWM on both Servo GPIO pins with a frequency of 50Hz
pwm1 = GPIO.PWM(servo_pin1, 50)  # 50Hz for first servo
pwm2 = GPIO.PWM(servo_pin2, 50)  # 50Hz for second servo

# Start PWM with a 0% duty cycle (stopped position) for Servo
pwm1.start(0)
pwm2.start(0)


curr_key = None


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

def spinLeft():
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(LMB, GPIO.HIGH)
    GPIO.output(RMF, GPIO.HIGH)
    GPIO.output(RMB, GPIO.LOW)
    
def right():
    GPIO.output(LMF, GPIO.HIGH)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMF, GPIO.LOW)
    GPIO.output(RMB, GPIO.LOW)

def spinRight():
    GPIO.output(LMF, GPIO.HIGH)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMF, GPIO.LOW)
    GPIO.output(RMB, GPIO.HIGH)
    
def stop():
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMF, GPIO.LOW)
    GPIO.output(RMB, GPIO.LOW)

def fullStop():
    GPIO.output(LMF, GPIO.HIGH)
    GPIO.output(LMB, GPIO.HIGH)
    GPIO.output(RMF, GPIO.HIGH)
    GPIO.output(RMB, GPIO.HIGH)


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
        


def read_infrared_data():
    
    # Function to read and print the state of each infrared sensor.
    
    # Read the value from each sensor
    irL_state = 1 if GPIO.input(IR_L) else 0
    irC_state = 1 if GPIO.input(IR_C) else 0
    irR_state = 1 if GPIO.input(IR_R) else 0

    # Print the state of each sensor
    print("IR01 State:", irL_state)
    print("IR02 State:", irC_state)
    print("IR03 State:", irR_state)

    return irL_state, irC_state, irR_state

def line_follow():

    irL_state, irC_state, irR_state = read_infrared_data()

    if irL_state == 0 and irC_state == 1 and irR_state == 0:
        # go forward
        front()

    elif irL_state == 1 and irR_state == 0:
        # Turn Left
        spinLeft()

    
    elif irR_state == 1 and irL_state == 0:
        # turn Right 
        spinRight()

    elif irL_state == 0 and irC_state == 0 and irR_state == 0:
        # Go Backwards
        back()
    
    elif irL_state == 1 and irC_state == 1 and irR_state == 1:
        # Full Stop
        fullStop()
        




def get_distance():
    """Measures distance using the HC-SR04 sensor and prints it."""
    
    # Ensure the trigger pin is LOW
    GPIO.output(TRIG, False)
    time.sleep(0.1)

    # Send a 10µs HIGH pulse to trigger measurement
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10µs pulse
    GPIO.output(TRIG, False)

    # Wait for the ECHO pin to go HIGH and record start time
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for the ECHO pin to go LOW and record end time
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate the pulse duration
    pulse_duration = pulse_end - pulse_start

    # Convert to distance (Speed of sound = 34300 cm/s, round-trip)
    distance = (pulse_duration * 34300) / 2

    # Print distance
    print(f"Distance: {round(distance, 2)} cm")

    return round(distance, 2)



def object_seeking():

    dist = get_distance()  # Call function to print distance

    if dist < 50 :

        fullStop()
    elif dist < 160 :

        #forward
        front()
    else :

        # spin
        spinLeft()
        time.sleep(0.25)
        object_seeking()


def object_avoidance():

    dist = get_distance()  # Call function to print distance

    if dist < 40 :

        fullStop()

        #spin left
        spinLeft()
        time.sleep(0.25)

        object_avoidance()

    else :

        # go forward
        front()




def autoGrab():

    dist = get_distance()

    if dist < 7.5:

        fullStop()
        
        time.sleep(0.2)

        arm_up()
        
        time.sleep(0.2)

        release()
        time.sleep(0.2)

        arm_down()
        time.sleep(0.2)

        grab()
        
        time.sleep(0.2)
        
        arm_up()

def manual():      
    if __name__ == "__main__":
        print("Starting Manual Control")
        print("'w': Forward")
        print("'a': Left")
        print("'s': Back")
        print("'d': Right")
        print("'u': Arm up")
        print("'j': Arm down")
        print("'o': Release")
        print("'l': Grab")
        curses.wrapper(key_listener)

        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
        
        pwm1.stop()
        pwm2.stop()
    
        GPIO.cleanup()

def line():

    print("Following Line")
    try:
        inc = 0
        while True:
            inc += 1
            print(f"Reading data for the {inc} time")
            line_follow() #controls line following
            # time.sleep(0.00001)
            time.sleep(0.01)
            stop()
            time.sleep(0.02)
        

    except KeyboardInterrupt:
        print("\nEnd of program")


    GPIO.cleanup()

def following():

    try:
        while True:
            object_seeking()
            time.sleep(0.25)  # wait 0.25s
            #stop()
            #time.sleep(0.1)  # wait 0.25s

    except KeyboardInterrupt:
        fullStop()
        print("\n Following stopped.")

    finally:
        GPIO.cleanup()  # Clean up GPIO

def avoiding():

    try:
        while True:
            object_avoidance()
            time.sleep(0.25)  # wait 0.5s
            stop()
            time.sleep(0.25)  # wait 0.5s


    except KeyboardInterrupt:
        print("\nMeasurement stopped.")

    finally:
        GPIO.cleanup()  # Clean up GPIO


def autonomous():

    try:
        inc = 0
        while True:
            inc += 1
            print(f"Reading data for the {inc} time")
            line_follow() #controls line following
            # time.sleep(0.00001)
            time.sleep(0.02)
            stop()
            time.sleep(0.000005)
            autoGrab()

        

    except KeyboardInterrupt:
        print("\nEnd of program")


    GPIO.cleanup()




def main():
    while True:
        # Prompt user for input
        print("\nSelect a function:")
        print("a. Manual Control")
        print("b. Line Following")
        print("c. Object Following")
        print("d. Object Avoidance")
        print("e. Autonomous Following + Grab")
        print("q. Quit")
        
        choice = input("Enter your choice: ").lower()  # Get input and convert to lowercase

        if choice == 'a':
            manual()
        elif choice == 'b':
            line()
        elif choice == 'c':
            following()
        elif choice == 'd':
            avoiding()
        elif choice == 'e':
            autonomous()
        elif choice == 'q':
            print("Exiting program.")
            break  # Exit the loop
        else:
            print("Invalid choice. Please try again.")

# Run the main function
main()
    

