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

# intialize variables
angle = []
time = []
index = 0
timeIndex = 0
processedTime = []
angleIndex = 0
angleODrive = 0


# fucntion for subtracting 1 sec from time
def process_time(staticTime):
	dynamicTime = [(-1 + sec) for sec in staticTime]
	return dynamicTime



processedTime.clear() # clear the processedtime list
time.clear() # clear the time list
angle.clear() # clear the angle list

while True:
	text = open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", "r") # open txt file
	text.seek(0,0) # start at beginning of text file
	textstr = text.readline() # read the line of the txt file
	
	textlist = textstr.split(',') # split the string into a list

	if(textlist[0] and textlist[0] != '\n'): # check if textlist is empty or not
		txt = textlist[0:4]
		listtext = [int(z) for z in txt]
		angle.append(listtext) # append to angle list
		time.append(textlist[4:5]) # append to time list
		index = index + 1 # counter for each line read
	
	timelist = [''.join(line) for line in time] # make list of list into one list
	newtime = [new[:-1] for new in timelist] # get rid of \n
	listtime = [int(x) for x in newtime] # make list items from str to int
	
	
	if(math.fmod(index,20) == 0): # check if script has read 20 lines from txt file
		delay = threading.Event() # clear a dummy event
		delay.wait(1) # 1 sec delay
		
		if(processedTime): # check if processedTime is empty or not
			listtime[0:len(processedTime)] = processedTime[0:len(processedTime)] # overwrite listtime with old listtime since each element has been subtracted by 1

		processedTime = process_time(listtime) # call function to subtract time by 1
		if(processedTime and processedTime[0:20] == ([0]*20)): # check if time has counted down to zero or not
			processedTime = processedTime[20:] # pop the first 20 values off the processedTime list
			time = time[20:] # pop the first 20 values off the time list to ensure it doesn't rewrite ther values again
			
			# process the first 20 joint angles
			while(angleODrive < 20):
				print(angle[0][:])
				angle = angle[1:][:]
				angleODrive = angleODrive + 1
			angleODrive = 0
		

	# read the entire text file to pop the current line off the text file
	with open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", 'r') as filein1:
		text = filein1.read().splitlines(True)
	with open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", 'w') as fileout1:
		fileout1.writelines(text[1:])
	
