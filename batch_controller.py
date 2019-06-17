import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import location
import math

SLEEP = 0.01
DELTA_X = 0.8*SLEEP 	# was 0.5
DELTA_Z = 1.3*SLEEP	# was 1
command = None
cancel = False


def stop(data):
    global cancel
    cancel = True

def start(data):
    global cancel
    cancel = False

def terminate(data):
    global cancel
    cancel = True

# not moving?
def zero():
    t = Twist()
    t.angular.z = 0
    t.linear.x = 0
    return t

pub_command = rospy.Publisher("/kobuki_command", Twist, queue_size=25)   # publish the command 
emergency_stop = rospy.Subscriber("/emergency_stop", Empty, stop)
resume = rospy.Subscriber("/resume", Empty, start)
kill = rospy.Subscriber("/kill", Empty, terminate)


# execite the commands base of the speeds and commands given
def execute(linear, angular, speed):
    location.resetOdom()
    rospy.sleep(0.1)


    if(angular == 0):	# forward/back
        _line(linear, speed)
    elif(linear == 0):	# turn
        _turn(angular, speed)
    else:		# else it is an arc command
        _arc(linear, angular, speed)

# forward and back in a certain distance
def _line(distance, speed):
    global SLEEP, DELTA_X, command, pub_command, cancel

    # determine the direction
    if distance < 0:	
	sign = -1	# back 
    else:
        sign = 1	# forward

    command = Twist()
    command.angular.z = 0
    command.linear.x = 0.05 * sign

    while command.linear.x != 0 and not cancel:
        print cancel
        x, y, theta = location.currentLocation
        cutoff = distance - (sign * (command.linear.x*2) ** 2) # temporary cutoff calculation
        if x >= cutoff and sign > 0: 	 	# if travelled to the cutoff point
            command.linear.x -= DELTA_X 	# started to decrease the speed slowly
	elif x <= cutoff and sign < 0:		# if not reached the cutoff point
            command.linear.x += DELTA_X		# increase the speed slowly
	
	# speed smoother
        elif command.linear.x < speed and command.linear.x > 0 and sign > 0:	
            command.linear.x = min(command.linear.x + DELTA_X, speed)
        elif command.linear.x > -speed and command.linear.x < 0 and sign < 0:
            command.linear.x = max(command.linear.x - DELTA_X, -speed)

	if abs(x) >= abs(distance):		# if reach the distance specified, stop 
            command.linear.x = 0
        
        if (command.linear.x < 0 and sign > 0) or (command.linear.x < 0 and sign > 0):
            command.linear.x = 0

	print x, cutoff, command.linear.x	# print check
	command.angular.z = 0			# make sure it is not turning 
        pub_command.publish(command)		# publish the command
        rospy.sleep(SLEEP)			
    
    pub_command.publish(zero())			# stop the robot
    

def _turn(degrees, speed):
    global SLEEP, DELTA_Z, command, pub_command, cancel

    # determine the direction
    if degrees < 0:
	sign = -1 	# right turn
    else:	
        sign = 1	# left turn

    # initialization
    command = Twist()
    command.linear.x = 0
    command.angular.z = 0.1 * sign
    
    loops = 0
    theta_prev = 0
    theta_total = 0

    while command.angular.z != 0 and not cancel:
        x, y, theta = location.currentLocation
        cutoff = degrees - (sign * (command.angular.z*5.5) ** 2) 	# temporary cutoff calculation

	# for turns bigger than 180 degree
	if ((theta < 0 and theta_prev > 0 and sign > 0)			# loop over from 180 to -180 during positive rotation
        or (theta > 0 and theta_prev < 0 and sign < 0)):		# loop over from -180 to 180 during negative rotation
            loops += 1
        
        theta_total = theta + (sign * 360 * loops)

	# smoother
        if theta_total >= cutoff and theta_prev != theta and sign > 0:
            command.angular.z -= DELTA_Z
	elif theta_total <= cutoff and theta_prev != theta and sign < 0:
            command.angular.z += DELTA_Z

        elif command.angular.z < speed and command.angular.z > 0 and sign > 0:
            command.angular.z = min(command.angular.z + DELTA_Z, speed)
        elif command.angular.z > -speed and command.angular.z < 0 and sign < 0:
            command.angular.z = max(command.angular.z - DELTA_Z, -speed)



        theta_prev = theta

	if abs(theta_total) >= abs(degrees):				# if degrees match the specified 
            command.angular.z = 0					# stop

        if (command.angular.z < 0 and sign > 0) or (command.angular.z < 0 and sign > 0):	
            command.angular.z = 0
        
	print theta, theta_total, cutoff, command.angular.z		# print to check the data
	command.linear.x = 0						# make sure the
        pub_command.publish(command)
        rospy.sleep(SLEEP)
    
    pub_command.publish(zero())
    


def _arc(length, radius, speed):
    global SLEEP, DELTA_X, command, pub_command, cancel
    radians = (length / radius)
    degrees = radians  * 180/math.pi


    # IF THIS DOESN'T WORK, ATTEMPT TO IMPLEMENT THE ALGORITHM DESCRIBED IN https://hal.archives-ouvertes.fr/hal-02014895/document
    # The equations of interest are:
    # v = Kp * p cos a
    # w = Kp * cos a * sin a + K * a * a
    # where:
    # a is the difference between current z angle and waypoint z angle
    # p is distance to waypoint position
    # Kp is a constant for smoothing
    # K is a constant for error correction
    


    if length < 0:
	sign = -1
    else:
        sign = 1

    if radius < 0:
        turn_sign = -sign
    else:
        turn_sign = sign

    command = Twist()

    command.linear.x = sign*0.05

    loops = 0
    theta_prev = 0
    theta_total = 0
    
    print sign, turn_sign
    while command.linear.x != 0 and not cancel:
        x, y, theta = location.currentLocation
        
        cutoff = degrees - (turn_sign * (command.angular.z*7) ** 2) # temporary cutoff calculation

        if ((theta < -1 and theta_prev > 1 and turn_sign > 0)	# loop over from 180 to -180 during positive rotation
        or (theta > 1 and theta_prev < -1 and turn_sign < 0)):	# loop over from -180 to 180 during negative rotation
            loops += 1
        
        theta_prev = theta
        theta_total = theta + (turn_sign * 360 * loops)


        if ((theta_total >= cutoff and turn_sign > 0)
	or (theta_total <= cutoff and turn_sign < 0)):
            command.linear.x -= DELTA_X * sign

        elif command.linear.x < speed and command.linear.x > 0 and sign > 0:
            command.linear.x = min(command.linear.x + DELTA_X, speed)
        elif command.linear.x > -speed and command.linear.x < 0 and sign < 0:
            command.linear.x = max(command.linear.x - DELTA_X, -speed)

        command.angular.z = location.currentVelocity/radius * 1.3

        if abs(theta_total) >= abs(degrees):
            command = zero()

        if (command.linear.x < 0 and sign > 0) or (command.linear.x < 0 and sign > 0):
            command.linear.x = 0

        pub_command.publish(command)
        print theta_total, command.linear.x, command.angular.z	
        rospy.sleep(SLEEP)
    
    pub_command.publish(zero())


