# This python script runs a bipolar stepper motor in a full-step sequence for a set number of steps at a specific speed in revolutions per minute.
# Written by Briana Bouchard 

import RPi.GPIO as GPIO
import time
import board
import digitalio
from digitalio import DigitalInOut, Direction, Pull
from time import sleep
import sys

switch = DigitalInOut(board.D14)
switch.direction = Direction.INPUT
switch.pull = Pull.DOWN

# Initialize pins using BCM mode (GPIO pin numbers not board numbers)
yellow1 = digitalio.DigitalInOut(board.D18)
yellow1.direction = digitalio.Direction.OUTPUT
red1 = digitalio.DigitalInOut(board.D17)
red1.direction = digitalio.Direction.OUTPUT
gray1 = digitalio.DigitalInOut(board.D27)
gray1.direction = digitalio.Direction.OUTPUT
green1 = digitalio.DigitalInOut(board.D22)
green1.direction = digitalio.Direction.OUTPUT

yellow2 = digitalio.DigitalInOut(board.D5)
yellow2.direction = digitalio.Direction.OUTPUT
red2 = digitalio.DigitalInOut(board.D6)
red2.direction = digitalio.Direction.OUTPUT
gray2 = digitalio.DigitalInOut(board.D26)
gray2.direction = digitalio.Direction.OUTPUT
green2 = digitalio.DigitalInOut(board.D16)
green2.direction = digitalio.Direction.OUTPUT

# Define direction values
cw = 1
ccw = 0

# Define the steps per revolution for the motor 
steps_rev = 200

def setMotor(current_step1, current_step2, delay):
    # check kill switch!
    if(switch.value):
        print("Kill switch was hit!")
        exit()
# This function provides the step sequence

    if current_step1 == 0:
        yellow1.value = True
        red1.value = False
        gray1.value = True
        green1.value = False

    elif current_step1 == 1:
        yellow1.value = False
        red1.value = True
        gray1.value = True
        green1.value = False

    elif current_step1 == 2:
        yellow1.value = False
        red1.value = True
        gray1.value = False
        green1.value = True

        
    elif current_step1 == 3:
        yellow1.value = True
        red1.value = False
        gray1.value = False
        green1.value = True


    if current_step2 == 0:

        yellow2.value = True
        red2.value = False
        gray2.value = True
        green2.value = False

    elif current_step2 == 1:

        yellow2.value = False
        red2.value = True
        gray2.value = True
        green2.value = False

    elif current_step2 == 2:

        yellow2.value = False
        red2.value = True
        gray2.value = False
        green2.value = True
        
    elif current_step2 == 3:

        yellow2.value = True
        red2.value = False
        gray2.value = False
        green2.value = True
    
    time.sleep(delay)

def moveSteps(input_steps1, input_steps2, speed):    

# This function tracks the number of steps remaining based on the step input and the loop cycles

    current_step1 = 0
    current_step2 = 0
    delay = 60/(steps_rev*speed)
    
    # Determines the direction based on sign of input_steps 
    if input_steps1 > 0:
        direction1 = ccw
    if input_steps1 < 0:
        direction1 = cw

    if input_steps2 > 0:
        direction2 = ccw
    if input_steps2 < 0:
        direction2 = cw
    

    for steps_remaining1 in range (abs(input_steps1), 0, -1):
        if direction1 == cw: 
            if current_step1 >= 0 and current_step1 < 3:
                current_step1 = current_step1 + 1
            elif current_step1 == 3:
                current_step1 = 0
        if direction1 == ccw: 
            if current_step1 <= 3 and current_step1 > 0:
                current_step1 = current_step1 - 1
            elif current_step1 == 0:
                current_step1 = 3
        if direction2 == cw: 
            if current_step2 >= 0 and current_step2 < 3:
                current_step2 = current_step2 + 1
            elif current_step2 == 3:
                current_step2 = 0
        if direction2 == ccw: 
            if current_step2 <= 3 and current_step2 > 0:
                current_step2 = current_step2 - 1
            elif current_step2 == 0:
                current_step2 = 3
                
        setMotor(current_step1, current_step2, delay)
        
    print("Stepping complete! Your motor completed " + str(abs(input_steps1)) + " steps at " + str(speed)+ " revolutions per minute")
    


while True:
    if(switch.value):
        time.sleep(1)
        # Define the steps per revolution for the motor 
        steps_rev = 200
        while True:
            # Set the number of steps to move and the speed in revolutions per minute
            moveSteps(-1000, 1000, 40)
    
        break
