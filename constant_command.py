#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from kobuki_msgs.msg import Led, BumperEvent, ButtonEvent

pub_velocity = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=10)
pub_led1 = rospy.Publisher('/mobile_base/commands/led1', Led, queue_size=10)


def zero():
    val = Twist()
    val.angular.z = 0
    val.linear.x = 0
    return val


currentCommand = zero()
targetCommand = zero()

stop = False
bumpers = [False, False, False]
obstructed = False
raw = False

def updateCallback(data):
    global targetCommand
    targetCommand = data

def emergencyStopCallback(data):
    doStop()

def resumeCallback(data):
    doStart()

def bumperCallback(data):
    global bumpers, obstructed
    if data.state == 1:
        doStop()
	bumpers[data.bumper] = True
	obstructed = True
	print "obstructed"
    elif data.state == 0:
	bumpers[data.bumper] = False
	if all(i == False for i in bumpers):
            obstructed = False
            print "unobstructed"


def buttonCallback(data):
    global stop
    if data.button == 0 and data.state == 1: #B0 and pressed
	if stop:
            doStart()
        else:
            doStop()

def doStop():
    global targetCommand, currentCommand, stop
    targetCommand = zero()
    currentCommand = zero()
    stop = True
    ledUpdate(3)
    pub_velocity.publish(zero())
    print "stopping"

def doStart():
    global targetCommand, currentCommand, stop, obstructed

    print "resuming"

    if obstructed:
        print "resume failed, robot is obstructed"
	return

    targetCommand = zero()
    currentCommand = zero()
    stop = False
    ledUpdate(1)
    pub_velocity.publish(zero())

def cleanUp():
    doStop()
    pub_velocity.publish(currentCommand)
    rospy.sleep(1)
    ledUpdate(0)

def smooth():
    global targetCommand, currentCommand, stop, raw

    if stop:
	targetCommand = zero()
        currentCommand = zero()
	pub_velocity.publish(zero())
        return
    
    if raw:
        currentCommand = targetCommand
        return

    
    DELTA_X = 0.02 # was 0.04
    DELTA_Z = 0.3 # was 0.4

    # smooth x
    t = targetCommand.linear.x
    v = currentCommand.linear.x
    if v < t:
        currentCommand.linear.x += min (t-v, DELTA_X)
    elif v > t:
        currentCommand.linear.x -= DELTA_X

    # smooth z
    t = targetCommand.angular.z
    v = currentCommand.angular.z
    if v < t:
        currentCommand.angular.z += min (t-v, DELTA_Z)
    elif v > t:
        currentCommand.angular.z -= DELTA_Z


#update led1 to value
def ledUpdate(value):
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

    rospy.sleep(0.2)
    ledUpdate(1)

    while not rospy.is_shutdown():
	if not stop:
	    smooth()
	    pub_velocity.publish(currentCommand)
	else:
            targetCommand = zero()
            currentCommand = zero()
            pub_velocity.publish(zero())
        rospy.sleep(0.1) 

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="node for controlling robot speed and emergency stops")

    parser.add_argument("-r", "--raw", dest="raw", action="store_const", const=True, default=False, help="use this option to disable constant_command's internal smoothing functionality")
    args = parser.parse_args()
    constantCommand()

