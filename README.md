# twiki

## Mobile Robots Class Notes

### Running Programs:

Kevin programmed ```./twiki.sh``` to open all terminal files. (Also have ```./debug.sh``` for debugging)

Pro tip : be ready for a ton of open terminal windows. Keep that sh*t organized. Leave all terminals open.
  
1. ```roscore``` : this is the ROS master, must run to execute any nodes.
  
2. ```rostopic list``` : lists all available topics published by all publisher nodes
		
    a. ```rostopic info <topic>``` : view info about topic
		
    b. ```rostopic echo <topic>``` : view published messages on topic
			- e.g., ```rostopic echo /mobile_base/commands/velocity```
			- ```rostopic echo -c <topic>``` : clears screen every time a new message comes in 
      
3. ```rosrun <file name>``` : executes file
		
    a. ```run <topic name>``` : tool to monitor publications & subscriptions
    
4. ```roslaunch <name of node/thing launching> <file name>.launch``` : launch robot
		- e.g., ```roslaunch kobuki_node minimal.launch```
		- ```kobuki_node``` : launch robot kobuki, minimal.launch
		- ```kobuki_softnode``` : virtual world robot (use with ```rosrun rviz rviz```), full.launch
		- Node: should hear robot turn on (and many topics should open)
    
5. ```rosrun mypackage <node name>.py``` : run file
	
### Ros Commands:

- ```roscd mypackage/<tab>``` or ```roscd mypackage/scripts``` : go to woring directory (i.e., pre-installed packages)
- ```rosnode``` : display info on running nodes
- ```rosout``` or ```rosnode info```: show info about nodes
- ```rostopic``` : display info on running topics
- ```rostopic tye <topic name>``` : return the type of the message type being published over this topic
- ```rosrun <package name> <node name>``` : runs a node from a given package
- ```rosls``` : lists files in ROS package
- ```roscp``` : copies files to/from a ROS package
- ```rosmsg``` : provides info on ROS message 
- ```rossrv``` : " " ROS service

with ```rostopic``` and ```rosnode```:
	+ ```list``` : list information 
	+ ```-h``` : help
	+ ```-c``` : refresh
	+ ```-v``` : verbose
	+ ```echo``` : print to console

#### Important Concepts

1. Nodes : your programs, which are connected via topics
	- can be subscriber or publisher nodes
	- combine together into a graph (communicate with other nodes)
	1.a. Publisher 
	```pub = rospy.Publisher("<topic name>", <data type>, <queue_size=##>)``` : an object that published to topic
		- e.g., ```cmvision``` publishes the location of a block of colors to the control node, which can then move to the ball
		- Note: must publish (Twist()) command constantly to have robot move smoothly
	1.b. Subscriber
	```rospy.Subscriber("<topic name>",<data type>,<function name**>)``` : when new data is available callback to topic
		- e.g., rospy.Subscriber("kobuki_command", Twist, updateCommand)
		**generally includes "callback"
		- listen until something happens
		- whichever nodes want data subscribe
		- wants to know when new data comes in 
		- you don't have to worry about polling / checking
		- e.g., cmvision node subscribes to camera node, i.e, it's waiting for an image from the camera.

2. Topics : channel of communication (think: TCP or pipe)
	- asynchronous function calls
	- strongly typed (by ROS message transports)
	- uses TCP or UDP

3. Control node : runs in __main__, is the coordinator

4. Messages : nodes communicate by publishing messages (think package that's being sent through topic)
	- strongly typed 
	
5. Services: TBD?


#### Terminal Shortcuts

- ```Ctrl-Alt-t``` : new terminal window
- ```Ctrl-Shift-t``` : new terminal tab
- ```|``` : pipe = starts with 
- ```lsof | grep <start of file name>``` : list of files starting with ...
- ```kill.<process id>``` : kills process via command line

#### Long Notes

**python:**

- ```#!/usr/bin/env python``` : enables python to be used
  
- ```import rospy``` : ROS python
- create objects of data types: ```<name> = <data type>()```
  - e.g., ```command = Twist()```
- ```chmod +x <file name>.py``` : changes the file to executable mode
	
--------

**common packages:**

- geometry_msgs.msg 
		- Twist
- sensor_msgs.msg 
		- Joy
- kobuki_msgs.msg 
		- Sound
		- Led
		- BumperEvent
		- ButtonEvent
- std_msgs.msg 
		- Empty
- nav_msgs.msg 
		- Odometry
- tf.transformations 
		- euler_from_quaternion : convert quanternion
- math
		
--------
		
**<data types> in ROS includes:**

- String
- Joy 
  - buttons : array of integers
  
|index | xbox buttons |
| :---: | :---: |
| 0 | A |
| 1 | B |
| 2 | X |
| 3 | Y |
| 4 | LB |
| 5 | RB |
| 6 | back | 
| 7 | start |
| 8 | power |
| 9 | button stick L |
| 10 | button stick R |

|index | state |
| :---: | :---: |
| 0 | released |
| 1 | pressed |

  - axes : array floating points

|index | button name |
| :---: | :---: |
| 0 | L/R axis stick left |
| 1 | Up/Down Axis stick left |
| 2 | Left trigger |
| 3 | L/R Axis stick right |
| 4 | Up/Down Axis stick right |
| 5 | Right trigger |
| 6 | cross key L/R |
| 7 | cross key Up/Down |

- Twist 
  - linear : how fast robot should move
    - linear.x ([-1.0, 1.0])
      - backwards (negative)
			- forwards (positive)
		- linear.y (Kobuki doesn't need)
			- up and down
	- angular : how fast robot should turn
		- angular.z	([-0.8,0.8])
			- left (positive)
			- right (negative)
- ButtonEvent

|index | button on robot |
| :---: | :---: |
| 0 | B0 |
| 1 | B1 |
| 2 | B2 |

|index | state |
| :---: | :---: |
| 0 | released |
| 1 | pressed |

- Sound

|index | sound |
| :---: | :---: |
| 0 | turn on |
| 1 | turn off |
| 2 | recharge start |
| 3 | press button |
| 4 | error sound |
| 5 | start cleaning |
| 6 | cleaning end |

- Led : light

|index | light color |
| :---: | :---: |
| 0 | black (off) |
| 1 | green |
| 2 | orange |
| 3 | red |
			
- BumperEvent

|index | bumper |
| :---: | :---: |
| 0 | left |
| 1 | center |
| 2 | right |

|index | state |
| :---: | :---: |
| 0 | released |
| 1 | pressed |
	
--------
					
**common publishing  / subscription topics:**	

- /kobuki_command : usually with type Twist
- /mobile_base/commands/velocity : communicates with robot hardware to control movement speed
  - e.g., ```pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=10)```
  - e.g., ```pub1 = rospy.Publisher('/mobile_base/commands/led1', Led, queue_size=10)```
  - when you tell robot Twist() /velocity tells robot to move
- /odom : can tell you -> how far? how many degrees?
  - pose
    - pose
      - position : z, float (in meters)
      - orientation : (in quanternion)
        - x
        - y
- /mobile_base/events/bumper : with type BumperEvent
- /mobile_base/events/button : with type ButtonEvent				
- /mobile_base/commands/reset odometry : allows us to use odometry
- /mobile_base/commands/sound : allows Kobuki to make sound
- /mobile_base/commands/led1 : light one
- /mobile_base/commands/led2 : light two 
- /emergency_stop : use type Empty for emergency stop
- /resume : use with type Empty

--------

**random:**

- ```
  if __name__ == '__main__' :
	  <control method>
  ```
e.g., 

``` 
if __name__ == '__main__':
  try:
     sendSounds()
  except rospy.ROSInterruptException:
    pass
```

- ```rospy.init_node("<file name>", anonymous = True)``` : must initialize our own nodes
	- e.g., ```rospy.init_node('forward', anonymous=True)``` : note that forward does not contain [.py]
	- e.g., ```rospy.init_node("joystick", anonymous=True)```
	- e.g., ```rospy.init_node('sound_sender', anonymous=True)```
	- e.g., ```rospy.init_node('leds_sender', anonymous=True)```
	
- ```rospy.sleep(<seconds>)``` : wait for <seconds> 

- ```rospy.on_shutdown(<method to reset robot>)``` : run till program recieved shutdown signal

- ```
  while pub.get_num_connections() == 0:
		pass
  ``` 
  : checks if there is a subscriber, if no one is listening, just continue (waiting until there is a subscriber node)
		
- ```rospy.spin()``` : keeps code from exiting until the service is shut down
	- required b/c main function does nothing (dev can use .spin() or create loop w/in main)

- for ```rviz```:
	1. set "fixed frame" to "odom"
	2. press "add"
	3. select "robotModel"

- ```
  while not rospy.is_shutdown():
	# code here
	pub.publish(<method; currentCommand>)
	rospy.sleep(0.1)
  ``` 
  need a loop, almost same as rospy.spin()

- You should **NOT** have a long queue (should be as short as possible)
	- callback can get called multiple times
  
	- ```queue_size=<#>``` : Maximum number of message that will be stored in case any subscriber is not receiving them fast enough.

	- ```rospy.spin()``` is a while loop that does calculations

- common nodes:
	- ```kobuki_node``` : robot + hardware
	- ```joy_node``` : 
		1. ```rosparam set joy_node/dev "/dev/input/js1"``` 
			- Notes: 
				- /dev/ represents all devices
				- by default joy_node uses js0
		2. ```rosrun joy joy_node``` : rosrun <package name> (<specific node name>)
