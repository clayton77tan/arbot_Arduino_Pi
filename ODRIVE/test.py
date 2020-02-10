from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

# Find a connected ODrive (this will block until you connect one)
print("Searching . . . ")
od = odrive.find_any() # search for the Odrive (may take about 6 seconds)
J1 = od.axis0 # set J2 to axis1 to control the next motor

# calibrate the motor and encoder of J1
cali = input("Do you want to calibrate (y or n): ")
if(cali == "y"):
    J1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    J1.motor.config.pre_calibrated = True
    J1.encoder.config.pre_calibrated = True
    time.sleep(15)

while True:
    mode = input("Set control mode (v or p): ")
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


