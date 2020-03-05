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
processcount = 0



# fucntion for subtracting 1 sec from time
def process_time(staticTime):
	dynamicTime = [(-1 + sec) for sec in staticTime]
	return dynamicTime



processedTime.clear() # clear the processedtime list
time.clear() # clear the time list
angle.clear() # clear the angle list
text = open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", "r") # open txt file
while True:

	# text.seek(0,0) # start at beginning of text file
	textstr = text.readline() # read the line of the txt file
	textlist = textstr.split(',') # split the string into a list

	if(textlist[0] and textlist[0] != '\n'): # check if textlist is empty or not
		txt = textlist[0:4] # store in a list
		listtext = [int(z) for z in txt] # convert strings to ints
		angle.append(listtext) # append to angle list
		time.append(textlist[4:5]) # append to time list
		
		# read the entire text file to pop the current line off the text file
		# with open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", 'r') as filein1:
			# text = filein1.read().splitlines(True)
		# with open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", 'w') as fileout1:
			# fileout1.writelines(text[1:])
		
	index = index + 1 # counter for each line read
	
	timelist = [''.join(line) for line in time] # make list of list into one list
	newtime = [new[:-1] for new in timelist] # get rid of \n
	listtime = [int(x) for x in newtime] # make list items from str to int


	if(math.fmod(index,20) == 0): # check if script has read 20 lines from txt file
		delay = threading.Event() # clear a dummy event
		delay.wait(1) # 1 sec delay
		
		if(processcount > 0): # check if processedTime is empty or not
			listtime[0:len(processedTime)] = processedTime[0:len(processedTime)] # overwrite listtime with old listtime since each element has been subtracted by 1
		processcount = processcount + 1 # on overwrite if it isn't the 1st index because it's empty
		
		if(listtime[0:20] != ([0]*20)): # check if listtime is empty or not so we don't subtract more than zero
			processedTime = process_time(listtime) # call function to subtract time by 1
		
		if(processedTime[0:20] == ([0]*20)): # check if time has counted down to zero or not
			processedTime = processedTime[20:] # pop the first 20 values off the processedTime list
			time = time[20:] # pop the first 20 values off the time list to ensure it doesn't rewrite ther values again
			
			while(angleODrive < 20 and angle): # process the first 20 joint angles
				print(str(angle[0][0]) + ',' +str(angle[0][1]) + ',' +str(angle[0][2]) + ',' +str(angle[0][3]))
				# print(str(angle[0][0]))
				# print(str(angle[0][1]))
				# print(str(angle[0][2]))
				# print(str(angle[0][3]))
				# print('\n')
				angle = angle[1:][:] # pop the 1st row off
				angleODrive = angleODrive + 1 # increase row count
			angleODrive = 0
	
