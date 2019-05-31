#!/usr/bin/env python

import rospy
from std_msgs.msg import Empty

def resetter():
    pub = rospy.Publisher('/mobile_base/commands/reset_odometry', Empty, queue_size=10)
    rospy.init_node('resetter', anonymous=True)
    while pub.get_num_connections() == 0:
        pass
    pub.publish(Empty())

if __name__ == '__main__':
    try:
        resetter()
    except rospy.ROSInterruptException:
        pass
