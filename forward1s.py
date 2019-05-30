#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import Led #added
from kobuki_msgs.msg import BumperEvent #added


def forward():
	rospy.init_node('forward', anonymous=True)
	pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
	command = Twist()

	while pub.get_num_connections() == 0:
		pass

	command.linear.x = 0.5
	command.angular.z = 0.0
	pub.publish(command)
	rospy.sleep(1.5);
	command.linear.x = 0.2
	pub.publish(command)
	rospy.sleep(1.5);
	
	
	#subscribes to kobuki_command topic
	
	#while running -> set LED1 to green (value 1)
	
	#if B0 is pressed 
		#--> constantly publish stop command
		#----> when running stop --> go back to normal, by constantly publishing the command from kobuki_command
		#--> set LED1 to red (value 3)
		
	#if constant_command is terminated, before it terminates itself, 
	#--> should publish the stop command
	#--> wait for a second
	#--> turn LED1 light off (value 0)
	
	#when bumber state is pressed (value 1) or zero (value 1)
	#--> stop robot 
	#-->set LED1 to red (value 3)

if __name__ == '__main__':
	forward()
