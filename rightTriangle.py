#!/usr/bin/python

from math import sin, cos, radians

class rightTriangle():
    def __init__(self, theta, h):

        self.theta = theta
        self.h = h
        self.alpha = 90 - h
		self.o = sin(radian(theta))* h
		self.a = cos(radian(theta))* h

    def getAdjacent(self):
        return a
