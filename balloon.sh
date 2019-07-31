#!/bin/bash

gnome-terminal --tab --title="roscore" -e "bash -c 'roscore'"

sleep 2s

gnome-terminal --tab --title="kobuki" -e "bash -c 'roslaunch kobuki_node minimal.launch'"

gnome-terminal --tab --title="kinect_aux" -e "bash -c 'rosrun kinect_aux kinect_aux_node'"

gnome-terminal --tab --title="kinect_data" -e "bash -c 'roslaunch openni_launch openni.launch'"

gnome-terminal --tab --title="balloon_vision" -e "bash -c 'roslaunch mypackage balloon_vision.launch'"

gnome-terminal --tab --title="constant_command" -e "bash -c 'rosrun mypackage constant_command.py -r'"

sleep 5s

rosrun mypackage balloon_catcher.py "$@"
