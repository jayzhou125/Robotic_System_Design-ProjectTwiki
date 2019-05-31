#!/usr/bin/env python

import rospy
from kobuki_msgs.msg import ButtonEvent

def buttonCallback(data):
    str = ""
    if data.button == 0:
        str = str + "Button 0 is "
    elif data.button == 1:
        str = str + "Button 1 is "
    else:
        str = str + "Button 2 is "

    if data.state == 0:
        str = str + "released."
    else:
        str = str + "pressed."

    rospy.loginfo(str)

def bumperExample():
    rospy.init_node('button_example', anonymous=True)
    rospy.Subscriber('/mobile_base/events/button', ButtonEvent, buttonCallback)
    rospy.spin()

if __name__ == '__main__':
    bumperExample()
