#!/usr/bin/env python

import rospy
from cmvision.msg import Blobs, Blob

mergedBlobs = Blobs()
colors = []

def blobsCallback(data):
	b = Blob()
	x = 0
	y = 0
	area = 0
	if data.blob_count > 0:
		for box in data.blobs:
			area = area + box.area
			x = x + (box.x * box.area)
			y = y + (box.y * box.area)
		x = x / area
		y = y / area
	print "(%i,%i)" % (x, y)

def detect_blob():
	rospy.init_node('blob_tracker', anonymous = True)
	rospy.Subscriber('/blobs', Blobs, blobsCallback)
	rospy.spin()

if __name__ == '__main__':
	detect_blob() 
