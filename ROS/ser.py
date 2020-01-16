from __future__ import print_function
import serial
from time import sleep

port = "/dev/ttyACM0"
baudrate = 9600
ser = serial.Serial(port, baudrate)

count = 0;
while True:
    ser.write(chr(count))
    count = (count+1)%5
    print("sent", count)
    sleep(2)
