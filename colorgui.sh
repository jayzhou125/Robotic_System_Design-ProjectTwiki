#!/bin/bash

gnome-terminal --tab --title="roscore" -e "bash -c 'roscore'"

sleep 2s

gnome-terminal --tab --title="gscam_launch" -e "bash -c 'roslaunch gscam v4l.launch'"

sleep 2s

gnome-terminal --tab --title="blob_tracker" -e "bash -c 'rosrun cmvision colorgui image:=/v4l/camera/image_raw';bash"
