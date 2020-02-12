import arbot

# Find a connected ODrive (this will block until you connect one)
arbot.search_odrive()

# prompt calibrate the motor and encoder of J1
calibrate_from_start = input("Do you want to calibrate (0,1,B,or N): ")
arbot.calibration(calibrate_from_start)

while True:
    motor,mode = input("Select a motor (0 or 1) and set the control mode (v or p) [Ex: 1,v]: ").split(',')
    arbot.control_motors(motor,mode)


