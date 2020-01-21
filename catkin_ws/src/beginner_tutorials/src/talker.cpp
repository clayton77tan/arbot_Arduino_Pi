// code explaination in below link
// wiki.ros.org/roscpp_tutorials/Tutorials/WritingPublisherSubscriber
#include "ros/ros.h"
#include "std_msgs/String.h"

#include <sstream>

int main(int argc, char **argv){
	ros::init(argc, argv, "talker"); // initalize ROS

	ros::NodeHandle n; // initialize Node

	ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000); // publish to to chatter topic

	ros::Rate loop_rate(10); // 10Hz loop

	int count = 0;
	while (ros::ok()){
		std_msgs::String msg;

		std::stringstream ss;
		ss << "hello world " << count; // put hello world and count in string
		msg.data = ss.str(); // put string to msg data

		ROS_INFO("%s", msg.data.c_str()); // print out msg data

		chatter_pub.publish(msg); // publish string

		ros::spinOnce();

		loop_rate.sleep(); // sleep
		++count;
	}
	return 0;
}
