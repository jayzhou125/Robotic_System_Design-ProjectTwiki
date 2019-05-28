#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist


pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=10)
currentCommand = Twist()
currentCommand.linear.x = 0.0
currentCommand.angular.z = 0.0
targetCommand = Twist()
targetCommand.linear.x = 0.0
targetCommand.angular.z = 0.0

def updateCommand(data):
    global targetCommand
    targetCommand = data

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
    rospy.on_shutdown(cleanUp)

    while pub.get_num_connections() == 0:
        pass

    while not rospy.is_shutdown():
        smooth()
        pub.publish(currentCommand)
        rospy.sleep(0.1)

def smooth():
    global targetCommand, currentCommand
    

    DELTA = 0.05

    # smooth x
    t = targetCommand.linear.x
    v = currentCommand.linear.x
    if v < t:
        currentCommand.linear.x += min (t-v, DELTA)
    elif v > t:
        currentCommand -= DELTA

    # smooth z
    t = targetCommand.angular.z
    v = currentCommand.angular.z
    if v < t:
        currentCommand.angular.z += min (t-v, DELTA)
    elif v > t:
        currentCommand.angular.z -= DELTA

if __name__ == '__main__':
    velSmoother()

