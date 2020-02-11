## Arbot.py will be used as a preliminary API for our application
## Created by Clayton Tan, Martin Contreras
## 02/07/2020

from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

#  Function initiates the search for an Odrive. To search for a specific Odrive go into the 
#  Odrive tool and find the serialnumber with odrv0.serial_number. Convert that value to hex
#  and use that to find the device as:

## od = odrive.find_any(serial_number="hex number")

def search_odrive():
	print("Searching . . . ")
	global od, J1, J2
	od = odrive.find_any() # search for the Odrive (may take about 6 seconds)
	J1 = od.axis0 # set J2 to axis1 to control the next motor
	J2 = od.axis1 # set J2 to axis1 to control the next motor


# The calibration() function will use the input from the user to choose to 
# calibrate one,two, or all motors on the Odrive. 

def calibration(motors):
    if(motors == "1"):
        J1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        J1.motor.config.pre_calibrated = True
        J1.encoder.config.pre_calibrated = True
        time.sleep(15)

    if(motors == "2"):
        J2.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        J2.motor.config.pre_calibrated = True
        J2.encoder.config.pre_calibrated = True
        time.sleep(15)

    if(motors == "B"): 
        J1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        J1.motor.config.pre_calibrated = True
        J1.encoder.config.pre_calibrated = True
        time.sleep(15)
        J2.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        J2.motor.config.pre_calibrated = True
        J2.encoder.config.pre_calibrated = True
        time.sleep(15)


## This option will allow the user to input the motor (1 or 2) and the mode to execute (v or p).
# Inside they will be continously asked to input the velocity of the motor or the position in
# units of counts. 
def control_motors(motor, mode):
	if motor == "1":
		J1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    	if (mode == "v"):
        	J1.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL
	        while True:
	            speed = input("Set speed (counts/s) or 'q' to quit velocity mode: ")
	            if(speed == "q"):
	                J1.controller.vel_setpoint = 0
	                break
	            else:
	                J1.controller.vel_setpoint = speed
    	elif (mode == "p"):
        	J1.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
        	while True:
		        position = input("Set position (count) or 'q' to quit position mode: ")
		        if(position == "q"):
		            break
		        else:
		            J1.controller.pos_setpoint = position

    if motor == "2":
		J2.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    	if (mode == "v"):
        	J2.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL
	        while True:
	            speed = input("Set speed (counts/s) or 'q' to quit velocity mode: ")
	            if(speed == "q"):
	                J2.controller.vel_setpoint = 0
	                break
	            else:
	                J2.controller.vel_setpoint = speed
    	elif (mode == "p"):
        	J2.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
        	while True:
		        position = input("Set position (count) or 'q' to quit position mode: ")
		        if(position == "q"):
		            break
		        else:
		            J2.controller.pos_setpoint = position


