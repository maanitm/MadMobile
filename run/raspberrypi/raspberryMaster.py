import smbus
import time
import pygame
import const
from os import sys
import RPi.GPIO as GPIO
from threading import Thread
import MySQLdb

print("Raspberry Pi Master")

db = MySQLdb.connect(host="localhost", user="admin", passwd="madmobile1234", db="madmobile")
cur = db.cursor()

bus = smbus.SMBus(1)

# arduino slave motor address
address = 0x04

stopped = False
currentSpeed = 0
phoneSpeed = 0
manual = True
frontDistance = 400
TRIG = 20
ECHO = 21

jValue = 0

pygame.init()

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

    while GPIO.input(ECHO)==0:
        pass

    start = time.time()

    while GPIO.input(ECHO)==1:
        pass

    stop = time.time()

    elapsed = stop - start

    return elapsed * 340 / 2 * 100

def writeNumber(value):
  bus.write_byte(address, value)
  return -1

def readNumber():
  number = bus.read_byte(address)
  return number

def setSpeed(speed):
    writeNumber(speed)
    time.sleep(0.1)

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

def stopDrive():
    global stopped
    stopped = True
    writeNumber(0)
    print("Stopping ... ")
    cur.close()
    db.close()
    GPIO.cleanup()
    j.quit()
    pygame.quit()
    sys.exit()

def distanceLoop():
    global frontDistance
    try:
        while not stopped:
            frontDistance = distance()
            # print frontDistance,"cm"
            time.sleep(0.3)
    except KeyboardInterrupt:
        stopDrive()

def driveLoop():
    global stopped
    global manual
    global currentSpeed
    global phoneSpeed
    try:
        while not stopped:
            # print phoneSpeed, "mph"
            if manual:
                currentSpeed = manualDrive()
            else:
                currentSpeed = cruiseControl()

            if currentSpeed <= const.motorMaxSpeed and currentSpeed >= const.motorZeroSpeed:
                setSpeed(currentSpeed)

    except KeyboardInterrupt:
        stopDrive()

def dataLoop():
    global cur
    global phoneSpeed
    try:
        while not stopped:
            cur.execute("SELECT * FROM madmobile.liveData")
            row = cur.fetchone()
            objId = int(row['id'])
            objType = str(row['type'])
            objValue = str(row['value'])
            objDate = str(row['date'])

            if objType == "speed":
                phoneSpeed = objValue

            print phoneSpeed
    except KeyboardInterrupt:
        stopDrive()

def startDrive():
    setup()
    t1 = Thread(target = driveLoop)
    t2 = Thread(target = distanceLoop)
    t3 = Thread(target = dataLoop)

    t1.start()
    t2.start()
    t3.start()
