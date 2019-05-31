#!/usr/bin/env python

import rospy
import math
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

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

def odomExample():
    rospy.init_node('odom_example', anonymous=True)
    rospy.Subscriber('/odom', Odometry, odomCallback)
    rospy.spin()

if __name__ == '__main__':
    odomExample()
