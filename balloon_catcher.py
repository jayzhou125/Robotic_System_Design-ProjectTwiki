#!/usr/bin/env python

import rospy
import location
import pid
from std_msgs.msg import Empty, Float64
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import Sound
from cmvision.msg import Blobs, Blob
from sensor_msgs.msg import Image
from batch_controller import execute, cancel
from rightTriangle import *
from struct import pack, unpack
from balloon_tracking_test import scan, get_blob_offset, rawBlobs
from timeit import default_timer
from math import isnan


pub_command = rospy.Publisher("/kobuki_command", Twist, queue_size=10)  # publish command
pub_stop = rospy.Publisher("/emergency_stop", Empty, queue_size=10)   # publish stop
pub_sound = rospy.Publisher("/mobile_base/commands/sound", Sound, queue_size=2)
kinect_angle = 0.0

depth_map = Image()
depth_available = False
ready = Sound()
ready.value = 0

##THOUGHTS:
# we probably need the pid to keep the balloon in the center of the screen
# We also might need to move quickly to the pid (sharpen the movement)


# get the angle of kinect
def angleCallback(data):
    global kinect_angle
    kinect_angle = data.data

def depthCallback(data):
    global depth_map, depth_available
    depth_map = data
    depth_available = True


def getDepth(x, y):
    global depth_map
    data = depth_map.data
    offset = (depth_map.step * y) + (4 * x)
    
    print "depth map size {}, offset {}:{}".format(len(data), offset, offset+3)
    dist = unpack('f', depth_map.data[offset] + depth_map.data[offset+1] + depth_map.data[offset+2] + depth_map.data[offset+3])
    return dist[0]

def cleanUp():
    global pub_stop
    pub_stop.publish(Empty())
    
# stop the robot
def zero():
    result = Twist();
    result.angular.z = 0
    result.linear.x = 0

    return result

def catcher(turn_first=False, no_wait=False):
    global pub_stop, pub_command, kinect_angle, depth_available

    rospy.init_node("balloon_catcher")
    rospy.Subscriber("/cur_tilt_angle", Float64, angleCallback)
    rospy.Subscriber("/camera/depth/image", Image, depthCallback)
    location.init()
    rospy.on_shutdown(cleanUp)

    while not depth_available:
        rospy.sleep(0.1)

    # get the balloon in the center of the screen(ball_tracker)
    if turn_first:
        targetBlob = scan(pub_command)
    else:
        targetBlob = None
        while targetBlob is None:
            centerOffset, targetBlob = get_blob_offset()

    KINECT_PIXELS_PER_DEGREE = 10
    
    dist = None
    horizontal = 0
    vertical = 0.001
    v_prev = 0.001
    V_THRESHOLD = 0.03 # meters
    last = default_timer()

    pub_sound.publish(ready)
        
    while v_prev - vertical <= V_THRESHOLD:
        print (v_prev, vertical, v_prev - vertical)
        centerOffset, targetBlob = get_blob_offset()
        now = default_timer()
	print("loop time {}".format(now - last))
        last = now
        if centerOffset is None or targetBlob is None:
            continue

        # calculate angle from ground to camera-balloon line
        angle = kinect_angle + ((depth_map.height/2) - targetBlob.y)/KINECT_PIXELS_PER_DEGREE

        # get the distance to the balloon 
        dist = getDepth(targetBlob.x, targetBlob.y)
        
        v_prev = vertical
        if isnan(dist):
            vertical = 0
            horizontal = 1.1
        else:
            vertical = getOpposite(angle, dist)
            horizontal = getAdjacent(angle, dist)
        if no_wait:
            break

    pub_sound.publish(ready)
    print (v_prev, vertical, v_prev - vertical)
    print "balloon falling {} meters from camera".format(dist)
    print "height {} meters, estimated landing point {} meters".format(vertical, horizontal)

    # move the calculated distance 
    # we could use batch command's execute but the trick will be the ball won't be in the center all the time when it falls
    # so we might need to use the tracking blob with a higher sensitivity.

    location.resetOdom()
    command = zero()
    SLEEP = 0.01
    DELTA_X = 0.9 * SLEEP
    Z_MAX = 0.6
    IMAGE_WIDTH = 640
    X_TURN_MAX = 0.7
    while(location.currentLocation[0] < horizontal):
        if command.linear.x < 1:
            command.linear.x += DELTA_X
        if command.linear.x > 1:
            command.linear.x = 1
        
        command.angular.z = 0

        centerOffset, _ = get_blob_offset()
        if centerOffset is None:
            pub_command.publish(command)
            continue
        
        speed = 50 * centerOffset/float(IMAGE_WIDTH)    # calculate the right amount of speed for the command

        
        if centerOffset > 20:   # if the offset is bigger than 20
            # print "{} LEFT".format(abs(centerOffset))
            command.angular.z = min(Z_MAX, speed) # turn left and follow
            # print([command.angular.z, centerOffset/rawBlobs.image_width])
        elif centerOffset < -20:    # if the offset is smaller than -20
            # print "{} RIGHT".format(abs(centerOffset))
            command.angular.z = max(-Z_MAX, speed)  # turn right and follow the ball
            # print([command.angular.z, centerOffset/rawBlobs.image_width])

        if abs(command.angular.z) > 0.2 and command.linear.x > X_TURN_MAX:
            command.linear.x = X_TURN_MAX
            # print "turning"

        pub_command.publish(command)
        # print "x {}, z {}".format(command.linear.x, command.angular.z)
        rospy.sleep(SLEEP)

    command = zero()
    pub_command.publish(command)
    
if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser("Balloon catcher program using Kinect sensor")
    parser.add_argument('-t', '--turn-first', dest='turn_first', action='store_const', const=True, default=False, help="add this flag to do a stationary turn before catching the balloon")
    parser.add_argument('-n', '--no-wait', dest="no_wait", action='store_const', const=True, default=False, help='add this flag to approach the balloon without waiting for it to drop')
    args = parser.parse_args()

    no_wait = args.no_wait
    turn_first = args.turn_first
    catcher(turn_first, no_wait)
