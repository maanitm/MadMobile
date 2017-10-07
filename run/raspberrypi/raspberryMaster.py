import smbus
import time
import pygame
import const
from os import sys
import RPi.GPIO as GPIO
from threading import Thread

print("Raspberry Pi Master")

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

stopped = False
currentSpeed = 0
manual = True
frontDistance = 400
TRIG = 20
ECHO = 21

jValue = 0

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

    start = time.time()

    while GPIO.input(ECHO)==0:    #Wait for the echo to go high- starting the measurement.
        pass

    start = time.time()

    while GPIO.input(ECHO)==1:    #Wait for the echo to go low
        pass

    stop = time.time()

    # Calculate pulse length
    elapsed = stop-start

    return elapsed * 340 / 2 * 100

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
    global jValue
    jBefore = jValue
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 1:
                jValue = event.value
        if j.get_button(11) and manual:
            print("NOT manual")
            manual = False
        if j.get_button(10) and not manual:
            print("manual")
            manual = True
        elif j.get_button(16):
            stopDrive()

    if not jValue and jValue is not 0:
        return jBefore
    return jValue

def manualDrive():
    driveV = getJoystickXValue()

    driveV = int(driveV * 53) * -1
    driveV = driveV + 75
    if driveV > 128:
        driveV = 128
    if driveV < 0:
        driveV = const.motorZeroSpeed

    return driveV

def cruiseControl():
    jValue = getJoystickXValue()
    # stopDif = const.cruiseMaxStopDistance - const.cruiseMinStopDistance
    # stopDistance = (currentSpeed - const.motorZeroSpeed) * 14.8148148148
    #
    # if stopDistance < const.cruiseMinStopDistance:
    #    stopDistance = const.cruiseMinStopDistance
    # if stopDistance > const.cruiseMaxStopDistance:
    #    stopDistance = const.cruiseMaxStopDistance
    #
    # if distance < stopDistance:
    #    driveV = const.motorZeroSpeed
    # elif distance <= 4 and distance > stopDistance:
    #    driveV = int(distance/0.3) + const.motorZeroSpeed
    # else:
    #    if driveV + const.cruiseSpeedIncrement < const.cruiseTopSpeed:
    #        driveV += const.cruiseSpeedIncrement

    driveV = int(frontDistance/27) + 75

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

def distanceLoop():
    global frontDistance
    try:
        while not stopped:
            frontDistance = distance()
            print(frontDistance)
            time.sleep(0.3)
    except KeyboardInterrupt:
        stopDrive()

def driveLoop():
    global stopped
    global manual
    global currentSpeed
    try:
        while not stopped:
            if manual:
                currentSpeed = manualDrive()
            else:
                currentSpeed = cruiseControl()

            if currentSpeed <= const.motorMaxSpeed and currentSpeed >= const.motorZeroSpeed:
                setSpeed(currentSpeed)

            print(manual)

    except KeyboardInterrupt:
        stopDrive()

def startDrive():
    setup()
    t1 = Thread(target = driveLoop)
    t2 = Thread(target = distanceLoop)

    t1.start()
    t2.start()
