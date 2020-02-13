import arbot

# Find a connected ODrive (this will block until you connect one)
arbot.search_odrive()

# prompt calibrate the motor and encoder of J1
calibrate_from_start = input("Do you want to calibrate (0,1,B,or N): ")
arbot.calibration(calibrate_from_start)

while True:
	motor = input("Select a motor to change the position(0,1,q): ")
	if motor == "q":
		arbot.shut_down()
	else:
		arbot.control_motors(motor)


