#!/usr/bin/env python3
...

import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber') # init the subscriber
        self.subscription = self.create_subscription(String,'topic',self.listener_callback,10) # listens in the topic for the callback
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg): # callback is msg
        self.get_logger().info('I heard: "%s"' % msg.data) # msg.data is the message we get
	

        num = msg.data.split(',') # split the string into a list
        time = float(num[0])
        angle0 = float(num[1]) # split list into a float
        angle1 = float(num[2]) # split list into a float
        angle2 = float(num[3]) # split list into a float
        angle3 = float(num[4]) # split list into a float


        #print(time)
        #print(angle0)
        #print(angle1)
        #print(angle2)
        #print(angle3)

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
