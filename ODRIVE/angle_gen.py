import math
flag = 1
while True:
	file2 = open("/home/arbot/arbot_Arduino_Pi/ODRIVE/protocol.txt", "r")
	file2.seek(0,0)
	
	if(flag == 1 or file2.readline() == "continue"):
		flag = 0
		count = 1
		file1 = open("/home/arbot/arbot_Arduino_Pi/ODRIVE/angle.txt", "w")
		file1.seek(0,0)

		while(count <= 12):
			if(math.fmod(count,4) != 0):
				file1.write(str(count) + ",")
			elif(math.fmod(count,4) == 0):
				file1.write(str(count) + "\n")
			count = count + 1
		if (count > 12):
			file2 = open("/home/arbot/arbot_Arduino_Pi/ODRIVE/protocol.txt", "w")
			file2.seek(0,0)
			file2.write("stop")
		file1.close()
