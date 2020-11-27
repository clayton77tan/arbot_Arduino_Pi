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

# declare lists
l = 0
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

        # make lists global
        global l
        global time
        global angle0
        global angle1
        global angle2
        global angle3

        num = msg.data.split(',') # split the string into a list
        numlist = num[0:100] # make array into list
        listnum = [float(a) for a in numlist] # make into float list

        # counter variables
        i = 0
        j = 0
        m = 0
        n = 0
        
        
        # split array into categories
        while i < 100:
            j = i%5
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
            i = i + 1

        if (l > 19):
            if (time[20] < time[0]):
                o = 0;
                while o < 20:
                    time[o], time[o + 20] = time[o + 20], time[o]
                    o = o + 1
            # remove from time list if time < 0.1
            if (time[20] < 0.1):
                time =  time[:20] + time[40:]
                angle0 = angle0[:20] + angle0[40:]
                angle1 = angle1[:20] + angle1[40:]
                angle2 = angle2[:20] + angle2[40:]
                angle3 = angle3[:20] + angle3[40:]                 



        # remove from time list if time < 0.1
        if (time[0] < 0.1):
            time =  time[20:]
            angle0 = angle0[20:]
            angle1 = angle1[20:]
            angle2 = angle2[20:]
            angle3 = angle3[20:]
            

        
        # store in txt file to view
        file = open("/home/arbot/Desktop/Time.txt", "a")
        str_time = str(time)
        file.write("time = " + str_time + "\n")
        file.close()
        
        # store in txt file to view
        file = open("/home/arbot/Desktop/ExeTime.txt", "a")
        str_exetime = str(time[0])
        file.write("exetime = " + str_exetime + "\n")
        file.close()
        
        # # store in txt file to view
        # file = open("/home/arbot/Desktop/Angle0.txt", "a")
        # str_angle0 = str(angle0)
        # file.write("angle0 = " + str_angle0 + "\n")
        # file.close()     
        
        # # store in txt file to view
        # file = open("/home/arbot/Desktop/Angle1.txt", "a")
        # str_angle1 = str(angle1)
        # file.write("angle1 = " + str_angle1 + "\n")
        # file.close() 
        
        # # store in txt file to view
        # file = open("/home/arbot/Desktop/Angle2.txt", "a")
        # str_angle2 = str(angle2)
        # file.write("angle2 = " + str_angle2 + "\n")
        # file.close() 
        
        # # store in txt file to view
        # file = open("/home/arbot/Desktop/Angle3.txt", "a")
        # str_angle3 = str(angle3)
        # file.write("angle3 = " + str_angle3 + "\n")
        # file.close() 
                                                       


        time[:] = [k - 0.1 for k in time] # subtract 0.1 sec from each time
        l = l + 1



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
