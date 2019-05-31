#!/bin/bash

rosparam set joy_node/dev "/dev/input/js1"
rosrun joy joy_node
