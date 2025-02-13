#!/usr/bin/env python

# takes the input from key_node.py command, determines what to do with it, and sends commands to constant_command.py

import rospy
import math
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, Int32, Empty
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from dir_codes import UP, DOWN, LEFT, RIGHT, STOP #adding directory codes
# import odom # is this how we connect odom?


pub_ctrl = rospy.Publisher("/kobuki_command", Twist, queue_size=10)	# publisher kobuki_command
pub_stop = rospy.Publisher("/emergency_stop", Empty, queue_size=10)	# publisher stop
# pub_resume = rospy.Publisher("/resume", Empty, queue_size=10)

# we probably need brake and reset (the lt and Y to control the robot better)!!!!!!!!!!!!!!!!!!!!!!!

targetX = 0.0
targetZ = 0.0
keyPressed = None
command = Twist()
dirty = False

def cleanUp():
    global pub_ctrl, command
    command.linear.x = 0.0
    command.angular.z = 0.0
    pub_ctrl.publish(command)
    rospy.sleep(1)

def keyCallback(data):
    global keyPressed, dirty
    keyPressed = data.data
    dirty = True

def update_command():
    global pub_ctrl, command, keyPressed, dirty, targetX, targetZ
    print "We are in update-command method"	
    # stop
    print "this is keypress inside the method " ,keyPressed
    if keyPressed == 0:	# stop the robot
	command.angular.z = 0.0
        command.linear.x = 0.0
	print "We are in stop"

    # forward
    if keyPressed == UP:
	command.linear.x = 0.8
	
    # backward
    if keyPressed == DOWN:
	command.linear.x = -0.8
	print "We are in up"
   
    # turn left
    if keyPressed == LEFT:
	command.angular.z = 1.0
	print "We are in left"
	
    # turn right
    if keyPressed == RIGHT:
	command.angular.z = -1.0
	print "We are in right"
    

def dxCallback(data):
    targetX = data
	
def dzCallback(data):
    targetZ = data

def keyController():
    global dirty, pub_ctrl
    rospy.init_node("key_controller", anonymous=True)   # initialize the node	
    rospy.Subscriber("/keys", Int32, keyCallback)	# subscribe to pub_keys
    rospy.Subscriber("/dx", Float32, dxCallback)	# subscribe to pub_dx
    rospy.Subscriber("/dz", Float32, dzCallback)	# subscribe to pub_dz
	
    rospy.on_shutdown(cleanUp)

    while not rospy.is_shutdown():
        if dirty:
            dirty = False
            update_command()
            pub_ctrl.publish(command)
	rospy.sleep(0.03)
    rospy.spin()
	
if __name__ == '__main__':
    keyController()







	

