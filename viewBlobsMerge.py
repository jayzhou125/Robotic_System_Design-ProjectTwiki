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

def mergeBlobs(blobs):
    x = 0;
    y = 0;
    left = 0;
    right = 0;
    top = 0;
    bottom = 0;
    area = 0;
    for b in blobs:
        x = x + (b.x * b.area)
        y = y + (b.y * b.area)
        left = left + (b.left * b.area)
        right = right + (b.right * b.area)
        top = top + (b.top * b.area)
        bottom = bottom + (b.bottom * b.area)
        area = area + b.area
    result = Blob()
    result.x = x / area
    result.y = y / area
    result.left = left / area
    result.right = right / area
    result.top = top / area
    result.bottom = bottom / area
    result.area = x * y
    return result

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

        if len(blobsCopy.blobs) > 0:
            oneBlob = mergeBlobs(blobsCopy.blobs)
            cv2.rectangle(color_image, (oneBlob.left, oneBlob.top), (oneBlob.right, oneBlob.bottom), (0,255,0), 2)

        cv2.imshow("Color Image", color_image)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
 
if __name__ == '__main__':
    main()
