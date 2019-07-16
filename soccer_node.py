#!/usr/bin/python

import rospy
import location
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from batch_controller import execute, cancel
from lines import Line
from math import sqrt
from soccer_scan import scan, stop

pub_command = rospy.Publisher("/kobuki_command", Twist, queue_size=10)
pub_stop = rospy.Publisher("/emergency_stop", Empty, queue_size=10)

TARGET_OFFSET = None

def soccer():
    global pub_command, pub_stop, TARGET_OFFSET
    rospy.init_node("soccer_node")
    location.init()
    rospy.on_shutdown(cleanUp)

    file = open("soccer.log", "w")

    print "Connecting..."
    while pub_command.get_num_connections() == 0:
        pass
    
    x = 0
    y = 0
    theta = 0
    true_angle = 0

    file.write("{} {}\n".format(x, y))
    print ["start", x, y]

    # scan from current position for ball and goal
    ball_angle_1, goal_angle_1 = scan(pub_command)

    execute(0, 1, 0.2, reset=False)

    rospy.sleep(1)

    # turn to face 45 degrees past ball away from goal
    if ball_angle_1 < 0:
        ball_angle_1 += 360
    if goal_angle_1 < 0:
        goal_angle_1 += 360

    direction = 1

    delta = goal_angle_1 - ball_angle_1
    if delta < -180 or (delta > 0 and delta < 180):
        direction = -1
        

    target_angle = ball_angle_1 + direction*45




    print "--- SCAN 1 RESULTS ---"
    print "x: {} y: {},  goal @ {}, ball @ {}".format(x, y, goal_angle_1, ball_angle_1)
    goal_vector_1 = Line(x=x, y=y, theta=goal_angle_1, useDegrees=True)
    ball_vector_1 = Line(x=x, y=y, theta=ball_angle_1, useDegrees=True)
    

    _, _, theta = location.currentLocation

    if theta < 0:
	theta += 360

    move_angle = target_angle - theta
    
    execute(0, move_angle, 0.6)
    rospy.sleep(1)

    # move to new location
    move_dist = 0.2
    execute(move_dist, 0, 0.5)


    print "--- REALIGNING FOR SCAN 2 ---"
    print "odom @ {}, angle from scan 1 start @ {}".format(location.currentLocation[2], target_angle)

    true_angle = target_angle

    scan_2_vector = Line(x=0, y=0, theta=true_angle, useDegrees=True)
    x, y = scan_2_vector.findPointFrom(0, 0, move_dist)
    

    file.write("{} {}\n".format(x, y))

    print ["scan_2", x, y]

    # get new position
    _, _, theta = location.currentLocation

    theta += true_angle

    # scan from current position for ball and goal
    ball_angle_2, goal_angle_2 = scan(pub_command)
    ball_angle_2 += true_angle
    goal_angle_2 += true_angle

    goal_vector_2 = Line(x=x, y=y, theta=goal_angle_2, useDegrees=True)
    ball_vector_2 = Line(x=x, y=y, theta=ball_angle_2, useDegrees=True)

    # calculate intersections
    goal_x, goal_y = goal_vector_1.intersect(goal_vector_2)
    ball_x, ball_y = ball_vector_1.intersect(ball_vector_2)

    print "--- SCAN 2 RESULTS ---"
    print "x: {}, y: {},  goal @ {}, ball @ {}".format(x, y, goal_angle_2, ball_angle_2)
    print "--- GOAL LOCATION ---"
    print "x: {}, y: {}".format(goal_x, goal_y)
    print "--- BALL LOCATION ---"
    print "x: {}, y: {}".format(ball_x, ball_y)


    file.write("{} {}\n".format(ball_x, ball_y))
    file.write("{} {}\n".format(goal_x, goal_y))

    print ["ball", ball_x, ball_y]
    print ["goal", goal_x, goal_y]

    # find line from ball to goal
    approach_vector = Line(x1=goal_x, y1=goal_y, x2=ball_x, y2=ball_y)


    TARGET_OFFSET = 0.5
    # select point on approach vector for robot to start
    target_x, target_y = approach_vector.findPointFrom(ball_x, ball_y, TARGET_OFFSET)
    alt_x = ball_x * 2 - target_x
    alt_y = ball_y * 2 - target_y


    file.write("{} {}\n".format(target_x, target_y))
    print ["kick", target_x, target_y]
    
    file.write("{} {}\n".format(alt_x, alt_y))
    print["kick_alt", alt_x, alt_y]

    d_ball_target = distance(ball_x, ball_y, target_x, target_y)
    d_ball_goal = distance(ball_x, ball_y, goal_x, goal_y)
    d_goal_target = distance(goal_x, goal_y, target_x, target_y)
    d_goal_alt = distance(goal_x, goal_y, alt_x, alt_y)
    
    if d_goal_alt > d_goal_target:
        print "--- ALT SELECTED ---"
        target_x = alt_x
        target_y = alt_y
    else:
        print "--- FIRST TARGET SELECTED ---"

    print "x: {}, y: {}".format(target_x, target_y)


    # find way to move from current position to target pt
    dist = distance(x, y, target_x, target_y)
    movement_vector = Line(x=x, y=y, x2=target_x, y2=target_y)
    angle = movement_vector.angle(useDegrees=True)

    tx, ty = movement_vector.findPointFrom(x, y, dist)

    if abs(tx - target_x) > 0.0001 or abs(ty - target_y) > 0.0001:
        print "--- USING ALTERNATE ANGLE ---"
        angle += 180

    print "--- APPROACHING SHOT LOCATION ---"
    print "angle to shot location @ {}".format(angle)

    _, _, theta = location.currentLocation
    theta += true_angle
    execute(0, angle - theta, 0.6, reset=True)
    execute(dist, 0, 0.6, reset=True)

    print "--- REALIGNING FOR SHOT ---"
    print "odom @ {}, angle from scan 2 start @ {}, angle from scan 1 start @ {}".format(location.currentLocation[2], angle, angle + true_angle)


    # scan for ball(and goal)
    ball_angle_fin, goal_angle_fin = scan(pub_command)

    # create background thread to stop robot once ball is hit
    from threading import Thread

    stop_thread = Thread(target=stopper)
    stop_thread.start()

    # make the shot
    execute(TARGET_OFFSET + 2,  0, 1, reset=True)
    
    stop_thread.join()
    file.close()


def distance(x1, y1, x2, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

    
def stopper():
    global pub_stop, TARGET_OFFSET
    while(location.currentLocation[0] < TARGET_OFFSET + 0.1):
        rospy.sleep(0.001)
    pub_stop.publish(Empty())



def cleanUp():
    global pub_stop
    stop = True
    pub_stop.publish(Empty())


if __name__ == "__main__":
    soccer()
