#include "ros/ros.h"
#include "std_msgs/String.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <PublisherSubscriber.h>

template<>
void PublisherSubscriber<std_msgs::String,std_msgs::String>::subscriberCallback(const std_msgs::String::ConstPtr& receivedMsg){
	ROS_INFO("I received the following from talker: %s", receivedMsg->data.c_str());
	std_msgs::String echo_msg;
	echo_msg.data = receivedMsg->data;
	ROS_INFO("Sending the received message to echo: %s", echo_msg.data.c_str());
	publisherObject.publish(echo_msg);
}

int main(int argc, char **argv){
	ros::init(argc, argv, "pub sub demo");
	PublisherSubscriber<std_msgs::String, std_msgs::String> parrot("echo","chatter", 1000);
	ros::spin();
}

