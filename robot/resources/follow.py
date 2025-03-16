

import rpi_gpio as GPIO
import time

# Define GPIO pins for Ultrasonic
TRIG = 27  # Trigger pin
ECHO = 22  # Echo pin

#Setting Motor Pins
LMF = 23
LMB = 24
RMF = 6
RMB = 5


# GPIO setup for Ultrasonic
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Set Motors as output
GPIO.setup(LMF, GPIO.OUT)
GPIO.setup(LMB, GPIO.OUT)
GPIO.setup(RMF, GPIO.OUT)
GPIO.setup(RMB, GPIO.OUT)

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

    if dist < 60 :

        fullStop()

        
    elif dist < 300 :

        #forward
        GPIO.output(LMF, GPIO.HIGH)
        GPIO.output(LMB, GPIO.LOW)
        GPIO.output(RMF, GPIO.HIGH)
        GPIO.output(RMB, GPIO.LOW)
        

    else :

        # spin
        GPIO.output(LMF, GPIO.HIGH)
        GPIO.output(LMB, GPIO.LOW)
        GPIO.output(RMF, GPIO.LOW)
        GPIO.output(RMB, GPIO.HIGH)
        time.sleep(0.1)
        object_seeking()

        

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



    
try:
    while True:
        object_seeking()
        time.sleep(0.25)  # wait 0.25s
        stop()
        time.sleep(0.1)  # wait 0.25s


except KeyboardInterrupt:
    fullStop()
    print("\nMeasurement stopped.")

finally:
    GPIO.cleanup()  # Clean up GPIO