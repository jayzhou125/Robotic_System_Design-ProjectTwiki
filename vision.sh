#!/bin/bash

gnome-terminal --tab --title="roscore" -e "bash -c 'roscore'"

sleep 2s

gnome-terminal --tab --title="kobuki" -e "bash -c 'roslaunch kobuki_node minimal.launch'"

gnome-terminal --tab --title="gscam_launch" -e "bash -c 'roslaunch gscam v4l.launch'"

gnome-terminal --tab --title="cmvision_launch" -e "bash -c 'roslaunch mypackage soccer_vision.launch'"

gnome-terminal --tab --title="blob_tracker" -e "bash -c 'rosrun mypackage blob_tracker.py';bash"

gnome-terminal --tab --title="constant_command" -e "bash -c 'rosrun mypackage constant_command.py'"
