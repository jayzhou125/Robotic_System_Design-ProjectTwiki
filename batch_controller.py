import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import location

SLEEP = 0.01
DELTA_X = 0.5*SLEEP
DELTA_Z = 2*SLEEP
command = None
cancel = False


def stop():
    cancel = True

def terminate():
    cancel = True

pub_command = rospy.Publisher("/kobuki_command", Twist, queue_size=25)   # publish the command 
emergency_stop = rospy.Subscriber("/emergency_stop", Empty, stop)
kill = rospy.Subscriber("/kill", Empty, terminate)


def execute(linear, angular, speed):
    location.resetOdom()
    rospy.sleep(SLEEP)

    if(angular == 0):
        _line(linear, speed)
    elif(linear == 0):
        _turn(angular, speed)
    else:
        _arc(linear, angular, speed)


def _line(distance, speed):
    global SLEEP, DELTA_X, command, pub_command, cancel

    if distance < 0:
	sign = -1
    else:
        sign = 1

    command = Twist()
    command.angular.z = 0
    command.linear.x = 0.1 * sign

    while command.linear.x != 0 and not cancel:
        x, y, theta = location.currentLocation
        cutoff = distance - (sign * (command.linear.x*2) ** 2) # temporary cutoff calculation
        if x >= cutoff and sign > 0:
            command.linear.x -= DELTA_X
	elif x <= cutoff and sign < 0:
            command.linear.x += DELTA_X

        elif command.linear.x < speed and command.linear.x > 0 and sign > 0:
            command.linear.x = min(command.linear.x + DELTA_X, speed)
        elif command.linear.x > -speed and command.linear.x < 0 and sign < 0:
            command.linear.x = max(command.linear.x - DELTA_X, -speed)
            print command.linear.x, -speed

	if abs(x) >= abs(distance):
            command.linear.x = 0
        
	print x, cutoff, command.linear.x
	command.angular.z = 0
        pub_command.publish(command)
        rospy.sleep(SLEEP)
    
    pub_command.publish(Twist())
    

def _turn(distance, speed):
    pass

def _arc(length, radius, speed):
    pass

