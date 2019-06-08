#!/usr/bin/env python

# takes the input from key_node.py command, determines what to do with it, and sends commands to constant_command.py

import rospy
import math
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, Int32, Empty
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from dir_codes import UP, DOWN, LEFT, RIGHT, STOP #adding directory codes
import odom # is this how we connect odom?


pub_ctrl = rospy.Publisher("/kobuki_command", Twist, queue_size=10)	# publisher kobuki_command
pub_stop = rospy.Publisher("/emergency_stop", Empty, queue_size=10)	# publisher stop

global targetX, targetZ

def keyCallback(data)
    keyPressed = data
    if keyPressed == STOP:	# stop the robot
    	pub_stop.publish(Empty())	
    elif keyPressed == UP：
		# move forward with constant_command.py
		# something like .... constant_command.publish(0)
		# as button is pressed, accelerate
		command.linear.x = SHIFT
    elif keyPressed == DOWN:
		# move backwards
		command.linear.x = -1 * SHIFT
    elif keyPressed == LEFT: 
		# move left
		command.angular.z = SHIFT
    elif keyPressed == RIGHT: 
		# move right
		command.angular.z = -1 * SHIFT

def dxCallback(data)
    targetX = data
	
def dzCallback(data)
    targetZ = data

def keyController():
    rospy.init_node("key_controller", anonymous=True)   # initialize the node	
    rospy.Subscriber("/keys", Int32, keyCallback)	# subscribe to pub_keys
    rospy.Subscriber("/dx", Float32, dxCallback)	# subscribe to pub_dx
    rospy.Subscriber("/dz", Float32, dzCallback)	# subscribe to pub_dz
    rospy.spin()
	
if __name__ == '__main__':
    keyController()
	
	
# # publish to constant_command
# pub_constant_command = rospy.Publisher("constant_command", Int32, queue_size=10) #added

# # publishing from controller
# pub_ctrl = rospy.Publisher("/kobuki_command", Twist, queue_size=10) # do we need this?
# pub_resume = rospy.Publisher("/resume", Empty, queue_size=10)

# input = None
# command = Twist()
# dirty = False
	
# def cleanUp():
# 	global pub_ctrl, command
# 	command.linear.x = 0.0
# 	command.angular.z = 0.0
# 	pub_ctrl.publish(command)
# 	rospy.sleep(1)

# def moveCallback(data): # from /key_handler on /keys channel command
# 	global input, dirty, command # do we need pub_stop?
# 	X_LIMIT = 0.8 # how do we incorporate the x and z limit?
# 	Z_LIMIT = 1.0
    
# 	SHIFT = 0.1

# 	if data == STOP:
# 		# stop the robot
# 		command.linear.x = 0.0
# 		command.angular.z = 0.0
# 		# do we want/need pub_stop?
# 	elif data == UP:
# 		# move forward with constant_command.py
# 		# something like .... constant_command.publish(0)
# 		# as button is pressed, accelerate
# 		command.linear.x = SHIFT
# 	elif data == DOWN:
# 		# move backwards
# 		command.linear.x = -1 * SHIFT
# 	elif data == LEFT: 
# 		# move left
# 		command.angular.z = SHIFT
# 	elif data == RIGHT: 
# 		# move right
# 		command.angular.z = -1 * SHIFT
# 	# do we need else?
  
# 	input = data
# 	dirty = True
# 	pub_constant_command.publish(command) # publish command to constant_command node


	
	
	
# 	global pub_ctrl, command, input, dirty
# 	rospy.init_node("controller", anonymous=True)
# 	rospy.Subscriber("key_node", Int32, moveCallback) # may need to update to what type of information recieving from key_node.py
# 	rospy.on_shutdown(cleanUp)

# 	while not rospy.is_shutdown():
# 		if dirty:
# 			dirty = False
# 			update_command()
# 			pub_ctrl.publish(command)
