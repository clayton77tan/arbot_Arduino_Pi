#include "ros/ros.h"
#include "std_msgs/String.h"
#include <iostream>
#include <fstream>
using namespace std;

void chatterCallback(const std_msgs::String::ConstPtr& msg){
	std::fstream myfile;
	myfile.open("/home/logan/catkin_ws/src/beginner_tutorials/launch/file.txt", std::ios_base::app);
	ROS_INFO("I heard: [%s]", msg->data.c_str());
	myfile << msg->data.c_str() << "\r\n";
	//myfile.close();
}

int main(int argc, char **argv){
	ros::init(argc, argv, "listener");

	ros::NodeHandle n;
	ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallback);

	ros::spin();

	return 0;
}
