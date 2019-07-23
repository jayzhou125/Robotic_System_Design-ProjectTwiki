#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from struct import *

depthData = Image();
isDepthReady = False;

def depthCallback(data):
    global depthData, isDepthReady
    depthData = data
    isDepthReady = True

def main():
    global depthData, isDepthReady
    rospy.init_node('depth_example', anonymous=True)
    rospy.Subscriber("/camera/depth/image", Image, depthCallback, queue_size=10)

    while not isDepthReady:
        pass

    while not rospy.is_shutdown():
        step = depthData.step
        midX = 320
        midY = 240
        offset = (240 * step) + (320 * 4)
        (dist,) = unpack('f', depthData.data[offset] + depthData.data[offset+1] + depthData.data[offset+2] + depthData.data[offset+3])
        print "Distance: %f" % dist

if __name__ == '__main__':
    main()
