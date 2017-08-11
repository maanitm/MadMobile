import const
import pygame
import time
import RPi.GPIO as GPIO
from RPIO import PWM
import math

servo = PWM.Servo()

servo.set_servo(const.leftMotorFrontPin, 1500)
servo.set_servo(const.leftMotorBackPin, 1500)
servo.set_servo(const.rightMotorFrontPin, 1500)
servo.set_servo(const.rightMotorBackPin, 1500)
# WARNING: Right side inverted!

drive = 0

turn = 0

print 'Initialized Servos For %s' % const.projectName

# Initialise the pygame library
pygame.init()

# Connect to the first JoyStick
j = pygame.joystick.Joystick(0)
j.init()

print('Initialized Joystick : %s' % j.get_name())

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

try:
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 1:
                    drive = event.value
                elif event.axis == 2:
                    turn = event.value

                driveTotal = drive * 450
                turnTotal = turn * 450

                move = int(1500+driveTotal)
                move2 = int(1500-driveTotal)

                servo.set_servo(constant.leftMotorFrontPin, roundup(move))
                servo.set_servo(constant.leftMotorBackPin, roundup(move))
                servo.set_servo(constant.rightMotorFrontPin, roundup(move2))
                servo.set_servo(constant.rightMotorBackPin, roundup(move2))

                if turnTotal > 0: #Turn Right
                    if driveTotal > 0:
                        turnVal = int(move - turnTotal)
                        print ("Move: ", move, "Turn: ", turnTotal, "Both: ", turnVal)
			servo.set_servo(const.rightMotorFrontPin, roundup(turnVal))
                        servo.set_servo(const.rightMotorBackPin, roundup(turnVal))
			print("Move: ", move, " turn: ", turnTotal)
                    if driveTotal < 0:
                        turnVal = int(move2 - turnTotal)
                        servo.set_servo(const.rightMotorFrontPin, roundup(turnVal))
                        servo.set_servo(const.rightMotorBackPin, roundup(turnVal))
                if turnTotal < 0: #Turn Left
                    if driveTotal > 0:
                        turnVal = int(move + turnTotal)
                        servo.set_servo(const.leftMotorFrontPin, roundup(turnVal))
                        servo.set_servo(const.leftMotorBackPin, roundup(turnVal))
                    if driveTotal < 0:
                        turnVal = int(move - turnTotal)
                        servo.set_servo(const.leftMotorFrontPin, roundup(turnVal))
const		if j.get_button(15):
		    driveVal = int(1500 - driveTotal)
		    servo.set_servo(const.rightMotorFrontPin, roundup(driveVal))
                    servo.set_servo(const.rightMotorBackPin, roundup(driveVal))
		    servo.set_servo(const.leftMotorFrontPin, roundup(driveVal))
                    servo.set_servo(const.leftMotorBackPin, roundup(driveVal))
	    if j.get_button(16):
                j.quit()
                sys.exit()
except KeyboardInterrupt:
    j.quit()#!/usr/bin/env python
