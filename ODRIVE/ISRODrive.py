import os
from array import *
from numpy import array
from numpy import empty
import odrive
from odrive.enums import *
import time
import math
import sys
import threading

angle = []
time = []

while True:
	file1 = open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", "r") # open txt file
	file1.seek(0,0)
	anglestr = file1.readline() # read the line of the txt file
	
	anglelist = anglestr.split(',') # split the string into a list
	


	if(anglelist[0]):
		angle.append(anglelist)
		print(angle[1])

	with open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", 'r') as filein1:
		text = filein1.read().splitlines(True)
	with open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", 'w') as fileout1:
		fileout1.writelines(text[1:])
