#!/bin/bash


gnome-terminal --tab --title="roscore" -e "bash -c 'roscore'"

sleep 2s

gnome-terminal --tab --title="kobuki" -e "bash -c 'roslaunch kobuki_node minimal.launch'"

gnome-terminal --tab --title="constant_command.py" -e "bash -c 'rosrun mypackage constant_command.py -r'"

rosrun mypackage batch_node.py "$@"
