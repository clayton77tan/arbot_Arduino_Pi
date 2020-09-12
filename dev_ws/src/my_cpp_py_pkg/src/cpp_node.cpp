#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include <iostream>
#include <stdlib.h>
#include <time.h> 

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;
using namespace std;

/* This example creates a subclass of Node and uses std::bind() to register a
 * member function as a callback from the timer. */

class MinimalPublisher : public rclcpp::Node
{
	public:
		MinimalPublisher()
			: Node("minimal_publisher"), count_(0)
		{
			publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
			timer_ = this->create_wall_timer(
					100ms, std::bind(&MinimalPublisher::timer_callback, this));
		}

	private:
		void timer_callback()
		{
			auto message = std_msgs::msg::String();
			message.data = to_string(count_++) + ", " + to_string(count_ + 1) + ", " + to_string(count_ + 2) + ", " + to_string(count_ + 3) + ", " + to_string(count_ + 4);
			RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
			publisher_->publish(message);
		}
		rclcpp::TimerBase::SharedPtr timer_;
		rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
		size_t count_;
};

int main(int argc, char * argv[])
{
	rclcpp::init(argc, argv);
	rclcpp::spin(std::make_shared<MinimalPublisher>());
	rclcpp::shutdown();
	return 0;
}

