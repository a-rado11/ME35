# This python script runs a bipolar stepper motor in a full-step sequence for a set number of steps at a specific speed in revolutions per minute.
# Written by Briana Bouchard 

import RPi.GPIO as GPIO
import time
import board
import digitalio


# Initialize pins using BCM mode (GPIO pin numbers not board numbers)
yellow = digitalio.DigitalInOut(board.D18)
yellow.direction = digitalio.Direction.OUTPUT
red = digitalio.DigitalInOut(board.D17)
red.direction = digitalio.Direction.OUTPUT
gray = digitalio.DigitalInOut(board.D27)
gray.direction = digitalio.Direction.OUTPUT
green = digitalio.DigitalInOut(board.D22)
green.direction = digitalio.Direction.OUTPUT

# Define direction values
cw = 1
ccw = 0

# Define the steps per revolution for the motor 
steps_rev = 200

def setMotor(current_step, delay):
# This function provides the step sequence

    if current_step == 0:
        yellow.value = True
        red.value = False
        gray.value = True
        green.value = False
        time.sleep(delay)

    elif current_step == 1:
        yellow.value = False
        red.value = True
        gray.value = True
        green.value = False
        time.sleep(delay)

    elif current_step == 2:
        yellow.value = False
        red.value = True
        gray.value = False
        green.value = True
        time.sleep(delay)
        
    elif current_step == 3:
        yellow.value = True
        red.value = False
        gray.value = False
        green.value = True
        time.sleep(delay)


def moveSteps(input_steps, speed):    
# This function tracks the number of steps remaining based on the step input and the loop cycles

    current_step = 0
    delay = 60/(steps_rev*speed)
    
    # Determines the direction based on sign of input_steps 
    if input_steps > 0:
        direction = ccw
    if input_steps < 0:
        direction = cw
    
    for steps_remaining in range(abs(input_steps), 0, -1):
        if direction == cw: 
            if current_step >= 0 and current_step < 3:
                current_step = current_step + 1
            elif current_step == 3:
                current_step = 0
        if direction == ccw: 
            if current_step <= 3 and current_step > 0:
                current_step = current_step - 1
            elif current_step == 0:
                current_step = 3
                
        setMotor(current_step, delay)
        
    print("Stepping complete! Your motor completed " + str(abs(input_steps)) + " steps at " + str(speed)+ " revolutions per minute")
    

while True:
    # Define the steps per revolution for the motor 
    steps_rev = 200
    
    # Set the number of steps to move and the speed in revolutions per minute
    moveSteps(-200, 20)
    
    break