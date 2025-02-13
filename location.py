#!/usr/bin/env python

import rospy
import math
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from std_msgs.msg import Float32, Empty

currentLocation = (0, 0, 0)
currentVelocity = 0

verbose = False

pub_reset = rospy.Publisher("/mobile_base/commands/reset_odometry", Empty, queue_size=10)

def resetOdom():
    pub_reset.publish(Empty())


def odomCallback(data):
    global currentLocation, currentVelocity, verbose
    # Convert quaternion to degree
    q = [data.pose.pose.orientation.x,
         data.pose.pose.orientation.y,
         data.pose.pose.orientation.z,
         data.pose.pose.orientation.w]
    roll, pitch, yaw = euler_from_quaternion(q)
    # roll, pitch, and yaw are in radian
    degree = yaw * 180 / math.pi
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
	
    currentLocation = ( x, y, degree ) # record the current location
    currentVelocity = data.twist.twist.linear.x
    if verbose:
        msg = "(%.6f,%.6f) at %.6f degree, moving %.6f" % (x, y, degree, currentVelocity) # format current location
        rospy.loginfo(msg) 	# print the location

def init():
    rospy.Subscriber('/odom', Odometry, odomCallback) # Subscribe to odom node and get position
	
if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="node for controlling robot speed and emergency stops")

    parser.add_argument("-v", "--verbose", dest="verbose", action="store_const", const=True, default=False, help="enable verbose position logging")
    args = parser.parse_args()
    verbose = args.verbose

    rospy.init_node("location_node", anonymous=True) # Initialize this node
    init()
    rospy.spin()

# global MAX_SPEED = 0.8 # this is used to mark when acceleration hits peak (so we can know hwen to slow down)

# publish to constant command
# pub_constant_command = rospy.Publisher("constant_command", Int32, queue_size=10)

# this method should just return the current x value (since we're just 
# moving forward and can reset after each turn)
# y is not necessary, b/c kobuki can't move on y plane
# z may... be important later

# def odomCallbackX(data):	
#     # Convert quaternion to degree
#     q = [data.pose.pose.orientation.x,
#          data.pose.pose.orientation.y,
#          data.pose.pose.orientation.z,
#          data.pose.pose.orientation.w]
#     roll, pitch, yaw = euler_from_quaternion(q)
	
#     # roll, pitch, and yaw are in radian
#     degree = yaw * 180 / math.pi
#     x = data.pose.pose.position.x
	
#     return x;

# # this method should get the desired distance (e.g., one meter) 
# # from the key_node via the /batch channel and calculate when to stop
# def odomCalcCallback() # need to get desiredDistance from /batch command
# 	shouldStop = distance - currentPositionX # if zero then we need to start stopping
	
# 	# record current position (i.e., controller will send a message, when max speed is reached)
# 	currentPositionX = odomCallbackX() # (not sure how to get this but...) we need X value
	
# 	# take desired distance (ex., 1 meter)	
# 	# subtract desired distance - current location (i.e., max speed)
# 	if shouldStop is 0:
# 		# publish to controller (so that it can stop)
# 		pub_constant_command.publish(stop()) # publish within constant command (not sure how to do this)
	

# def batchParse(data): # takes in /batch data ([direction, speed, distance]) and transforms to globals
# 	# TODO: parse string that's sent via /batch and get information
	
# 	global direction, speed, distance = -1 # TODO: remove -1 when parsing is added


	
		# Subscribe to controller
# 	rospy.Subscribe("/batch", Float32MultiArray, batchParse) # will get a float from batch with ([direction, speed, distance]) = data
	
	# not sure where we should put this
	# when the current speed hits the peak acceleration
	# if we later compare to distance, we can know when
	# to start stopping
# 	when speed == MAX_SPEED
# 		odomCalcCallback()
	
	# continue
