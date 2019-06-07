#!/usr/bin/env python

# takes the key_node.py and sents commands to constant_command.py

import rospy
import math
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from std_msgs.msg import Float32, Int32

# publish to constant command
pub_constant_command = rospy.Publisher("constant_command", Int32, queue_size=10)

def moveCallback(data): # from /key command
	# forward, back (meters), left, right (degress)
	if data == 0:
		# move forward with constant_command.py
		# something like .... constant_command.publish(0)
		# should this be constant speed?
		# how do we want to accelerate?
	if data == 1:
		# move backward
	if data == 2:
		# move left
	if data == 3: 
		# move right
	
def direction():
	rospy_init("keypress_node", anonymous=True)
	rospy.Subscribe("key", Int32, moveCallback) # listening for an int (which is the direction command from /key)
	rospy.spin()
	
if __name__ == '__main__':
	direction()