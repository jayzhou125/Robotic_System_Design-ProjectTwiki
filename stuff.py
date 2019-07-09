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

def track_blobs():
    global rawBlobs, pub_command
    global ball_x, ball_y, ball_goal, goal_x, goal_y, goal_angle, ballNotFound, goalNotFound

    Z_MAX = 0.3 # speed

    while ballNotFound and goalNotFound:
        # turn left
        command = zero() 
        trackingBlob = mergeBlobs()  # get the bolb to follow
        center = rawBlobs.image_width//2    # the center of the image
        centerOffset = center - trackingBlob.x  # the offset that the ball need to travel 
        if trackingBlob.x == 0 and trackingBlob.y == 0:     # no bolb is found
            continue

        speed = 4 * centerOffset/float(rawBlobs.image_width)    # calculate the right amount of speed for the command

        # print "Tracking Blob Object Attr: ", trackingBlob.name, "<<" # added AS

        if centerOffset > 20:   # if the offset is bigger than 20
            command.angular.z = min(Z_MAX, speed) # turn left and follow 
            # print([command.angular.z, centerOffset/rawBlobs.image_width])
        elif centerOffset < -20:    # if the offset is smaller than -20
            command.angular.z = max(-Z_MAX, speed)  # turn right and follow the ball
            # print([command.angular.z, centerOffset/rawBlobs.image_width])

        pub_command.publish(command)    # publish the twist command to the kuboki node

        if trackingBlob.name == "blueball" and trackingBlob.area > 1000000000:
            # record odom
            ball_x, ball_y, ball_angle = location.currentLocation
            # ball is now found, set to False
            ballNotFound = False
            print "blueball found, area", trackingBlob.area
        if trackingBlob.name == "greenline" and trackingBlob.area > 1000000000:
            # record odom
            goal_x, goal_y, goal_angle = location.currentLocation
            # goal is now found, set to False
            goalNotFound = False
            print "yellogoal found, area", trackingBlob.area
        #if not ballNotFound and not goalNotFound:
         #   return ball_x, ball_y, ball_goal, goal_x, goal_y, goal_angle