# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility
import RPistepper as stp

M1_pins = [18, 17, 27, 22]
M1 = stp.Motor(M1_pins)
M2_pins = [5, 6, 26, 16]
M2 = stp.Motor(M2_pins)

def left():
    i = 0
    while i < 10:
        M1.move(1)
        i = i + 1

def right_reverse():
    i = 0
    while i < 20:
        M1.move(-1)
        i = i + 1

def right():
    i = 0
    while i < 10:
        M2.move(-1)
        i = i + 1

def left_reverse():
    i = 0
    while i < 20:
        M2.move(1)
        i = i + 1

def foward():
    i = 0
    while i < 25:
        M1.move(1)
        M2.move(-1)
        i = i + 1

def reverse():
    i = 0
    while i < 25:
        M1.move(-1)
        M2.move(1)
        i = i + 1

def follow_red(r,g,b):
    if r/(r + g + b) > 0.6 and r/(r + g + b) < 0.62:
        print("let's go")
        foward()
    elif r/(r + g + b) > 0.62:
        print("we got this")
        right()
    elif r/(r + g + b) < 0.6:
        print("let's go!")
        left()


i = 0
steps = 200

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
apds = APDS9960(i2c)
apds.enable_color = True

# following red path Nolop
# upper = 0.62
# lower = 0.6

# following purple path Blake (attempted)
# upper = 0.50
# lower = 0.45

# following blue path Blake
#upper = 0.49
#lower = 0.45

# following green path Blake
upper = 0.33
lower = 0.36


while True:
    # wait for color data to be ready
    while not apds.color_data_ready:
        time.sleep(0.005)

    # get the data and print the different channels
    r, g, b, c = apds.color_data
    print("red: ", r)
    print("green: ", g)
    print("blue: ", b)
    print("clear: ", c)

    print("color temp {}".format(colorutility.calculate_color_temperature(r, g, b)))
    print("light lux {}".format(colorutility.calculate_lux(r, g, b)))
    
    if b/(r + g + b) > 0.3:
        print("we are at an intersection!")
        
        lower = 0.33
        upper = 0.35
        i = 0
        while i < 45:
            left()
            i = i + 1

    elif g/(r + g + b) > lower and g/(r + g + b) < upper:
        foward()
    elif g/(r + g + b) > upper:
        left()
    elif g/(r + g + b) < lower:
        right()
    
        
    time.sleep(0.5)

M1.release()
M1.cleanup
M2.release()
M2.cleanup
