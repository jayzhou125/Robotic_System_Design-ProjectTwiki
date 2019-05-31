#!/usr/bin/env python

import rospy
from kobuki_msgs.msg import Led

def sendLEDs():
    rospy.init_node('leds_sender', anonymous=True)
    pub1 = rospy.Publisher('/mobile_base/commands/led1', Led, queue_size=10)
    pub2 = rospy.Publisher('/mobile_base/commands/led2', Led, queue_size=10)
    while pub1.get_num_connections() == 0 or pub2.get_num_connections() == 0:
        pass
    led = Led()
    x = 3
    while x != -1:
        led.value = x
        pub1.publish(led)
        x = x - 1
        rospy.sleep(1)

    x = 3
    while x != -1:
        led.value = x
        pub2.publish(led)
        x = x - 1
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        sendLEDs()
    except rospy.ROSInterruptException:
        pass
