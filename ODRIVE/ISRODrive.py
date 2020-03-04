import os
from array import *
# from numpy import array
# from numpy import empty
# import odrive
# from odrive.enums import *
import time
import math
import sys
import threading


angle = []
time = []
index = 0
timeIndex = 0


def process_time(staticTime):
	dynamicTime = [(-1 + sec) for sec in staticTime]
	return dynamicTime

while True:
	text = open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", "r") # open txt file
	text.seek(0,0)
	textstr = text.readline() # read the line of the txt file
	
	textlist = textstr.split(',') # split the string into a list

	if(textlist[0]):
		angle.append(textlist[0:4])
		# print("angle: " + str(angle[index]))
		time.append(textlist[4:5])
		# print("time: " + str(time[index]))
		index = index + 1
	
	timelist = [''.join(line) for line in time]
	newtime = [new[:-1] for new in timelist]
	listtime = [int(x) for x in newtime]
	
	delay = threading.Event()
	delay.wait(1)
	dynamicTime = process_time(listtime)
	
	
	
	# if (dynamicTime[timeIndex] == 0):
		

	with open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", 'r') as filein1:
		text = filein1.read().splitlines(True)
	with open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", 'w') as fileout1:
		fileout1.writelines(text[1:])
	
