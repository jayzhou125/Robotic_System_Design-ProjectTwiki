import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import location
import math

SLEEP = 0.01
DELTA_X = 0.5*SLEEP
DELTA_Z = 1*SLEEP
command = None
cancel = False


def stop():
    global cancel
    cancel = True

def terminate():
    global cancel
    cancel = True

def zero():
    t = Twist()
    t.angular.z = 0
    t.linear.x = 0
    return t

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
    
    pub_command.publish(zero())
    

def _turn(degrees, speed):
    global SLEEP, DELTA_Z, command, pub_command, cancel

    if degrees < 0:
	sign = -1
    else:
        sign = 1

    command = Twist()
    command.linear.x = 0
    command.angular.z = 0.1 * sign
    
    loops = 0
    theta_prev = 0
    theta_total = 0

    while command.angular.z != 0 and not cancel:
        x, y, theta = location.currentLocation
        cutoff = degrees - (sign * (command.angular.z*6.5) ** 2) # temporary cutoff calculation

	if ((theta < 0 and theta_prev > 0 and sign > 0)	# loop over from 180 to -180 during positive rotation
        or (theta > 0 and theta_prev < 0 and sign < 0)):	# loop over from -180 to 180 during negative rotation
            loops += 1
        
        theta_prev = theta
        theta_total = theta + (sign * 360 * loops)

        if theta_total >= cutoff and sign > 0:
            command.angular.z -= DELTA_Z
	elif theta_total <= cutoff and sign < 0:
            command.angular.z += DELTA_Z

        elif command.angular.z < speed and command.angular.z > 0 and sign > 0:
            command.angular.z = min(command.angular.z + DELTA_Z, speed)
        elif command.angular.z > -speed and command.angular.z < 0 and sign < 0:
            command.angular.z = max(command.angular.z - DELTA_Z, -speed)

	if abs(theta_total) >= abs(degrees):
            command.angular.z = 0
        
	print theta, theta_total, cutoff, command.angular.z
	command.linear.x = 0
        pub_command.publish(command)
        rospy.sleep(SLEEP)
    
    pub_command.publish(zero())
    


def _arc(length, radius, speed):
    global SLEEP, DELTA_X, command, pub_command, cancel
    radians = (length / radius)
    degrees = radians  * 180/math.pi
    x_dest = radius * math.cos(radians)
    y_dest = radius * (1-math.sin(radians))


    # for a given arc, angular speed and linear speed have a fixed ratio determined by the radius of the arc
    

    if length < 0:
	sign = -1
    else:
        sign = 1

    if degrees < 0:
        turn_sign = -sign
    else:
        turn_sign = sign

    command = Twist()
    command.angular.z = 0
    command.linear.x = 0.1
    
    loops = 0
    theta_prev = 0
    theta_total = 0
    x_prev = 0
    y_prev = 0
    dx_prev = 0
    d_total = 0

    timeout = 50
    print sign, turn_sign

    while command.linear.x != 0 and not cancel and timeout > 0:
	timeout -= 1
        x, y, theta = location.currentLocation
        cutoff = length - (sign * (command.linear.x*2) ** 2) # temporary cutoff calculation

	if ((theta < 0 and theta_prev > 0 and sign > 0)	# loop over from 180 to -180 during positive rotation
        or (theta > 0 and theta_prev < 0 and sign < 0)):	# loop over from -180 to 180 during negative rotation
            loops += 1

        dt = theta - theta_prev
        theta_next = theta + dt
	tn_radians = theta_next * math.pi/180
        theta_prev = theta
        theta_total = theta + (turn_sign * 360 * loops)

        dx = x - x_prev
        dy = y - y_prev

        d = sign * math.sqrt(dx ** 2 + dy ** 2)
        d_total += d


	x_target = radius * math.cos(tn_radians)
        y_target = radius * (1 - math.sin(tn_radians))

        x_next = x + d*math.sin(tn_radians)
        y_next = y + d*math.cos(tn_radians)
	
        radius_current = x_next/math.cos(tn_radians)
        

        if d_total >= cutoff and sign > 0:
            command.linear.x -= DELTA_X
	elif d_total <= cutoff and sign < 0:
            command.linear.x += DELTA_X

        elif command.linear.x < speed and command.linear.x > 0 and sign > 0:
            command.linear.x = min(command.linear.x + DELTA_X, speed)
        elif command.linear.x > -speed and command.linear.x < 0 and sign < 0:
            command.linear.x = max(command.linear.x - DELTA_X, -speed)

        if radius_current > radius:
            command.angular.z += turn_sign * DELTA_Z
        elif radius_current < radius:
            command.angular.z -= turn_sign * DELTA_Z

	if abs(d_total) >= abs(length):
            command.linear.x = 0
            command.angular.z = 0
        
	print theta_next, (x_next, y_next), (x_target, y_target), radius, radius_current, command.angular.z
        pub_command.publish(command)
        rospy.sleep(SLEEP)
    
    pub_command.publish(zero())
