def search_odrive(): # connect to odrive
	print("Searching . . . ")
	global od, J0, J1
	od = odrive.find_any() # search for the Odrive (may take about 6 seconds)
	J0 = od.axis0 # set J2 to axis1 to control the next motor
	J1 = od.axis1 # set J2 to axis1 to control the next motor
	
	
def angle_count(angle): # angle to counts
	count = float(angle) // -4.09 # 1 count is about 4.09 degrees
	return count # return converted value
	
def control_motors(angle):
	J1.controller.config.control_mode = CTRL_MODE_TRAJECTORY_CONTROL # trajectory mode
	J1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL # loop the controls
	J1.controller.move_to_pos(angle_count(angle)) # move to the set position

#search_odrive() # find odrive

while True:
	file1 = open("/home/arbot/arbot_Arduino_Pi/ODRIVE/file.txt", "r") # open txt file
	file1.seek(0,0)
	anglestr = file1.readline() # read the line of the txt file
	
	with open("/home/arbot/arbot_Arduino_Pi/ODRIVE/file.txt", 'r') as filein:
		text = filein.read().splitlines(True)
	with open("/home/arbot/arbot_Arduino_Pi/ODRIVE/file.txt", 'w') as fileout:
		fileout.writelines(text[1:])
	
	anglelist = anglestr.split(',') # split the string into a list
	angle0 = float(anglelist[0]) # split list into a float
	angle1 = float(anglelist[1]) # split list into a float
	angle2 = float(anglelist[2]) # split list into a float
	angle3 = float(anglelist[3]) # split list into a float
	print(str(angle0) + "\n")
	print(str(angle1) + "\n")
	print(str(angle2) + "\n")
	print(str(angle3) + "\n")
	
	#control_motors(angle1) # control motors
