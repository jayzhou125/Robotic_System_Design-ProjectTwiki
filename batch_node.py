#!/usr/bin/python

import sys
import rospy
from std_msgs.msg import String, Float32, Empty
from command_parser import *

pub_command = rospy.Publisher("/batch_command", String, queue_size=25)      # publish the command 
pub_dx = rospy.Publisher("/dx", Float32, queue_size=10)                     # publish delta x
pub_dz = rospy.Publisher("/dz", Float32, queue_size=10)                     # publish delta z
pub_kill = rospy.Publisher("/emergency_stop", Empty, queue_size=10)         # publish an emergency stop

def batch_node(f=None, dx=0, dz=0):
    global pub_command
    rospy.init_node("batch_publisher")
    rospy.on_shutdown(cleanUp)

    # wait for all channels to connect
    while pub_command.get_num_connections() == 0 or pub_dx.get_num_connections() == 0 or pub_dz.get_num_connections() == 0:
        pass

    pub_dx.publish(dx)
    pub_dz.publish(dz)

    if f == None:
        print "LIVE MODE: enter commands or q to quit"

        command = None
        while command != "q":
            command = sys.stdin.readline().strip()
            publish(command)
    
    else:
        print str(f)
        for command in f.readlines():
            publish(command)
    
    cleanUp()

def publish(command):
        linear, angular = parse_command(command)
        command_string = "{0} {1}".format(linear, angular)
        pub_command.publish(command_string)

def cleanUp():
    pub_kill.publish(Empty())
    print "Exiting..."



if __name__ == "__main__":
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser(description="takes batches of instructions and converts them to robot directions\n\tsee BATCH_FORMAT.md for more information")
    
    parser.add_argument("-x", "--delta-x", type=float, nargs='?', const=0, help="set the linear acceleration constant")
    parser.add_argument("-z", "--delta-z", type=float, nargs='?', const=0, help="set the angular acceleration constant")
    parser.add_argument("-f", "--file", type=FileType("r"), help="file with batch commands to transmit to the robot")

    args = parser.parse_args()

    dx = args.delta_x
    dz = args.delta_z
    f = args.file
    

    batch_node(f, dx, dz)
