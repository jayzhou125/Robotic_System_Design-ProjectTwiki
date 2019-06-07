#!/usr/bin/python

import rospy
import key_handler
from std_msgs.msg import Int32, Float32
from threading import Thread

handler = Thread(target=key_handler.keypress)

def key_node():
    global handler
    rospy.init_node("key_node")
    rospy.on_shutdown(cleanUp)
    pub_keys = rospy.Publisher("/keys", Int32, queue_size=20)
    pub_dx = rospy.Publisher("/dx", Float32, queue_size=10)
    pub_dz = rospy.Publisher("/dz", Float32, queue_size=10)

    DELTA_X = 0.0
    DELTA_Z = 0.0

    pub_dx.publish(DELTA_X)
    pub_dz.publish(DELTA_Z)

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
    key_node()