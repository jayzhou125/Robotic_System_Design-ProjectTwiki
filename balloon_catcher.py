#!/usr/bin/env python

import rospy
import location
import pid
from std_msgs.msg import Empty, Float64
from geometry_msgs.msg import Twist
from cmvision.msg import Blobs, Blob
from sensor_msgs.msg import Image
from batch_controller import execute, cancel
from rightTriangle import *
from struct import pack, unpack
from balloon_tracking_test import scan


pub_command = rospy.Publisher("/kobuki_command", Twist, queue_size=10)  # publish command
pub_stop = rospy.Publisher("/emergency_stop", Empty, queue_size=10)   # publish stop
kinect_angle = 0.0

depth_map = Image()

##THOUGHTS:
# we probably need the pid to keep the balloon in the center of the screen
# We also might need to move quickly to the pid (sharpen the movement)


# get the angle of kinect
def angleCallback(data):
	global kinect_angle
	kinect_angle = data.data

def depthCallback(data):
	global depth_map
	depth_map = data

def getDepth(x, y):
	global depth_map
	data = depth_map.data
	offset = (depth_map.step * y) + (4 * x)
	dist = unpack('f', depth_map.data[offset] + depth_map.data[offset+1] + depth_map.data[offset+2] + depth_map.data[offset+3])
	return dist[0]

def cleanUp():
	global pub_stop
	pub_stop.publish(Empty())

def catcher():
	global pub_stop, pub_command, kinect_angle

	rospy.init_node("balloon_catcher")
	rospy.Subscriber("/cur_tilt_angle", Float64, angleCallback)
	rospy.Subscriber("/camera/depth/image", Image, depthCallback)
	rospy.on_shutdown(cleanUp)

	# get the balloon in the center of the screen(ball_tracker)
	targetBlob = scan(pub_command)
	
	KINECT_ANGLE_PER_PIXEL = 10
	
	# calculate angle from ground to camera-balloon line
	angle = kinect_angle + (targetBlob.y - (depth_map.height/2))/KINECT_ANGLE_PER_PIXEL

	# get the distance to the balloon 
	dist = getDepth(targetBlob.x, targetBlob.y)
	vertical = getOpposite(angle, dist)
	horizontal = getAdjacent(angle, dist)

	print "balloon detected {} meters from camera".format(dist)
	print "height {} meters, estimated landing point {} meters".format(vertical, horizontal)

	# move the calculated distance 


if __name__ == "__main__":
	catcher()
