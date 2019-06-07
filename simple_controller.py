# Lab 4 - v1/ ideas
# Create a very simple control program that make the robot move forward at 0.3 for 2 seconds and
# then move backward at 0.3 for 2 seconds and stop

# Side note: I heard we're also going to need to make the bot move forward 1 meter exactly 
# Example on GitHub: https://github.com/markwsilliman/turtlebot/blob/master/goforward.py 

#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
import math #added
from nav_msgs.msg import Odometry #added
from tf.transformations import euler_from_quaternion #added

def controller():
    pub = rospy.Publisher("simple_controller", Float32) #updated node to match node name
    rospy.init_node("simple_controller", anonymous=True) #updated node to match node name

    while not rospy.is_shutdown():
        moveForward(0.3, 2) # added
        moveBackwards(0.3,2) # added

#should break out into it's own node
def moveForward(double delta, int seconds):
  #must insert here

#should break out into it's own node
def moveBackwards(double delta, int seconds):
  #must insert here

#added from odom_example
def odomCallback(data):
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
    msg = "(%.6f,%.6f) at %.6f degree." % (x, y, degree) 
    rospy.loginfo(msg)
    
if __name__ == "__main__":
    controller()
