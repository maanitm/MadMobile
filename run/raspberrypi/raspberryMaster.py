import smbus
import time
import pygame

drive = 0

# Initialise the pygame library
pygame.init()

# Connect to the first JoyStick
j = pygame.joystick.Joystick(0)
j.init()

print 'Initialized Joystick : %s' % j.get_name()

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

def writeNumber(value):
  bus.write_byte(address, value)
  # bus.write_byte_data(address, 0, value)
  return -1

def readNumber():
  number = bus.read_byte(address)
  # number = bus.read_byte_data(address, 1)
  return number

def stopDrive():
    writeNumber(0)
    print("Stopping ...")
    j.quit()
    pygame.quit()
    sys.exit()

def startDrive():
    try:
        while True:
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
    	        continue

	    if var >= 75:
  	        writeNumber(var)
  	        print "RPI: Hi Arduino, I sent you ", var
  	        # sleep tenth second
  	        time.sleep(0.1)
            if j.get_button(3):
	        writeNumber(130)
	        print "RPI: Hi Arduino, I sent you ", 130
	        time.sleep(0.1)
	    if j.get_button(16):
		stopDrive()
    except KeyboardInterrupt:
        j.quit()#!/usr/bin/env python
        pygame.quit()
