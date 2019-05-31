#!/usr/bin/env python

import rospy
from kobuki_msgs.msg import BumperEvent

def bumperCallback(data):
    str = ""
    if data.bumper == 0:
        str = str + "Left bumper is "
    elif data.bumper == 1:
        str = str + "Center bumper is "
    else:
        str = str + "Right bumper is "

    if data.state == 0:
        str = str + "released."
    else:
        str = str + "pressed."

    rospy.loginfo(str)

def bumperExample():
    rospy.init_node('bumper_example', anonymous=True)
    rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, bumperCallback)
    rospy.spin()

if __name__ == '__main__':
    bumperExample()
