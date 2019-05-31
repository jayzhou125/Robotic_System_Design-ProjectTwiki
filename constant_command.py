#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from kobuki_msgs.msg import Led, BumperEvent, ButtonEvent

pub_velocity = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=10)
pub_led1 = rospy.Publisher('/mobile_base/commands/led1', Led, queue_size=10)

zero = Twist()
zero.angular.z = 0.0
zero.linear.x = 0.0

currentCommand = zero
targetCommand = zero

stop = False

def updateCallback(data):
    global targetCommand
    targetCommand = data

def emergencyStopCallback(data):
    stop()

def resumeCallback(data):
    start()

def bumperCallback(data):
    if data.state == 1:
        stop()

def buttonCallback(data):
    global stop
    if data.button == 0 and data.state == 1: #B0 and pressed
		if stop:
            start()
        else:
            stop()


def stop():
    global targetCommand, stop
    targetCommand = zero
    stop = True
    ledUpdate(1)

def start():
    global targetCommand, stop
    targetCommand = zero
    stop = False
    ledUpdate(3)

def cleanUp():
    stop()
    pub_velocity.publish(currentCommand)
    rospy.sleep(1)
    ledUpdate(0)

def smooth():
    global targetCommand, currentCommand, stop

    if stop:
        currentCommand = zero
        return
    
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


#update led1 to value
def ledUpdate(int value):
    global pub_led1
	led = Led()
    led.value = value
    pub_led1.publish(value)
	


def constantCommand():
    global pub_velocity, targetCommand, currentCommand
    rospy.init_node("velocitySmoother", anonymous=True)
    rospy.Subscriber("/kobuki_command", Twist, updateCallback)
    rospy.Subscriber("/emergency_stop", Empty, emergencyStopCallback)
    rospy.Subscriber("/resume", Empty, resumeCallback)
    rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, bumperCallback)
    rospy.Subscriber("/mobile_base/events/button", ButtonEvent, buttonCallback)
    rospy.on_shutdown(cleanUp)

    while pub_velocity.get_num_connections() == 0:
        pass

    while not rospy.is_shutdown():
        smooth()
        pub_velocity.publish(currentCommand)
        rospy.sleep(0.1)

if __name__ == '__main__':
    constantCommand()

