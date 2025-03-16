import rpi_gpio as GPIO
import time

# Setting IR Sensor Pins
IR_L = 16
IR_C = 26
IR_R = 21

#Setting Motor Pins
LMF = 23
LMB = 24
RMF = 6
RMB = 5

# Set IR sensors as input
GPIO.setup(IR_L, GPIO.IN)  
GPIO.setup(IR_C, GPIO.IN)
GPIO.setup(IR_R, GPIO.IN)

# Set Motors out output
GPIO.setup(LMF, GPIO.OUT)
GPIO.setup(LMB, GPIO.OUT)
GPIO.setup(RMF, GPIO.OUT)
GPIO.setup(RMB, GPIO.OUT)

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
        GPIO.output(LMF, GPIO.HIGH)
        GPIO.output(LMB, GPIO.LOW)
        GPIO.output(RMF, GPIO.HIGH)
        GPIO.output(RMB, GPIO.LOW)

    elif irL_state == 1 and irR_state == 0:

        # Turn Left
        GPIO.output(LMF, GPIO.LOW)
        GPIO.output(LMB, GPIO.HIGH)
        GPIO.output(RMF, GPIO.HIGH)
        GPIO.output(RMB, GPIO.LOW)

    
    elif irR_state == 1 and irL_state == 0:
        # turn Right 
        GPIO.output(LMF, GPIO.HIGH)
        GPIO.output(LMB, GPIO.LOW)
        GPIO.output(RMF, GPIO.LOW)
        GPIO.output(RMB, GPIO.HIGH)

    elif irL_state == 0 and irC_state == 0 and irR_state == 0:
        # Go Backwards
        GPIO.output(LMF, GPIO.LOW)
        GPIO.output(LMB, GPIO.HIGH)
        GPIO.output(RMF, GPIO.LOW)
        GPIO.output(RMB, GPIO.HIGH)
    
    elif irL_state == 1 and irC_state == 1 and irR_state == 1:
        # Go Backwards
        GPIO.output(LMF, GPIO.HIGH)
        GPIO.output(LMB, GPIO.HIGH)
        GPIO.output(RMF, GPIO.HIGH)
        GPIO.output(RMB, GPIO.HIGH)

def stop():
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMF, GPIO.LOW)
    GPIO.output(RMB, GPIO.LOW)
    

# Main program
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
