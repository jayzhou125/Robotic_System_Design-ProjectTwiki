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

def soccer():
    global pub_command, pub_stop
    rospy.init_node("soccer_node")
    location.init()
    rospy.on_shutdown(cleanUp)

    print "Connecting..."
    while pub_command.get_num_connections() == 0:
        pass
    
    x = 0
    y = 0
    theta = 0


    # scan from current position for ball and goal
    ball_angle_1, goal_angle_1 = scan(pub_command)

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


    print [ball_angle_1, goal_angle_1, target_angle]


    print [x, y, goal_angle_1]
    goal_vector_1 = Line(x=x, y=y, theta=goal_angle_1, useDegrees=True)
    ball_vector_1 = Line(x=x, y=y, theta=ball_angle_1, useDegrees=True)
    

    x, y, theta = location.currentLocation

    if theta < 0:
	theta += 360

    move_angle = target_angle - theta
    execute(0, move_angle, 0.6, reset=False)

    # move to new location
    move_dist = 0.2
    execute(move_dist, 0, 0.5, reset=False)

    # get new position
    x, y, theta = location.currentLocation

    # scan from current position for ball and goal
    ball_angle_2, goal_angle_2 = scan(pub_command)

    goal_vector_2 = Line(x=x, y=y, theta=goal_angle_2, useDegrees=True)
    ball_vector_2 = Line(x=x, y=y, theta=ball_angle_2, useDegrees=True)

    # calculate intersections
    goal_x, goal_y = goal_vector_1.intersect(goal_vector_2)
    ball_x, ball_y = ball_vector_1.intersect(ball_vector_2)

    # find line for hitting the ball
    approach_vector = Line(x1=goal_x, y1=goal_y, x2=ball_x, y2=ball_y)


    TARGET_OFFSET = 0.5
    # select point on approach vector for robot to start
    target_x, target_y = approach_vector.findPointFrom(ball_x, ball_y, TARGET_OFFSET)

    d_ball_target = distance(ball_x, ball_y, target_x, target_y)
    d_ball_goal = distance(ball_x, ball_y, goal_x, goal_y)
    d_goal_target = distance(goal_x, goal_y, target_x, target_y)

    # if target pt is closer to goal than to ball or target is between goal and ball:
    if d_goal_target < d_ball_target or d_goal_target < d_goal_ball:
        target_x, target_y = approach_vector.findPointFrom(ball_x, ball_y, TARGET_OFFSET)

    # find way to move from current position to target pt
    dist = distance(x, y, target_x, target_y)
    movement_vector = Line(x=x, y=y, x2=target_x, y2=target_y)
    angle = movement_vector.angle(useDegrees=True)

    # assumes theta == 0 after scan
    execute(0, angle, 0.6, reset=False)
    execute(dist, 0, 0.6, reset=False)


    # scan for ball(and goal)
    ball_angle_fin, goal_angle_fin = scan(pub_command)

    # make the shot
    execute(TARGET_OFFSET + 0.2,  0, 0.6, reset=True)

def distance(x1, y1, x2, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)



def cleanUp():
    global pub_stop
    stop = True
    pub_stop.publish(Empty())


if __name__ == "__main__":
    soccer()
