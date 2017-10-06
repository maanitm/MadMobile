import smbus
import time
import pygame
import const
from os import sys
import RPi.GPIO as GPIO

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

# Initialise the pygame library
pygame.init()

# Connect to the first JoyStick
j = pygame.joystick.Joystick(0)
j.init()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        a = 0
        time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
        time2 = time.time()
    during = time2 - time1
    return during * 340 / 2 * 100

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
    GPIO.cleanup()
    j.quit()
    pygame.quit()
    sys.exit()

def startDrive():
    global stopped
    global manual
    global currentSpeed
    try:
        while not stopped:
	    dis = distance()
            print(dis, "cm")
            print("")
            time.sleep(0.3)
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
        stopDrive()
