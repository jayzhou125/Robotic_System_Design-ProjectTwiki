#!/usr/bin/env python

import rospy
from kobuki_msgs.msg import Sound

def sendSounds():
    rospy.init_node('sound_sender', anonymous=True)
    pub = rospy.Publisher('/mobile_base/commands/sound', Sound, queue_size=10)
    while pub.get_num_connections() == 0:
        pass
    s = Sound()
    for x in range (0,7):
        s.value = x
        pub.publish(s)
        rospy.sleep(1.5)

if __name__ == '__main__':
    try:
        sendSounds()
    except rospy.ROSInterruptException:
        pass
