#!/usr/bin/env python

import rospy
import math
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from std_msgs.msg import Float32

global MAX_SPEED = 0.8

# publish to constant command
pub_constant_command = rospy.Publisher("constant_command", Int32, queue_size=10)


def odomCallbackX(data):	
    # Convert quaternion to degree
    q = [data.pose.pose.orientation.x,
         data.pose.pose.orientation.y,
         data.pose.pose.orientation.z,
         data.pose.pose.orientation.w]
    roll, pitch, yaw = euler_from_quaternion(q)
	
    # roll, pitch, and yaw are in radian
    degree = yaw * 180 / math.pi
    x = data.pose.pose.position.x
	
	return x;
   
def odomCalcCallback() # need to get desiredDistance from /batch command
	# record current position (i.e., controller will send a message, when max speed is reached)
	currentPositionX = odomCallbackX() # not how this works
	
	# take desired distance (ex., 1 meter)	
	# subtract desired distance - current location (i.e., max speed)
	if (distance - currentPositionX == 0):
		# publish to controller (so that it can stop)
		pub_constant_command.publish(stop()) # publish within constant command
	

def batchParse(data): # takes in /batch data ([direction, speed, distance]) and transforms to globals
	# parse string and get information
	# TODO
	
	global direction, speed, distance = -1 # remove -1 when parsing is added

def listen():
	# Initialize this node
	rospy_init("odom_node", anonymous=True) # note: may not need to initialize, b/c it is part of controller
	
	# Subscribe to controller
	rospy.Subscribe("/batch", Float32MultiArray, batchParse) # will get a float from batch with ([direction, speed, distance]) = data
	
	# Subscribe to odom node and get position
	rospy.Subscriber('/odom', Odometry, odomCallback) 

	#when speed == MAX_SPEED
		#odomCalcCallback()
	
	# continue
	rospy.spin()
	

if __name__ == '__main__':
	listen()
