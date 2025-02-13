#!/bin/bash

gnome-terminal --tab --title="roscore" -e "bash -c 'roscore'"

sleep 2s

gnome-terminal --tab --title="joystick" -e "bash -c './set_joystick.sh'"

gnome-terminal --tab --title="kobuki" -e "bash -c 'roslaunch kobuki_node minimal.launch'"

gnome-terminal --tab --title="remoteCtrl.py" -e "bash -c 'rosrun mypackage remoteCtrl.py'"

gnome-terminal --tab --title="constant_command.py" -e "bash -c 'rosrun mypackage constant_command.py'"
