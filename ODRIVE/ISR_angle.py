import math
import time
import threading

# intialize variables
count = 201
file1 = open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", "w")
file1.seek(0,0)
flag = 10000
incre = 1

while True:
	while(count <= 300): # count to 100
		if(math.fmod(count,5) != 0):
			file1.write(str(count) + ",") # separate by ','
		elif(math.fmod(count,5) == 0):
			file1.write(str(5 + incre) + "\n") # separate by '\n' every 5th number
		count = count + 1 # increment the count
	if(count > 300): # check if the count has reached 100
		incre = incre + 1 # increment time
		# while(flag > 1): # blocking delay to reset count back to 1
			# flag = flag - 1
		# count = 1 # reset count to 1
		# flag = 10000 # reset the flag
		break
