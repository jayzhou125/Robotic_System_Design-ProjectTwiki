# initialization
rawBlobs = Blobs()
mergedBlobs = Blobs()
width = 0
ballNotFound = True
goalNotFound = True

def init():
    rospy.init_node("blob_tracker")     # initialize the node
    location.init()                     # init the location
    rospy.on_shutdown(cleanUp)          
    rospy.Subscriber("/blobs", Blobs, setRawBlobs)  # subscribe to blobs

def turn_left(speed)
    command.angular.z = speed
    pub_command.publish(command)    # publish the twist command to the kuboki node

# stop the robot
def zero():
    result = Twist();
    result.angular.z = 0
    result.linear.x = 0

    return result

# keep turning left until the ball and the goal is find
def scan():
    global rawBlobs, pub_command
    global ball_x, ball_y, ball_angle, goal_x, goal_y, goal_angle, ballNotFound, goalNotFound
    ballNotFound = True
    goalNotFound = True
    
    Z_MAX = 0.3 # speed

    # if the ball not found yet
    while ballNotFound:
        if "blueball" not in merge.keys():
            turn_left(Z_MAX)
        else 
            ballNotFound = track_blobs()
            if ballNotFound == False:
                break
    
    while goalNotFoundZ:
        if "yellowgoal" not in merge.keys():

#     keep_turning(Z_MAX)

    return ball_angle, goal_angle

# track the bolb
def track_blobs():
    global rawBlobs, pub_command, ballNotFound, goalNotFound

    Z_MAX = 0.5  # maximum speed

#     while(True):
    command = zero() 
    trackingBlob = mergeBlobs()  # get the bolb to follow
    center = rawBlobs.image_width//2    # the center of the image
    centerOffset = center - trackingBlob.x  # the offset that the robot need to travel 
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
    else centerOffset == 0:
        ballNotFound = False
        command = zero()
        # stop the robot
        pub_command.publish(command)    # publish the twist command to the kuboki nod
        
    pub_command.publish(command)    # publish the twist command to the kuboki node
        
    return ballNotFound

def record_ball_location()
    global pub_command, ballNotFound, ball_x, ball_y, ball_angle
    command = zero()
    ballNotFound = False
    
    # record odom
    ball_x, ball_y, ball_angle = location.currentLocation
    
    
    
    return ball_angle

# merge bolbs
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

#             # record odom
#             ball_x, ball_y, ball_angle = location.currentLocation
#             # ball is now found, set to False
#             ballNotFound = False
#             command = zero()
#             print "blueball found"
#         if trackingBlob.name == "greenline":
#             # record odom
#             goal_x, goal_y, goal_angle = location.currentLocation
#             # goal is now found, set to False
#             goalNotFound = False
#             command = zero()
#             print "yellogoal found, area"

        # # find_ball()
        # # find_goal()
        # # turn left
        # command = zero() 
        # # trackingBlob = mergeBlobs()  # get the bolb to follow
        # center = rawBlobs.image_width//2    # the center of the image
        # centerOffset = center - trackingBlob.x  # the offset that the ball need to travel 
        # if trackingBlob.x == 0 and trackingBlob.y == 0:     # no bolb is found
        #     continue

        # speed = 4 * centerOffset/float(rawBlobs.image_width)    # calculate the right amount of speed for the command

        # print "Tracking Blob Object Attr: ", trackingBlob.name, "<<" # added AS

        # if centerOffset > 20:   # if the offset is bigger than 20
        #     command.angular.z = min(Z_MAX, speed) # turn left and follow 
        #     # print([command.angular.z, centerOffset/rawBlobs.image_width])
        # elif centerOffset < -20:    # if the offset is smaller than -20
        #     command.angular.z = max(-Z_MAX, speed)  # turn right and follow the ball
        #     # print([command.angular.z, centerOffset/rawBlobs.image_width])

        # pub_command.publish(command)    # publish the twist command to the kuboki node

        # if trackingBlob.name == "blueball" and trackingBlob.area > 1000000000:
        #     # record odom
        #     ball_x, ball_y, ball_angle = location.currentLocation
        #     # ball is now found, set to False
        #     ballNotFound = False
        #     print "blueball found, area", trackingBlob.area
        # if trackingBlob.name == "greenline" and trackingBlob.area > 1000000000:
        #     # record odom
        #     goal_x, goal_y, goal_angle = location.currentLocation
        #     # goal is now found, set to False
        #     goalNotFound = False
        #     print "yellogoal found, area", trackingBlob.area
        #if not ballNotFound and not goalNotFound:
         #   return ball_x, ball_y, ball_goal, goal_x, goal_y, goal_angle
