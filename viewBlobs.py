#!/usr/bin/env python

import roslib
import rospy
import cv2
import copy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from cmvision.msg import Blobs, Blob

colorImage = Image()
isColorImageReady = False
blobsInfo = Blobs()
isBlobsInfoReady = False

def updateColorImage(data):
    global colorImage, isColorImageReady
    colorImage = data
    isColorImageReady = True

def updateBlobsInfo(data):
    global blobsInfo, isBlobsInfoReady
    blobsInfo = data
    isBlobsInfoReady = True

def main():
    global colorImage, isColorImageReady, blobsInfo, isBlobsInfoReady
    rospy.init_node('showBlobs', anonymous=True)
    rospy.Subscriber("/blobs", Blobs, updateBlobsInfo)
    rospy.Subscriber("/v4l/camera/image_raw", Image, updateColorImage)
    bridge = CvBridge()
    cv2.namedWindow("Blob Location")

    while not rospy.is_shutdown() and (not isBlobsInfoReady or not isColorImageReady):
        pass

    while not rospy.is_shutdown():
        try:
            color_image = bridge.imgmsg_to_cv2(colorImage, "bgr8")
        except CvBridgeError, e:
            print e
            print "colorImage"

        blobsCopy = copy.deepcopy(blobsInfo)

	for b in blobsCopy.blobs:
		cv2.rectangle(color_image, (b.left, b.top), (b.right, b.bottom), (0,255,0), 2)

        cv2.imshow("Color Image", color_image)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
 
if __name__ == '__main__':
    main()
