#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from kobuki_msgs.msg import Led #added
from kobuki_msgs.msg import BumperEvent #added
from kobuki_msgs.msg import ButtonEvent #added

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

	
	#subscribes to kobuki_command topic
#Subscribe('kobuki_command',Twist,queue_size=10)
#Subscribe('velocitySmoother',Twist,queue_size=10)
#Subscribe('/mobile_base/events/button',Twist,queue_size=10)
#Subscriber('/mobile_base/events/bumper', BumperEvent, bumperStop)
	
#while running 
while not rospy.is_shutdown():
	ledUpate(1) # set /mobile_base/commands/led1 to green (value 1)
	
	#if B0 is pressed (the first time) (value 0)
	if(data.button == 0) #B0
		ledUpdate(3) #set /mobile_base/commands/led1 to red (value 3)
		if (data.state == 1) #pressed
			stopCommand() #constantly publish stop command
		if (data.button == 0) # when running stopped and press B0 (i.e., pressing B0 twice)
			# todo: go back to normal, by constantly publishing the command from kobuki_command

	#when bumper state is pressed (value 1) or released (value 0)
	bumperStop()

	#todo: if constant_command is terminated, before it terminates itself, 
		stopCommand() # should publish the stop command
		rospy.sleep(1.)# wait for a second
		ledUpdate(0) # turn LED1 light off (value 0)

#update led1 to value
def ledUpdate(int value):
	pub1 = rospy.Subscriber('/mobile_base/commands/led1',Led,queue_size=10)
	while pub1.get_num_connections() == 0
		pass
	led = Led()
	x = value

#update bumper to stop when released (value 0) or pressed (value 1)
def bumperStop(data):
	if(data.state == 0 or data.state == 1)
		ledUpdate(3) # set /mobile_base/commands/led1 to red (value 3)
		stopCommand() # stop robot 
	
if __name__ == '__main__':
    velSmoother()

