# Core opencv code provided by Einsteinium Studios
# Revisions to work with Pi Camera v3 by Briana Bouchard

import numpy as np
import cv2
from picamera2 import Picamera2
from libcamera import controls
import time
import board
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility
import RPistepper as stp

M1_pins = [18, 17, 27, 22]
M1 = stp.Motor(M1_pins)
M2_pins = [5, 6, 26, 16]
M2 = stp.Motor(M2_pins)

picam2 = Picamera2() # assigns camera variable

capture_config = picam2.create_still_configuration() #automatically 4608x2592 width by height (columns by rows) pixels
picam2.configure(capture_config)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) #sets auto focus mode

picam2.start() # activates camera

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

time.sleep(1) # wait to give camera time to start up

x = 0
y = 0
 
while(True):
    
    # Display camera input
    image = picam2.capture_array("main")
    cv2.imshow('img',image)

    #create boundary for red values as two arrays
    lower = np.array([0,30,0]) #lower range of bgr values for red
    upper = np.array([60,255,60]) #upper range of bgr values for red

    #determine if the pixel in the image has bgr values within the range & putting the image in grayscale
    image_mask = cv2.inRange(image,lower,upper) #returns array of 0s & 255s, 255=white=within range, 0=black=not in range
    image_mask = ~image_mask # inverting the photo such that tape line is black; everything else is white.
 
    # Gaussian blur
    blur = cv2.GaussianBlur(image_mask,(5,5),0)
 
    # Color thresholding
    input_threshold,comp_threshold = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV)
 
    # Find the contours of the frame
    contours,hierarchy = cv2.findContours(comp_threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
 
    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c) # determine moment - weighted average of intensities
 
        cx = int(M['m10']/M['m00']) # find x component of centroid location
        cy = int(M['m01']/M['m00']) # find y component of centroid location
 
        cv2.line(image,(cx,0),(cx,720),(255,0,0),1) # display vertical line at x value of centroid
        cv2.line(image,(0,cy),(1280,cy),(255,0,0),1) # display horizontal line at y value of centroid
 
        cv2.drawContours(image, contours, -1, (0,255,0), 2) # display green lines for all contours
         
        # determine location of centroid in x direction and adjust steering recommendation
        print(cx)
        if cx >=2377:
            print("Turn Left!")
            right()
            x = 1
 
        if cx < 2377 and cx > 570:
            print("On Track!")
            foward()
            y = 1
 
        if cx <= 570:
            print("Turn Right")
            left()
            x = 3
 
    else:
        print("I don't see the line")

        # Remembering the last direction so that the robot can backtrack if line is lost
        if x == 1:
            left()
        elif x == 3:
            right()
        elif y == 1:
            y = 0
            if x == 1:
                left()
            elif x == 3:
                right()
 
    # Display the resulting frame
    cv2.imshow('frame',image)
    
    # Check for "q" key press to end program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break