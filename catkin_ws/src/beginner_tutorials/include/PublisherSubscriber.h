#ifndef PUBLISHER_SUBSCRIBER_H
#define PUBLISHER_SUBSCRIBER_H

#include "ros/ros.h"
#include "std_msgs/String.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <PublisherSubscriber.h>

template<typename PublishT,typename SubscribeT>
class PublisherSubscriber{
	public:
		PublisherSubscriber(){}
		PublisherSubscriber(std::string publishTopicName, std::string subscribeTopicName, int queueSize){
			publisherObject = nH.advertise<PublishT>(publishTopicName, queueSize);
			subscriberObject = nH.subscribe<SubscribeT>(subscribeTopicName, queueSize, &PublisherSubscriber::subscriberCallback, this);
		}
		void subscriberCallback(const typename SubscribeT::ConstPtr& receivedMsg);
	protected:
		ros::Subscriber subscriberObject;
		ros::Publisher publisherObject;
		ros::NodeHandle nH;
};

#endif
