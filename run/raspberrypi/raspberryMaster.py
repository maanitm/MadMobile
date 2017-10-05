import smbus
import time
import pygame
from flask import Flask, render_template, request
from os import sys

app = Flask(__name__)

stopped = False

drive = 0

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/writeNumber/<int:value>')
def writeNumber(value):
  bus.write_byte(address, value)
  # bus.write_byte_data(address, 0, value)
  return index()

def readNumber():
  number = bus.read_byte(address)
  # number = bus.read_byte_data(address, 1)
  return number

@app.route('/stopDrive')
def stopDrive():
    global stopped
    stopped = True
    writeNumber(0)
    print "Stopped ..."

@app.route('/startDrive')
def startDrive():
    # Initialise the pygame library
    pygame.init()

    # Connect to the first JoyStick
    j = pygame.joystick.Joystick(0)
    j.init()

    print 'Initialized Joystick : %s' % j.get_name()

    global stopped
    global drive
    stopped = False
    try:
        while not stopped:
            print(stopped)
	    events = pygame.event.get()
            for event in events:
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 1:
                        drive = event.value

	    var = int(drive * 128) * -1
	    var = var + 75
	    if var > 128:
	        var = 128

	    if not var and var is not 0:
    	        var = 0

	    if var >= 75:
  	        writeNumber(var)
  	        print "RPI: Hi Arduino, I sent you ", var
  	        # sleep tenth second
  	        time.sleep(0.1)
            if j.get_button(3):
	        toggleAuto()
	    if j.get_button(16):
		stopDrive()
    except KeyboardInterrupt:
        j.quit()#!/usr/bin/env python
        pygame.quit()

    return render_template('index.html')

@app.route('/toggleAuto')
def toggleAuto():
    writeNumber(130)
    print "RPI: Hi Arduino, I sent you ", 130
    time.sleep(0.1)
    return render_template('index.html')

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0')

