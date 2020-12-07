#!/usr/bin/env python3
...

import rclpy
import os
from array import *
import math
import sys
import threading

from rclpy.node import Node

from std_msgs.msg import String

# declare global variables
l = 0 # global counter
MAX_LIST_LEN = 100 # 5 items(time, angle 0-3) for 20 end effector positions
NUM_EXE = 20 # 20 end effector positions
FREQ = 0.1 # positions updated every 0.1 sec
NUM_ITEMS = 5 # time, angle0, angle1, angle2, angle3 

# declare lists
time = []
angle0 = []
angle1 = []
angle2 = []
angle3 = []

# clear lists
time.clear()
angle0.clear()
angle1.clear()
angle2.clear()
angle3.clear()

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber') # init the subscriber
        self.subscription = self.create_subscription(String,'topic',self.listener_callback,10) # listens in the topic for the callback
        self.subscription  # prevent unused variable warning


    def listener_callback(self, msg): # callback is msg
        self.get_logger().info('I heard: "%s"' % msg.data) # msg.data is the message we get

        # make lists/variables global
        global l
        global MAX_LIST_LEN
        global NUM_EXE
        global FREQ
        global NUM_ITEMS
        global time
        global angle0
        global angle1
        global angle2
        global angle3

        num = msg.data.split(',') # split the string into a list
        numlist = num[0:MAX_LIST_LEN] # make array into list
        listnum = [float(a) for a in numlist] # make into float list

        # counter variables
        i = 0
        j = 0              
        
        # split array into categories
        while i < MAX_LIST_LEN:
            j = i%NUM_ITEMS
            if (j == 0):
                time.append(listnum[i])
            elif(j == 1):
                angle0.append(listnum[i])
            elif(j == 2):
                angle1.append(listnum[i])
            elif(j == 3):
                angle2.append(listnum[i])
            elif(j == 4):
                angle3.append(listnum[i])
            i += 1


        # rearrange if time 1 < time 2
        if (l >= NUM_EXE):
            if (time[0] > time[NUM_EXE]):
                o = 0
                              
                while o < NUM_EXE:
                    time[o], time[o + NUM_EXE] = time[o + NUM_EXE], time[o]
                    angle0[o], angle0[o + NUM_EXE] = angle0[o + NUM_EXE], angle0[o]
                    angle1[o], angle1[o + NUM_EXE] = angle1[o + NUM_EXE], angle1[o]
                    angle2[o], angle2[o + NUM_EXE] = angle2[o + NUM_EXE], angle2[o]
                    angle3[o], angle3[o + NUM_EXE] = angle3[o + NUM_EXE], angle3[o]
                    o += 1  
                
            # remove from time list if time < 0.1
            if (time[NUM_EXE] < FREQ):
                time =  time[:NUM_EXE] + time[NUM_EXE*2:]
                angle0 = angle0[:NUM_EXE] + angle0[NUM_EXE*2:]
                angle1 = angle1[:NUM_EXE] + angle1[NUM_EXE*2:]
                angle2 = angle2[:NUM_EXE] + angle2[NUM_EXE*2:]
                angle3 = angle3[:NUM_EXE] + angle3[NUM_EXE*2:]                 

        # remove from time list if time < 0.1
        if (time[0] < FREQ):
            # execute ODrive commands here
            
            # store in txt file to view
            file = open("/home/arbot/Desktop/time.txt", "a")
            str_time = str(time)
            file.write("Time: " + str(l) + " time = " + str_time + "\n")
            file.close()  
            
            # store in txt file to view
            file = open("/home/arbot/Desktop/Angle0.txt", "a")
            str_angle0 = str(angle0)
            file.write("Time: " + str(l) + " angle0 = " + str_angle0 + "\n")
            file.close()     
            
            # store in txt file to view
            file = open("/home/arbot/Desktop/exetime.txt", "a")
            str_exetime = str(time[0])
            file.write("Time: " + str(l) + " exetime = " + str_exetime + "\n")
            file.close()  
            
            # store in txt file to view
            file = open("/home/arbot/Desktop/exeAngle0.txt", "a")
            str_exeangle0 = str(angle0[0])
            file.write("Time: " + str(l) + " exeangle0 = " + str_exeangle0 + "\n")
            file.close()             
            
            time =  time[NUM_EXE:]
            angle0 = angle0[NUM_EXE:]
            angle1 = angle1[NUM_EXE:]
            angle2 = angle2[NUM_EXE:]
            angle3 = angle3[NUM_EXE:]                                                               

        time[:] = [k - FREQ for k in time] # subtract 0.1 sec from each time
        l += 1


def main(args=None):
    rclpy.init(args=args) # initializes rclpy

    minimal_subscriber = MinimalSubscriber() # minimalsub class assigned to minimal sub variable

    rclpy.spin(minimal_subscriber) # everytime rclpy spins, minimalsub class is called

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
