#!/usr/bin/env python
import roslib
#roslib.load_manifest('rosopencv')
import sys
import rospy
import cv2
import math
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

depthImage = Image()
isDepthImageReady = False;
colorImage = Image()
isColorImageReady = False;
xLocation = 320
yLocation = 240

def mouseClick(event, x, y, flags, param):
    global xLocation, yLocation
    if event == cv2.EVENT_LBUTTONDOWN:
        xLocation = x
        yLocation = y

def updateDepthImage(data):
    global depthImage, isDepthImageReady
    depthImage = data
    isDepthImageReady = True

def updateColorImage(data):
    global colorImage, isColorImageReady
    colorImage = data
    isColorImageReady = True

def main():
    global depthImage, isDepthImageReady, colorImage, isColorImageReady, xLocation, yLocation
    rospy.init_node('image_converter', anonymous=True)
    rospy.Subscriber("/camera/depth/image", Image, updateDepthImage, queue_size=10)
    rospy.Subscriber("/camera/rgb/image_color", Image, updateColorImage, queue_size=10)
    bridge = CvBridge()
    cv2.namedWindow("Color Image")
    cv2.setMouseCallback("Color Image", mouseClick)

    while not isDepthImageReady or not isColorImageReady:
        pass

    while not rospy.is_shutdown():
        try:
            depth = bridge.imgmsg_to_cv2(depthImage, desired_encoding="passthrough")
        except CvBridgeError, e:
            print e
            print "depthImage"

        try:
            color_image = bridge.imgmsg_to_cv2(colorImage, "bgr8")
        except CvBridgeError, e:
            print e
            print "colorImage"
        
        depthValue = depth.item(yLocation,xLocation,0)

        #print "Depth at (%i,%i) is %f." % (xLocation,yLocation,depthValue)

        depthStr = "%.2f" % depthValue

        cv2.rectangle(color_image, (xLocation-10,yLocation-10), (xLocation+10,yLocation+10), (0,255,0), 2)
        cv2.putText(color_image, depthStr, (xLocation+15,yLocation+10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        cv2.imshow("Color Image", color_image)
        cv2.waitKey(1)

    cv2.destroyAllWindows()


 
if __name__ == '__main__':
    main()
