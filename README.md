# BLDC Mecanum Car Demo (ROS 2 Jazzy + Gazebo with Detailed Rollers)

This ROS 2 package simulates a 4-wheel mecanum drive robot in Gazebo Sim, utilizing **mecanum wheel models with individually modeled rollers** for higher physical fidelity. It employs the `BLDCGazeboROS2` plugin to simulate BLDC motor physics based on voltage commands. A `MecanumMapper` node (`cmd_vel_to_voltage.py`) converts `/cmd_vel` Twist messages into individual voltage commands for each wheel.

## 1. Prerequisites

* Ubuntu 24.04 (Noble)
* ROS 2 Jazzy
* Gazebo Sim (usually installed with `ros-jazzy-gazebo-ros-pkgs`)
* `colcon`, `git`
* `ros-jazzy-teleop-twist-keyboard`

## Install required ROS packages:

`sudo apt update`
`sudo apt install ros-jazzy-desktop ros-jazzy-gazebo-ros-pkgs python3-colcon-common-extensions git ros-jazzy-teleop-twist-keyboard`

## 2. Workspace Setup
Create your ROS 2 workspace:

mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src


Clone this package (replace <YOUR_REPO_URL>):

git clone <YOUR_REPO_URL>
git clone https://github.com/enro-itu/BLDCGazeboROS2.git


## Build
Navigate to the root of your workspace and build the packages:

cd ~/ros2_ws
colcon build --symlink-install


## Environment Setup
In every new terminal you use for this project, run the following commands:

source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

Set Gazebo Plugin Path: Ensure Gazebo can find the BLDC plugin library:

export GZ_SIM_SYSTEM_PLUGIN_PATH=$HOME/ros2_ws/install/bldc_gz_sim/lib:$GZ_SIM_SYSTEM_PLUGIN_PATH

Tip: Add these source and export commands to your ~/.bashrc file for automatic loading in new terminals.

1. Running the Simulation
You will need two separate terminals (ensure Environment Setup is done in both):

Terminal A (Start Simulation & Controller):

ros2 launch bldc_car_demo sim_car.launch.py

This launches Gazebo Sim with the specified world and the mecanum robot model (including detailed rollers and BLDC plugins). It also starts the mecanum_cmd_vel_to_voltage (MecanumMapper) node, loading parameters from params/car.yaml.

Terminal B (Keyboard Teleoperation):

ros2 run teleop_twist_keyboard teleop_twist_keyboard
This starts the keyboard teleoperation node, publishing commands to the /cmd_vel topic.


1. Controls
Use Terminal B (running teleop_twist_keyboard) to control the robot. Make sure this terminal window has focus.

Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

q/z, w/x, e/c: Adjust Speeds (Max, Linear, Angular)

CTRL+C: Stops the teleop node.
