#!/bin/bash

gnome-terminal --tab --title="roscore" -e "bash -c 'roscore'"

sleep 2s

gnome-terminal --tab --title="gscam_launch" -e "bash -c 'roslaunch openni_launch openni.launch'"

sleep 2s

gnome-terminal --tab --title="blob_tracker" -e "bash -c 'rosrun cmvision colorgui image:=/camera/rgb/image_color';bash"
