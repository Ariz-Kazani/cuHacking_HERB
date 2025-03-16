import rpi_gpio as GPIO
import time

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

try:
    for i in range(2):
        # Move first servo to one position
        pwm1.ChangeDutyCycle(11)  # Adjust duty cycle for position
        time.sleep(1)  # Wait for 1 second

        # Move second servo to another position
        pwm2.ChangeDutyCycle(7)  # Adjust duty cycle for position
        time.sleep(1)  # Wait for 1 second

    # Stop both PWM signals
    
    
    
    

except KeyboardInterrupt:
    pass

# Stop PWM and clean up GPIO settings
print("Cleaning up")
GPIO.cleanup()
