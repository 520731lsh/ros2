#!/bin/bash
cd ~/carla-ros-bridge/catkin_ws/src
chmod +x carla_manual_control.py
cd ~/carla-ros-bridge/catkin_ws && catkin_make
source devel/setup.bash
rosrun carla_ros_bridge carla_manual_control.py
