import rospy
from std_msgs.msg import String
from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math
import sys

def search_odrive(): # connect to odrive
	print("Searching . . . ")
	global od, J0, J1
	global Listcount
	global angleList = []
	od = odrive.find_any() # search for the Odrive (may take about 6 seconds)
	J0 = od.axis0 # set J2 to axis1 to control the next motor
	J1 = od.axis1 # set J2 to axis1 to control the next motor

def calibration(): # calibrate encoder and motor
	print("in calibration")
	J1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	J1.motor.config.pre_calibrated = True
	J1.encoder.config.pre_calibrated = True
	time.sleep(15)

def angle_count(angle): # angle to counts
	count = float(angle) // -4.09
	return count

def control_motors(angle):
	J1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	J1.controller.config.control_mode = CTRL_MODE_TRAJECTORY_CONTROL
	J1.controller.move_to_pos(angle_count(angle))

#pub = rospy.Publisher('chatter', String,queue_size = 10)

def callback(data): # ROS receive angles and drive motor
    str1 = data.data
    listx= [int(s) for s in str1.split() if s.isdigit()]
    for inty in listx:
        listAngle = inty
    angleList.append(listAngle)
    Listcount = Listcount + 1

    rospy.loginfo(rospy.get_caller_id() + ' Joint Angle: %s', listAngle)
    
    for intangle in listAngle:
		angle = intangle
    control_motors(angle)

def listener():
	
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('chatter', String, callback)

    # # spin() simply keeps python from exiting until this node is stopped
    # rospy.spin()
    
    # if (Listcount == 10):
		# received_str = "Received Array"
		# rospy.loginfo(received_str)
		# pub.publish(received_str)

if __name__ == '__main__':
	search_odrive()
	calibration()
    listener()

