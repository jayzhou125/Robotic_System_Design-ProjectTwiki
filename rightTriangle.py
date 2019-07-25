#!/usr/bin/python

from math import sin, cos, radians

theta = 0.0
h = 0.0 

'''
class rightTriangle():
    def __init__(self, theta, h):

        self.theta = theta
        self.h = h
        self.alpha = 90 - h
	self.o = sin(radian(theta))* h
	self.a = cos(radian(theta))* h

    def getAdjacent(self):
        return a
'''

def getOpposite(theta, h):
    return sin(radian(theta))* h

def getAdjacent(theta, h):
    return cos(radian(theta))* h

def getAlpha(h):
    return 90 - h
