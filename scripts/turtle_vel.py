#!/usr/bin/env python3

# import ROS for developing the node
import rospy
# import geometry_msgs/Twist for control commands
from geometry_msgs.msg import Twist
# we are going to read turtlesim/Pose messages this time
from turtlesim.msg import Pose
#importing the new message from our package
from robotics_lab_1.msg import Turtlecontrol
# for radians to degrees conversions
import math

ROTATION_SCALE = 180.0/math.pi
pos_msg = Pose()
control_msg = Turtlecontrol()
def pose_callback(data):
	global pos_msg
	#convert x to cm
	pos_msg.x = data.x
	#print('pose callback:',pos_msg, data)
	
def control_gain(data):
	global control_msg
	control_msg.kp = data.kp
	control_msg.xd = data.xd
	#print('control callback:',data,control_msg)


if __name__ == '__main__':
	# initialize the node
	rospy.init_node('turtle_vel', anonymous = True)
	# add a subscriber to it to read the position information
	rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
	rospy.Subscriber('/turtle1/control_params', Turtlecontrol, control_gain)

	# add a publisher with a new topic using the Turtlecontrol message
	cmd_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
	# set a 10Hz frequency for this loop
	loop_rate = rospy.Rate(10)
	vel_cmd = Twist()
	
	while not rospy.is_shutdown():
		# publish the message
		print('main loop:',pos_msg,control_msg)
		
		vel_cmd.linear.x = control_msg.kp*(control_msg.xd-pos_msg.x)
		cmd_pub.publish(vel_cmd)
		# wait for 0.1 seconds until the next loop and repeat
		loop_rate.sleep()
	

