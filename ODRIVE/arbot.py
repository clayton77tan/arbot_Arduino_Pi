## Arbot.py will be used as a preliminary API for our application
from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math



def search_odrive():
	print("Searching . . . ")
	global od
	od = odrive.find_any() # search for the Odrive (may take about 6 seconds)
	global J1 
	J1 = od.axis0 # set J2 to axis1 to control the next motor
	global J2 
	J2 = od.axis1 # set J2 to axis1 to control the next motor

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


