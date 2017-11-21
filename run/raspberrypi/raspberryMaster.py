import smbus
import time
import pygame
import const
from os import sys
import RPi.GPIO as GPIO
from threading import Thread
#import MySQLdb

print("Raspberry Pi Master")

bus = smbus.SMBus(1)

# arduino slave motor address
address = 0x06

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

# setup GPIO and variables before starting
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

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

# send number through serial to arduino
def writeNumber(value):
  print(address)
  print(value)
  bus.write_byte_data(address, 201, value)
  return value

# read number through serial from arduino
def readNumber():
  number = bus.read_byte(address)
  return number

# set motor speed
def setSpeed(speed):
    writeNumber(speed)
    time.sleep(0.1)

# set motor speed
def setTurn(turn):
    if turn < 0:
        newTurn = 100 - (turn * -1)
    else:
        newTurn = turn + 100

    writeNumber(int(newTurn/2))
    change = (newTurn/2) - readNumber()
    time.sleep(3.0 * (float(newTurn/2)/100.0))

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
    writeNumber(0)
    print("Stopping ... ")
    cur.close()
    db.close()
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
    global phoneSpeed
    try:
        while not stopped:
            print phoneSpeed, "mph"
            if manual:
                currentSpeed = manualDrive()
            else:
                currentSpeed = cruiseControl()

            if currentSpeed <= const.motorMaxSpeed and currentSpeed >= const.motorZeroSpeed:
                setSpeed(currentSpeed)

    except KeyboardInterrupt:
        stopDrive()

# get data from mysql database and store in global variables until stopped
def dataLoop():
    global phoneSpeed
    try:
        while not stopped:
            db = MySQLdb.connect(host="localhost", user="admin", passwd="madmobile1234", db="madmobile")
            cur = db.cursor()
            cur.execute("SELECT * FROM madmobile.liveData ORDER BY id DESC")
            row = cur.fetchone()
            objId = int(row[0])
            objType = str(row[1])
            objValue = str(row[2])
            objDate = str(row[3])

            if objType == "speed":
                phoneSpeed = objValue

            print phoneSpeed
            #test closure of Cursor after every loop to recheck the database (may crash !!!)
            cur.close()
    except KeyboardInterrupt:
        stopDrive()

def turnLoop():
    global currentTurn
    global stopped
    try:
        while not stopped:
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
    t3 = Thread(target = dataLoop)
    t4 = Thread(target = turnLoop)

    # t1.start()
    # t2.start()
    # t3.start()
    t4.start()
