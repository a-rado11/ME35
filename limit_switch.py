# import RPi.GPIO as GPIO
# from time import sleep
# import sys

# GPIO.setmode(GPIO.BOARD)

# GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# #GPIO.output(29,GPIO.HIGH)

# def callback():
#         print("Hello World!")


# while True:

#     if(GPIO.input(40) == 1):
#         callback()
#     else:
#         print("boo")


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

def callback():
        print("Hello World!")
        pass

while True:
    if(switch.value):
        callback()
    else:
        print("boo")