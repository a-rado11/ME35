# Kelly Macdonald, Anthony Radovanovich
# Import libraries
import RPi.GPIO as GPIO
import time
from time import sleep
import sys

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(32,GPIO.OUT)
servo1 = GPIO.PWM(32,50) # Note 11 is pin, 50 = 50Hz pulse

#assign GPIO pins for motor
motor_channel = (11,12)  
GPIO.setwarnings(False)
#for defining more than 1 GPIO channel as input/output use
GPIO.setup(motor_channel, GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)


#start PWM running, but with value of 0 (pulse off)
servo1.start(0)
print ("Waiting for 2 seconds")
time.sleep(2)

#turn back to 0 degrees
print ("Turning out")
servo1.ChangeDutyCycle(12)
time.sleep(0.5)
servo1.ChangeDutyCycle(0)

print("Going up")
for i in range(400):
    GPIO.output(motor_channel, (GPIO.LOW,GPIO.HIGH))
    sleep(0.02)
GPIO.output(motor_channel, (GPIO.LOW,GPIO.LOW))


#Clean things up at the end
servo1.stop()
GPIO.cleanup()
print ("Servo STPO")
