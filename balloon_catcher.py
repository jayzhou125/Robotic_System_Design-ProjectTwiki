#!/usr/bin/env python

import rospy
import location
import pid
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from cmvision.msg import Blobs, Blob
from sensor_msgs.msg import Image
from batch_controller import execute, cancel


pub_command = rospy.Publisher("/kobuki_command", Twist, queue_size=10)  # publish command
pub_stop = rospy.Publisher("/emergency_stop", Empty, queue_size=10)   # publish stop

##THOUGHTS:
# we probably need the pid to keep the balloon in the center of the screen
# We also might need to move quickly to the pid (sharpen the movement)

def catcher():

	# get the angle of kinect

	# get the balloon in the center of the screen(ball_tracker)

	# get the distance to the balloon 

	# calculate the forward distance to catch the balloon

	# move the calculated distance 



