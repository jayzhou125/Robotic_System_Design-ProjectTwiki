#!/usr/bin/python

import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from cmvision.msg import Blobs, Blob
from sensor_msgs.msg import Image
import location
import pid

rawBlobs = Blobs()
mergedBlobs = {}
width = 0
pub_command = None

stop = False

def setRawBlobs(blobs):
    global rawBlobs
    rawBlobs = blobs
          
rospy.Subscriber("/blobs", Blobs, setRawBlobs)  # subscribe to blobs

# stop the robot
def zero():
    result = Twist();
    result.angular.z = 0
    result.linear.x = 0

    return result


def turn_left(speed):
    global pub_command
    command = zero()
    command.angular.z = speed
    pub_command.publish(command)    # publish the twist command to the kuboki node


# keep turning left until the balloon is found
def scan(publisher):
    global rawBlobs, pub_command
    pub_command = publisher
    
   # turn_left(0.4)
    
    return track_blobs("balloon") # image coordinates for center of the blob

def track_blobs(mode):
    global rawBlobs, pub_command, ballNotFound

    Z_MAX = 0.5  # maximum speed

    while not stop:
       
        command = zero() 
        mergedBlobs = mergeBlobs()
        trackingBlob = None

        # print mergedBlobs.keys()

        if "orangeballoon" in mergedBlobs.keys() and len(mergedBlobs["orangeballoon"]) > 0:
            trackingBlob = mergedBlobs["orangeballoon"][0]
                        
        if trackingBlob is None:
            continue

        center = rawBlobs.image_width//2    # the center of the image
        centerOffset = center - trackingBlob.x  # the offset that the ball need to travel 
        
        speed = 4 * centerOffset/float(rawBlobs.image_width)    # calculate the right amount of speed for the command

        # print "Tracking Blob Object Attr: ", trackingBlob.name, "<<" # added AS

        if centerOffset > 20:   # if the offset is bigger than 20
            # print "{} LEFT".format(mode)
            command.angular.z = min(Z_MAX, speed) # turn left and follow 
            # print([command.angular.z, centerOffset/rawBlobs.image_width])
        elif centerOffset < -20:    # if the offset is smaller than -20
            # print "{} RIGHT".format(mode)
            command.angular.z = max(-Z_MAX, speed)  # turn right and follow the ball
            # print([command.angular.z, centerOffset/rawBlobs.image_width])
        else:
            # print "{} CENTERED".format(mode)
            command = zero()
            # stop the robot
            pub_command.publish(command)    # publish the twist command to the kuboki nod
            return trackingBlob
        
        pub_command.publish(command)    # publish the twist command to the kuboki node
       
def record_location():
    # record odom
    _, _, angle = location.currentLocation
    return angle
    


# merge blobs
def mergeBlobs():
    global rawBlobs

    merged = {}
    MIN_AREA = 40

    for b in rawBlobs.blobs:
        mergeTarget = Blob()
        mergeNeeded = False
        
        #check to see if there is an existing blob to merge with
        if b.name in merged.keys(): 
            for m in merged[b.name]:
                if overlaps(b, m):
                    mergeTarget = m
                    mergeNeeded = True
                    break
        
        else: # no blobs by that name
            merged[b.name] = []
        
        # merge
        if not mergeNeeded:
            merged[b.name].append(b)
        else: # merge needed
            mergeTarget.left = min(mergeTarget.left, b.left)
            mergeTarget.right = max(mergeTarget.right, b.right)
            mergeTarget.top = min(mergeTarget.top, b.top)
            mergeTarget.bottom = max(mergeTarget.bottom, b.bottom)
            mergeTarget.area = (mergeTarget.right - mergeTarget.left) * (mergeTarget.bottom - mergeTarget.top)
    
    for m in merged.keys():
        merged[m].sort(key=lambda x: x.area, reverse=True)
        merged[m][:] = [i for i in merged[m] if i.area > MIN_AREA]
    
    return merged

# find the overlap blob
def overlaps(blob1, blob2):
    h_over = False
    v_over = True
    if (blob1.left > blob2.left and blob2.left < blob2.right
    or  blob1.right > blob2.left and blob1.right < blob2.right
    or  blob2.left > blob1.left and blob2.left < blob1.right
    or  blob2.right > blob1.left and blob2.right < blob1.right):
        h_over = True
    
    if (blob1.top > blob2.top and blob2.top < blob2.bottom
    or  blob1.bottom > blob2.top and blob1.bottom < blob2.bottom
    or  blob2.top > blob1.top and blob2.top < blob1.bottom
    or  blob2.bottom > blob1.top and blob2.bottom < blob1.bottom):
        v_over = True

    return h_over and v_over
