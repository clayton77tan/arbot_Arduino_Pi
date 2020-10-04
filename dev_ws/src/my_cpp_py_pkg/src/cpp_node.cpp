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
		float round(float var){
			float value = (int)(var * 1000 + .5);
			return (float)value / 1000;
		}
		void timer_callback(){
			srand (time(NULL));

			double arr[20][5]={};

			arr[0][0] = round(2.49 + static_cast <double> (rand()) / ( static_cast <double> (RAND_MAX/(2.685-2.49))));
			for(int i = 0; i< 20; i++){
				arr[i][0]= arr[0][0]; 
				for(int j = 1; j< 5; j++){
					arr[i][j] = round(-90 + static_cast <double> (rand()) / ( static_cast <double> (RAND_MAX/(90-(-90)))));
				}
			}

			auto message = std_msgs::msg::String();

			for(int k = 0; k<20;k++){
				for(int l = 0;l<5;l++){
					if(l == 0 && k == 0){
						message.data = to_string(arr[k][l]) + ", ";
					}
					else if(l == 4 && k != 19){
						message.data = message.data + to_string(arr[k][l]) + ", ";
					}
					else if(l == 4 && k == 19){
						message.data = message.data + to_string(arr[k][l]);
					}
					else{
						message.data = message.data + to_string(arr[k][l]) + ", ";
					}
				}
			}
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

