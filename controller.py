#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32

def controller():
    pub = rospy.Publisher("controller", Float32)
    rospy.init_node("controller", anonymous=True)

    query_str = "Please enter a floating-point number: "

    while not rospy.is_shutdown():
        data = raw_input(query_str)
        try:
            data = float(data)
        except ValueError:
            print "INVALID"
            continue
        
        pub.publish(data)

if __name__ == "__main__":
    controller()
