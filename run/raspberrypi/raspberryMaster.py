import smbus
import time
import pygame
from gpiozero import DistanceSensor
import const
from os import sys

print(const.projectName)

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

stopped = False

distance = 0
manual = True

# Initialise the pygame library
pygame.init()

# Connect to the first JoyStick
j = pygame.joystick.Joystick(0)
j.init()

ultrasonic = DistanceSensor(echo=17, trigger=4, max_distance=4)

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
    stopDif = const.cruiseMaxStopDistance - const.cruiseMinStopDistance
    stopDistance = (currentSpeed - const.motorZeroSpeed) * 14.8148148148

    if stopDistance < const.cruiseMinStopDistance:
        stopDistance = const.cruiseMinStopDistance
    if stopDistance > const.cruiseMaxStopDistance:
        stopDistance = const.cruiseMaxStopDistance

    distance = ultrasonic.distance

    if distance < stopDistance:
        driveV = const.motorZeroSpeed
    elif distance <= 4 and distance > stopDistance:
        driveV = int(distance/0.3) + const.motorZeroSpeed
    else:
        if driveV + const.cruiseSpeedIncrement < const.cruiseTopSpeed:
            driveV += const.cruiseSpeedIncrement

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
    try:
        while not stopped:
            if not manual:
                driveV = cruiseControl()
            else:
                driveV = manualDrive()

            if not driveV and driveV is not 0:
                continue

            if driveV > const.motorMaxSpeed:
                setSpeed(const.motorMaxSpeed)
                continue

            if driveV >= const.motorZeroSpeed:
      	        setSpeed(driveV)

            if j.get_button(3):
                manual = True

            if j.get_button(16):
                stopDrive()
    except KeyboardInterrupt:
        writeNumber(0)
        j.quit()#!/usr/bin/env python
        pygame.quit()
