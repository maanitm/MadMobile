import time
import pygame
import const
from os import sys
import RPi.GPIO as GPIO
from threading import Thread
from multiprocessing import Process
import subprocess
import serial

print("Raspberry Pi Master")

driveSer = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
turnSer = serial.Serial('/dev/ttyACM1', 9600, timeout=1)

stopped = False
currentSpeed = 0
currentTurn = 0
manual = True
frontDistance = 400
TRIG = 20
ECHO = 21

jValue = 0

pygame.init()

j = pygame.joystick.Joystick(0)
j.init()

# setup GPIO and variables before starting
def setup():
    global stopped
    global currentSpeed
    global currentTurn
    global manual
    global frontDistance
    global jValue

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    stopped = False
    currentSpeed = 0
    currentTurn = 0
    manual = True
    frontDistance = 400
    jValue = 0


# measure distance between ultrasonic sensor and object
def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    start = time.time()

    while GPIO.input(ECHO)==0:
        pass

    start = time.time()

    while GPIO.input(ECHO)==1:
        pass

    stop = time.time()

    elapsed = stop - start

    return elapsed * 340 / 2 * 100

# set motor speed
def setSpeed(speed):
    # writeNumber(speed, driveAddress)
    print("-------------------")
    print(speed)
    try:
        driveSer.write(speed)
    except IOError:
        print("disconnected")

    time.sleep(0.1)

# set motor speed
def setTurn(turn):
    if turn < 0:
        newTurn = 100 - (turn * -1)
    else:
        newTurn = turn + 100

    print("-------------------")
    print(turnAddress)
    print(newTurn/2)

    try:
        turnSer.write(newTurn/2)
    except IOError:
        print("disconnected")

    # writeNumber(int(newTurn/2), turnAddress)
    time.sleep(3)

# get PS3 joystick value
def getJoystickXValue():
    global manual
    global jValue
    jBefore = jValue
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 1:
                jValue = event.value
        if j.get_button(11) and manual:
            print("Cruise")
            manual = False
        if j.get_button(10) and not manual:
            print("Manual")
            manual = True
        elif j.get_button(16):
            stopDrive()

    if not jValue and jValue is not 0:
        return jBefore
    return jValue

def getJoystickYValue():
    global manual
    global jValue
    jBefore = jValue
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 2:
                jValue = event.value
        if j.get_button(16):
            stopDrive()

    if not jValue and jValue is not 0:
        return jBefore
    return jValue

# enable manual driving and return speed
def manualDrive():
    driveV = getJoystickXValue()

    driveV = int(driveV * 53) * -1
    driveV = driveV + 75
    if driveV > 128:
        driveV = 128
    if driveV < 0:
        driveV = const.motorZeroSpeed

    return driveV

# enable cruise control and return speed
def cruiseControl():
    driveV = 0
    jValue = getJoystickXValue()
    stopDif = const.cruiseMaxStopDistance - const.cruiseMinStopDistance
    stopDistance = (currentSpeed - const.motorZeroSpeed) * 14.8148148148

    if stopDistance < const.cruiseMinStopDistance:
        stopDistance = const.cruiseMinStopDistance
    if stopDistance > const.cruiseMaxStopDistance:
        stopDistance = const.cruiseMaxStopDistance

    if frontDistance < stopDistance:
        driveV = const.motorZeroSpeed
    elif frontDistance <= 400 and frontDistance > stopDistance:
        driveV = int(frontDistance/30) + const.motorZeroSpeed
    else:
        if currentSpeed + const.cruiseSpeedIncrement < const.cruiseTopSpeed:
            driveV = currentSpeed
            driveV += const.cruiseSpeedIncrement
        else:
            driveV = currentSpeed

    # print driveV, " driveV"

    return driveV

# stop drive and close program
def stopDrive():
    global stopped
    stopped = True
    driveSer.write(0)
    turnSer.write(50)
    print("Stopping ... ")
    cur.close()
    db.close()
    driveSer.close()
    turnSer.close()
    GPIO.cleanup()
    j.quit()
    pygame.quit()
    sys.exit()

# repeatedly return distance values until stopped
def distanceLoop():
    global frontDistance
    try:
        while not stopped:
            frontDistance = distance()
            # print frontDistance,"cm"
            time.sleep(0.3)
    except KeyboardInterrupt:
        stopDrive()

# repeatedly apply voltage to motor based on drive type until stopped
def driveLoop():
    global stopped
    global manual
    global currentSpeed
    try:
        while not stopped:
            print "drive"
            if manual:
                currentSpeed = manualDrive()
            else:
                currentSpeed = cruiseControl()

            if currentSpeed <= const.motorMaxSpeed and currentSpeed >= const.motorZeroSpeed:
                setSpeed(currentSpeed)

    except KeyboardInterrupt:
        stopDrive()

def turnLoop():
    global currentTurn
    global stopped
    try:
        while not stopped:
	        print "turn"
            turnP = getJoystickYValue() * 100
            currentTurn = turnP
            setTurn(int(turnP))

    except KeyboardInterrupt:
        stopDrive()

# start drive and multiple threads and main method
def startDrive():
    setup()
    t1 = Thread(target = driveLoop)
    t2 = Thread(target = distanceLoop)
    t4 = Thread(target = turnLoop)

    t1.start()
    # t2.start()
    t4.start()
