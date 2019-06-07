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

# publish to constant_command
pub_constant_command = rospy.Publisher("constant_command", Int32, queue_size=10) #added

# publishing from controller
pub_ctrl = rospy.Publisher("/kobuki_command", Twist, queue_size=10) # do we need this?
pub_resume = rospy.Publisher("/resume", Empty, queue_size=10)

input = None
command = Twist()
dirty = False
	
def cleanUp():
    global pub_ctrl, command
    command.linear.x = 0.0
    command.angular.z = 0.0
    pub_ctrl.publish(command)
    rospy.sleep(1)

def remoteController():
    global pub_ctrl, command, input, dirty
    rospy.init_node("controller", anonymous=True)
    rospy.Subscriber("key_node", Int32, moveCallback) # may need to update to what type of information recieving from key_node.py
    rospy.on_shutdown(cleanUp)

    while not rospy.is_shutdown():
        if dirty:
            dirty = False
            update_command()
            pub_ctrl.publish(command)

    #rospy.spin()

# TODO: Need to update update_command()
def update_command():
    global input, command, pub_stop
    
    # turning
    Z_LIMIT = 1.0
    raw_z = input.axes[0] # LR stick left

    if raw_z < 0:
        command.angular.z = max(raw_z, -1*Z_LIMIT)
    elif raw_z > 0:
	    command.angular.z = min(raw_z, Z_LIMIT)

    # forward/backward
    X_LIMIT = 0.8
    raw_x = input.axes[5] # right trigger
    invert = input.buttons[0] == 1

    raw_x = ((-1*raw_x) + 1) / 2 # convert depressing right trigger to 0 > 1 instead of 1 > -1

    trim_x = min(raw_x, X_LIMIT)

    if invert:
	    trim_x *= -1

    command.linear.x = trim_x



def moveCallback(data): # from /key_handler on /keys channel command
    global input, dirty

    if data == STOP:
	# stop the robot
	command.linear.x = 0.0
	command.angular.z = 0.0
    elif data == UP:
	# move forward with constant_command.py
	# something like .... constant_command.publish(0)
	# should this be constant speed?
	# how do we want to accelerate?
    elif data == DOWN:
	# move backwards
    elif data == LEFT: 
	# move left
    elif data == RIGHT: 
	# move right
	# do we need else?
    

    input = data
    dirty = True
    pub_constant_command.publish(command) # publish command to constant_command node
	
if __name__ == '__main__':
    remoteController()
