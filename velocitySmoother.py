#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty


pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=10)

zero = Twist()
zero.angular.z = 0.0
zero.linear.x = 0.0

currentCommand = zero
targetCommand = zero

stop = False

def updateCommand(data):
    global targetCommand
    targetCommand = data

def stopCommand(data):
    global targetCommand, stop
    targetCommand = zero
    stop = True

def cleanUp():
    global currentCommand
    currentCommand.linear.x = 0.0
    currentCommand.angular.z = 0.0
    pub.publish(currentCommand)
    rospy.sleep(1)

def velSmoother():
    global pub, targetCommand, currentCommand
    rospy.init_node("velocitySmoother", anonymous=True)
    rospy.Subscriber("kobuki_command", Twist, updateCommand)
    rospy.Subscriber("emergency_stop", Empty, stopCommand)
    rospy.on_shutdown(cleanUp)

    while pub.get_num_connections() == 0:
        pass

    while not rospy.is_shutdown():
        smooth()
        pub.publish(currentCommand)
        rospy.sleep(0.1)

def smooth():
    global targetCommand, currentCommand, stop

    if stop:
        currentCommand = zero
        stop = False
        return
    

    X_DELTA = 0.07

    Z_DELTA = 0.4

    # smooth x
    t = targetCommand.linear.x
    v = currentCommand.linear.x
    if v < t:
        currentCommand.linear.x += min (t-v, X_DELTA)
    elif v > t:
        currentCommand.linear.x -= X_DELTA

    # smooth z
    t = targetCommand.angular.z
    v = currentCommand.angular.z
    if v < t:
        currentCommand.angular.z += min (t-v, Z_DELTA)
    elif v > t:
        currentCommand.angular.z -= Z_DELTA

if __name__ == '__main__':
    velSmoother()

