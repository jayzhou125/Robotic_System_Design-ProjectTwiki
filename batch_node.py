#!/usr/bin/python

import sys
import rospy
from std_msgs.msg import String, Float32, Empty
from geometry_msgs.msg import Twist
from command_parser import *
from batch_controller import execute
import location

pub_command = rospy.Publisher("/kobuki_command", Twist, queue_size=10)
pub_dx = rospy.Publisher("/dx", Float32, queue_size=10)                     # publish delta x
pub_dz = rospy.Publisher("/dz", Float32, queue_size=10)                     # publish delta z
pub_kill = rospy.Publisher("/emergency_stop", Empty, queue_size=10)         # publish an emergency stop

def batch_node(f=None, dx=0, dz=0):
    global pub_command
    rospy.init_node("batch_publisher")
    location.init()
    rospy.on_shutdown(cleanUp)

    # wait for all channels to connect
    print "Connecting..."
    while pub_command.get_num_connections() == 0:
        pass

    pub_dx.publish(dx)
    pub_dz.publish(dz)

    if f == None:       # if no command, get command from user's input
        print "LIVE MODE: enter commands or q to quit"  

        command = None  # initialize the command    
        while True:
            command = sys.stdin.readline().strip()  # get the command
            if command == "q":  # if q was the command, quit
                break
            execute(*parse_command(command))    # parse the command and execute the commands
    
    else:
        print str(f)    # print the command as string to see what command is given
        for command in f.readlines():   # get the command or series of commands
            execute(*parse_command(command))    # parse the commands and execite them
    
    cleanUp()   # done and exit

# def publish(command):
#         linear, angular, speed = parse_command(command)
#         command_string = "{0} {1} {2}".format(linear, angular, speed)
#         pub_command.publish(command_string)

def cleanUp():
    pub_kill.publish(Empty())   
    print "Exiting..."



if __name__ == "__main__":
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser(description="takes batches of instructions and converts them to robot directions\n\tsee BATCH_FORMAT.md for more information")
    
    parser.add_argument("-x", "--delta-x", type=float, nargs='?', const=0, help="set the linear acceleration constant")
    parser.add_argument("-z", "--delta-z", type=float, nargs='?', const=0, help="set the angular acceleration constant")
    parser.add_argument("-f", "--file", type=FileType("r"), help="file with batch commands to transmit to the robot")

    args = parser.parse_args()      # get the commands

    dx = args.delta_x
    dz = args.delta_z
    f = args.file
    

    batch_node(f, dx, dz)   # process the commands
