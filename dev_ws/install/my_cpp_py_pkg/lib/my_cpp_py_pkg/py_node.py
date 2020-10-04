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

l = 0
rmtime = []
time = []
angle0 = []
angle1 = []
angle2 = []
angle3 = []

rmtime.clear()
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

        global l

        num = msg.data.split(',') # split the string into a list
        numlist = num[0:100]
        listnum = [float(a) for a in numlist]

        #print(listnum)    

        i = 0
        j = 0
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

        print("time[0]: ", time[0])

        if (time[0] < 0.1 and l == 0):
            rmtime =  time[20:]
        else:
            if(rmtime[0] < 0.1 and l != 0):
                rmtime = time[20:]
            else:
                rmtime = time
            #print("in condition")
        print("rmtime: ", rmtime)

        listtime = [float(b) for b in rmtime]
        listangle0 = [float(c) for c in angle0]
        listangle1 = [float(d) for d in angle1]
        listangle2 = [float(e) for e in angle2]
        listangle3 = [float(f) for f in angle3]

        #print(listtime)
        #print(listangle0)
        #print(listangle1)
        #print(listangle2)
        #print(listangle3)

        time[:] = [k - 0.1 for k in time]

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
