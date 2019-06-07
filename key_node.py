#!/usr/bin/python

import rospy
import key_handler
from std_msgs.msg import Int32, Float32
from threading import Thread

handler = Thread(target=key_handler.keypress)

def key_node(dx=0, dz=0):
    global handler
    rospy.init_node("key_node")
    rospy.on_shutdown(cleanUp)
    pub_keys = rospy.Publisher("/keys", Int32, queue_size=20)
    pub_dx = rospy.Publisher("/dx", Float32, queue_size=10)
    pub_dz = rospy.Publisher("/dz", Float32, queue_size=10)

    pub_dx.publish(dx)
    pub_dz.publish(dz)

    handler.start() # start keypress handler in background thread

    while True:
        dirty = key_handler.dirty
        code = key_handler.code
        kill = key_handler.kill

        if dirty and code != None:
            pub_keys.publish(code)
            key_handler.dirty = False
        
        elif key_handler.kill == True:
            break

        rospy.sleep(0.05)
    
    handler.join()


def cleanUp():
    global handler
    key_handler.kill = True
    handler.join()


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="takes WASD or arrow key inputs and converts them to robot directions")
    
    parser.add_argument("-x", "--delta-x", type=float, nargs='?', const=0, help="set the linear acceleration constant")
    parser.add_argument("-z", "--delta-z", type=float, nargs='?', const=0, help="set the angular acceleration constant")
    args = parser.parse_args()
    
    dx = args.delta_x
    dz = args.delta_z

    key_node(dx, dz)