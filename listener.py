#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def callback(data):
    print Listener heard “[message]” from the message.
def listener():
    rospy.init_node("listener", anonymous=True)
    rospy.Subscriber("chatter2", String, callback)
    rospy.spin()
if __name__ == '__main__':
    listener()
