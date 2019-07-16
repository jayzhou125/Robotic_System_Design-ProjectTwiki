#!/usr/bin/python

import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from cmvision.msg import Blobs, Blob
from sensor_msgs.msg import Image
import location
import pid

pub_command = rospy.Publisher("/kobuki_command", Twist, queue_size=10)  # publish command
pub_stop = rospy.Publisher("/emergency_stop", Empty, queue_size=10)     # publish stop

# initialization
rawBlobs = Blobs()
mergedBlobs = {}
width = 0

def init():
    rospy.init_node("tracking_line")     # initialize the node
    location.init()                      # init the location
    rospy.on_shutdown(cleanUp)          
    rospy.Subscriber("/blobs", Blobs, setRawBlobs)  # subscribe to blobs

def track_blobs():
    global rawBlobs, pub_command

    Z_MAX = 0.4  # maximum speed

    zero_count = 0

    while(True):
        command = zero()
        command.linear.x = 0.35 # update values; .7 = too fast
        mergedBlobs = mergeBlobs()
        trackingBlob = None

       # print mergedBlobs.keys()

        if "greenline" in mergedBlobs.keys() and len(mergedBlobs["greenline"]) > 0:
            trackingBlob = mergedBlobs["greenline"][0]
                        
        if trackingBlob is None:
            if zero_count < 1000:
                zero_count += 1
            else:
                print "no line"
                pub_command.publish(zero())
            continue
        
        zero_count = 0


        # pid error (Proportional-Integral-Derivative (PID) Controller)
        p = 0.009 # update values
        i = 0 # can leave this as zero
        d = 0 # update values; .5 = crazy turn
        controller = pid.PID(p, i, d)
        controller.start()
        
        center = rawBlobs.image_width//2    # the center of the image
        centerOffset = center - trackingBlob.x  # the offset that the ball need to travel 
        
        cor = controller.correction(centerOffset) # added, right angular speed you want
        
	print cor

        # print "Tracking Blob Object Attr: ", trackingBlob.name, "<<" # added AS
        
        command.angular.z = cor
        
        # if centerOffset > 20:   # if the offset is bigger than 20
            # command.angular.z = corr
            # print([command.angular.z, centerOffset/rawBlobs.image_width])
        # elif centerOffset < -20:    # if the offset is smaller than -20
            # command.angular.z = corr
            # command.angular.z = max(-Z_MAX, speed)  # turn right and follow the ball
            # print([command.angular.z, centerOffset/rawBlobs.image_width])
        
        pub_command.publish(command)    # publish the twist command to the kuboki node

	rospy.sleep(0.001)
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

