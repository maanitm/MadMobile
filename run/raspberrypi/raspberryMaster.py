import smbus
import time
import pygame
import const
from os import sys
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

print("Raspberry Pi Master")

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

stopped = False
currentSpeed = 0
manual = True

TRIG = 4
ECHO = 17

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)

# Initialise the pygame library
pygame.init()

# Connect to the first JoyStick
j = pygame.joystick.Joystick(0)
j.init()

def writeNumber(value):
  bus.write_byte(address, value)
  # bus.write_byte_data(address, 0, value)
  return -1

def readNumber():
  number = bus.read_byte(address)
  # number = bus.read_byte_data(address, 1)
  return number

def setSpeed(speed):
    writeNumber(speed)
    time.sleep(0.1)

def getJoystickXValue():
    value = 0
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 1:
                value = event.value
    return value

def manualDrive():
    driveV = getJoystickXValue()

    driveV = int(driveV * 128) * -1
    driveV = driveV + 75
    if driveV > 128:
        driveV = 128

    return driveV

def cruiseControl():
    global currentSpeed
    print(currentSpeed)
    #stopDif = const.cruiseMaxStopDistance - const.cruiseMinStopDistance
    #stopDistance = (currentSpeed - const.motorZeroSpeed) * 14.8148148148

    #if stopDistance < const.cruiseMinStopDistance:
    #    stopDistance = const.cruiseMinStopDistance
    #if stopDistance > const.cruiseMaxStopDistance:
    #    stopDistance = const.cruiseMaxStopDistance

    distance = ultrasonic.distance
    print(distance)

    #if distance < stopDistance:
    #    driveV = const.motorZeroSpeed
    #elif distance <= 4 and distance > stopDistance:
    #    driveV = int(distance/0.3) + const.motorZeroSpeed
    #else:
    #    if driveV + const.cruiseSpeedIncrement < const.cruiseTopSpeed:
    #        driveV += const.cruiseSpeedIncrement

    driveV = int(27/distance) + 75

    print(driveV)
    return driveV

def stopDrive():
    global stopped
    stopped = True
    writeNumber(0)
    print("Stopping ...")
    j.quit()
    pygame.quit()
    sys.exit()

def startDrive():
    global stopped
    global manual
    global currentSpeed
    try:
	GPIO.output(TRIG, False)                 #Set TRIG as LOW
        print "Waitng For Sensor To Settle"
        time.sleep(2)
        while not stopped:
	    GPIO.output(TRIG, True)                  #Set TRIG as HIGH
            time.sleep(0.00001)                      #Delay of 0.00001 seconds
            GPIO.output(TRIG, False)
            while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
                pulse_start = time.time()              #Saves the last known time of LOW pulse

            while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
                pulse_end = time.time()                #Saves the last known time of HIGH pulse

            pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

            distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
            distance = round(distance, 2)            #Round to two decimal points

            if distance > 2 and distance < 400:      #Check whether the distance is within range
                print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
            else:
                print "Out Of Range"
            if not manual:
        	print("1")
                currentSpeed = cruiseControl()
        	print("2")
            else:
                currentSpeed = manualDrive()

                if not currentSpeed and currentSpeed is not 0:
                    continue

                if currentSpeed <= const.motorMaxSpeed and currentSpeed >= const.motorZeroSpeed:
                    setSpeed(currentSpeed)

                if j.get_button(3):
    		    if not manual:
    		        manual = True
    		    else:
    		        manual = False

                if j.get_button(16):
                    stopDrive()

    except KeyboardInterrupt:
        writeNumber(0)
        j.quit()#!/usr/bin/env python
        pygame.quit()
