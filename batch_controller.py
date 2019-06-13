import rospy
from geometry_msgs.msg import Twist
from location import currentLocation, resetOdom

SLEEP = 0.05
DELTA_X = 0.05*SLEEP
DELTA_Z = 0.4*SLEEP
command
cancel = False

pub_command = rospy.Publisher("/constant_command", Twist, queue_size=25)   # publish the command 
emergency_stop = rospy.Subscriber("/emergency_stop", Empty, stop)

def stop():
    cancel = True

def execute(linear, angular, speed):
    if(angular == 0):
        _line(linear, speed)
    elif(linear == 0):
        _turn(angular, speed)
    else:
        _arc(linear, angular, speed)


def _line(distance, speed):
    global SLEEP, DELTA_X, command, pub_command
    resetOdom()

    command = Twist()
    command.angular.z = 0
    command.linear.x = 0.1

    while command.linear.x > 0 and not cancel:
        x, y, theta = currentLocation
        cutoff = distance - (command.linear.x) ** 2 # temporary cutoff calculation
        if x >= cutoff:
            command.linear.x -= DELTA_X
        elif abs(command.linear.x) < abs(speed):
            command.linear.x = min(command.linear.x + DELTA_X, speed)
        
        pub_command.publish(command)
        rospy.sleep(SLEEP)
    
    print "final position: {0}".format(currentLocation.x)
    

def _turn(distance, speed):
    pass

def _arc(length, radius, speed):
    pass

