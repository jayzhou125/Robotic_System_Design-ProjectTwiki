#!/usr/bin/env python

import rospy
from math import fabs
from std_msgs.msg import Float32

target = 0.0
value = 0.0
delta = 0.01

def smoother_callback(packet):
    global target

    target = packet.data

def smoother_update():
    global target
    global value
    global delta

    if value < target:
        value += min(target-value, delta)
    elif value > target:
        value -= min(value-target, delta)
    
    print value

def smoother():
    rospy.init_node("smoother", anonymous=True)
    rospy.Subscriber("controller", Float32, smoother_callback)
    
    rate = rospy.Rate(10) # 10 Hz
    
    while not rospy.is_shutdown():
        smoother_update()
        rate.sleep()

if __name__ == "__main__":
	smoother()
