import rospy
import location
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from batch_controller import execute, cancel
from lines import Line
from math import sqrt

pub_command = rospy.Publisher("/kobuki_command", Twist, queue_size=10)
pub_stop = rospy.Publisher("/emergency_stop", Empty, queue_size=10)

def soccer_node():
    global pub_command, pub_stop
    rospy.init_node("soccer_node")
    location.init()
    rospy.on_shutdown(cleanUp())

    print "Connecting..."
    while pub_command.get_num_connections() == 0:
        pass
    
    x = 0
    y = 0
    theta = 0

    # scan from current position for ball and goal
    goal_angle_1 = 0
    ball_angle_1 = 0

    goal_vector_1 = Line(x=x, y=y, theta=goal_angle_1, useDegrees=True)
    ball_vector_1 = Line(x=x, y=y, theta=ball_angle_1, useDegrees=True)


    # decide where to move next

    # move to new location
    move_dist = 0.5
    execute(0.5, 0, 0.5, reset=False)

    # get new position
    x, y, theta = location.currentLocation

    # scan from current position for ball and goal
    goal_angle_2 = 0
    ball_angle_2 = 0

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


    # make the shot
    execute(TARGET_OFFSET + 0.2,  0, 0.6, reset=True)

def distance(x1, y1, x2, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)



def cleanUp():
    global pub_stop
    pub_stop.publish(Empty())