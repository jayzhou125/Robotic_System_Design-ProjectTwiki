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
mergedBlobs = {}
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
        mergedBlobs = mergeBlobs()
        trackingBlob = None

        print mergedBlobs.keys()

        if "blueball" in mergedBlobs.keys():
            trackingBlob = mergedBlobs["blueball"][0]
        elif "pinkgoal" in mergedBlobs.keys() and "yellowgoal" in mergedBlobs.keys():
            for outer in mergedBlobs["yellowgoal"]:
                for inner in mergedBlobs["pinkgoal"]:
                    if (inner.left >= outer.left
                    and inner.right <= outer.right
                    and inner.top >= outer.top
                    and inner.bottom <= outer.bottom):
                        trackingBlob = inner
                        break
                
                if trackingBlob is not None:
                    break
                        
        if trackingBlob is None:
            continue

        center = rawBlobs.image_width//2    # the center of the image
        centerOffset = center - trackingBlob.x  # the offset that the ball need to travel 
        
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

# def mergeBlobs():
#     # try out the area param simple detection
#     global rawBlobs
#     result = Blob()

#     params = cv2.SimpleBlobDetector_Params()
# 	# params.minThreshold = 0
# 	# params.maxThreshold = 255
# 	# params.filterByArea = True
#     params.minArea = 0.01 * rawBlobs.image_width * rawBlobs.image_height # tenth of the image size
#     params.maxArea = rawBlobs.image_width * rawBlobs.image_height
# 	# params.filterByCircularity = True
# 	# params.minCircularity = 0.1
# 	# params.filterByConvexity = False
# 	# params.minConvexity = 0.9
# 	# params.filterByInertia = False
# 	# params.minInertiaRatio = 0.5
#     ver = (cv2.__version__).split('.')
#     if int(ver[0]) < 3:
#         result = cv2.SimpleBlobDetector(params)
#     else:
#     	result = cv2.SimpleBlobDetector_create(params)

#     return result

def mergeBlobs():
    global rawBlobs

    merged = {}

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
    
    return merged


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
            

#     global rawBlobs
#     x = 0;
#     y = 0;
#     left = 0;
#     right = 0;
#     top = 0;
#     bottom = 0;
#     area = 0;
#     name = ""; # added AS
#     for b in rawBlobs.blobs:
#         x = x + (b.x * b.area)
#         y = y + (b.y * b.area)
#         left = left + (b.left * b.area)
#         right = right + (b.right * b.area)
#         top = top + (b.top * b.area)
#         bottom = bottom + (b.bottom * b.area)
#         area = area + b.area
# 	name = b.name # added AS
#     result = Blob()

#     if area > 0:
#         result.x = x / area
#         result.y = y / area
#         result.left = left / area
#         result.right = right / area
#         result.top = top / area
#         result.bottom = bottom / area
#         result.area = x * y
# 	result.name = name # added AS; what gets assigned to trackingBlob

#     # print "blob merged center is + (", x, ", ", y, ")"
#     return result

def cleanUp():
    pub_stop.publish(Empty())

if __name__ == "__main__":
    init()
    track_blobs()
