# Code to spin DC motor in two directions

import RPi.GPIO as GPIO
from time import sleep
import sys

#assign GPIO pins for motor
motor_channel = (18,17)  
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#for defining more than 1 GPIO channel as input/output use
GPIO.setup(motor_channel, GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)

motor_direction = input('select motor direction u=up, d=down: ')
while True:
    try:
        if(motor_direction == 'u'): #up
            print('motor running clockwise\n')
            GPIO.output(motor_channel, (GPIO.HIGH,GPIO.LOW))
            sleep(0.02)

        elif(motor_direction == 'd'): #down
            print('motor running anti-clockwise\n')
            GPIO.output(motor_channel, (GPIO.LOW,GPIO.HIGH))
            sleep(0.02)

           
    #press ctrl+c for keyboard interrupt
    except KeyboardInterrupt:
        #query for setting motor direction or exit
        GPIO.output(motor_channel, (GPIO.LOW,GPIO.LOW))
        motor_direction = input('select motor direction u=up, d=down: ')
        #check for exit
        if(motor_direction == 'q'):
            GPIO.cleanup()
            print('motor stopped')
            sys.exit(0)
