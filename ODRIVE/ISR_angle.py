import math
import time
import threading

count = 1
file1 = open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", "w")
file1.seek(0,0)
flag = 10000

while True:
	while(count <= 15):
		if(math.fmod(count,5) != 0):
			file1.write(str(count) + ",")
		elif(math.fmod(count,5) == 0):
			file1.write(str(count) + "\n")
		count = count + 1
	if(count > 15):
		while(flag > 1):
			flag = flag - 1
		count = 1
		flag = 10000
		# break
