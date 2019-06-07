#!/bin/bash

gnome-terminal --tab --title="roscore" -e "bash -c 'roscore';bash"

sleep 2s

gnome-terminal --tab --title="joystick" -e "bash -c './set_joystick.sh';bash"

gnome-terminal --tab --title="kobuki" -e "bash -c 'roslaunch kobuki_node minimal.launch';bash"

gnome-terminal --tab --title="remoteCtrl.py" -e "bash -c 'rosrun mypackage remoteCtrl.py';bash"

gnome-terminal --tab --title="constant_command.py" -e "bash -c 'rosrun mypackage constant_command.py';bash"

gnome-terminal --tab --title="kobuki_command echo" -e "bash -c 'rostopic echo -c /kobuki_command';bash"
