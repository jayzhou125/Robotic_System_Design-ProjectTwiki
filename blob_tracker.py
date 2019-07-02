#!/usr/bin/python

import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from cmvision.msg import Blobs, Blob
from sensor_msgs.msg import Image
import location

pub_command = rospy.Publisher("/kobuki_command", Twist, queue_size=10)
pub_stop = rospy.Publisher("/emergency_stop", Empty, queue_size=10)


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

    Z_MAX = 1.0

    while(True):
        command = zero() 
        trackingBlob = mergeBlobs()
        centerOffset = rawBlobs.image_width - trackingBlob.x
        if trackingBlob.x == 0 and trackingBlob.y == 0:
            continue

        elif centerOffset > 0.005 * rawBlobs.image_width:
            command.angular.z = max(-Z_MAX, -0.01 * centerOffset)
            
        elif centerOffset < -0.005 * rawBlobs.image_width:
            command.angular.z = min(Z_MAX, 0.01 * centerOffset)
            
        pub_command.publish(command)
    

def setRawBlobs(blobs):
    global rawBlobs
    rawBlobs = blobs

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
    for b in rawBlobs.blobs:
        x = x + (b.x * b.area)
        y = y + (b.y * b.area)
        left = left + (b.left * b.area)
        right = right + (b.right * b.area)
        top = top + (b.top * b.area)
        bottom = bottom + (b.bottom * b.area)
        area = area + b.area
    result = Blob()

    if area > 0:
        result.x = x / area
        result.y = y / area
        result.left = left / area
        result.right = right / area
        result.top = top / area
        result.bottom = bottom / area
        result.area = x * y

    print "blob merged center is + (", x, ", ", y, ")"
    return result



def cleanUp():
    pub_stop.publish(Empty())

if __name__ == "__main__":
    init()
    track_blobs()
