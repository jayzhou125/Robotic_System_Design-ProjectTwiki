#!/usr/bin/python

import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from cmvision.msg import Blobs, Blob
from sensor_msgs.msg import Image
import location

pub_command = rospy.Publisher("/kobuki_command", Twist, queue_size=10)  # publish command
pub_stop = rospy.Publisher("/emergency_stop", Empty, queue_size=10)     # publish stop

# initialization
rawBlobs = Blobs()
mergedBlobs = Blobs()
width = 0

def init():
    rospy.init_node("blob_tracker")     # initialize the node
    location.init()                     # init the location
    rospy.on_shutdown(cleanUp)          
    rospy.Subscriber("/blobs", Blobs, setRawBlobs)  # subscribe to blobs

def track_blobs():
    global rawBlobs, pub_command

    Z_MAX = 0.5  # maximum speed

    while(True):
        command = zero() 
        trackingBlob = mergeBlobs()  # get the bolb to follow
        center = rawBlobs.image_width//2    # the center of the image
        centerOffset = center - trackingBlob.x  # the offset that the ball need to travel 
        if trackingBlob.x == 0 and trackingBlob.y == 0:     # no bolb is found
            continue

        speed = 4 * centerOffset/float(rawBlobs.image_width)    # calculate the right amount of speed for the command

        print "Tracking Blob Object Attr: ", trackingBlob.name, "<<" # added AS

        if centerOffset > 20:   # if the offset is bigger than 20
            command.angular.z = min(Z_MAX, speed) # turn left and follow 
            # print([command.angular.z, centerOffset/rawBlobs.image_width])
        elif centerOffset < -20:    # if the offset is smaller than -20
            command.angular.z = max(-Z_MAX, speed)  # turn right and follow the ball
            # print([command.angular.z, centerOffset/rawBlobs.image_width])
        
        pub_command.publish(command)    # publish the twist command to the kuboki node

def setRawBlobs(blobs):
    global rawBlobs
    rawBlobs = blobs

# stop the robot
def zero():
    result = Twist();
    result.angular.z = 0
    result.linear.x = 0

    return result

def mergeBlobs():
    global rawBlobs
    x = 0;
    y = 0;
    left = 0;
    right = 0;
    top = 0;
    bottom = 0;
    area = 0;
    name = ""; # added AS
    for b in rawBlobs.blobs:
        x = x + (b.x * b.area)
        y = y + (b.y * b.area)
        left = left + (b.left * b.area)
        right = right + (b.right * b.area)
        top = top + (b.top * b.area)
        bottom = bottom + (b.bottom * b.area)
        area = area + b.area
	name = b.name # added AS
    result = Blob()

    if area > 0:
        result.x = x / area
        result.y = y / area
        result.left = left / area
        result.right = right / area
        result.top = top / area
        result.bottom = bottom / area
        result.area = x * y
	result.name = name # added AS; what gets assigned to trackingBlob

    # print "blob merged center is + (", x, ", ", y, ")"
    return result

def cleanUp():
    pub_stop.publish(Empty())

if __name__ == "__main__":
    init()
    track_blobs()
