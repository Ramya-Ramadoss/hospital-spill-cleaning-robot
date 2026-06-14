# Hospital Navigation System

A ROS 2 Jazzy + Gazebo Harmonic simulation project for an autonomous mobile
robot operating inside a simulated hospital environment.

---

## 1. Project Overview

This project simulates a mobile robot navigating a hospital building that
contains the following areas:

- Reception Area
- Waiting Area
- Nurse Station
- ICU Room
- Patient Room 1
- Patient Room 2
- Central Corridor connecting all rooms

The simulation environment is built entirely from simple SDF box geometries
(walls, beds, chairs, tables, medical carts) so it runs without external mesh
dependencies.

### Team Responsibilities

| Area | Owner |
|------|-------|
| Hospital environment (Gazebo world) | Member 1 |
| Robot description (URDF) | Member 1 |
| Gazebo simulation launch setup | Member 1 |
| Documentation | Member 1 |
| SLAM (slam_toolbox / Cartographer) | Member 2 |
| Navigation (Nav2) / Localization | Member 2 |

This repository (Member 1 deliverables) does **not** include SLAM, mapping,
localization, or Nav2 configuration. Those are maintained separately by the
SLAM/Navigation team member.

---

## 2. Folder Structure

Hospital-Navigation-System/

│

├── README.md

├── docs/

│

└── hospital_ws/

├── src/

│   ├── hospital_description/

│   │   ├── launch/

│   │   │   └── spawn_robot.launch.py

│   │   ├── urdf/

│   │   │   └── hospital_robot.urdf

│   │   ├── meshes/

│   │   ├── config/

│   │   └── resource/

│   │

│   ├── hospital_simulation/

│   │   ├── worlds/

│   │   │   └── hospital_world.sdf

│   │   ├── models/

│   │   ├── launch/

│   │   │   └── hospital_world.launch.py

│   │   └── resource/

│   │

│   ├── hospital_slam/        (maintained by SLAM/Navigation member)

│   └── hospital_navigation/  (maintained by SLAM/Navigation member)

│

├── build/

├── install/

└── log/

---

---

## 3. Technology Stack

- Ubuntu 24.04 LTS
- ROS 2 Jazzy Jalisco
- Gazebo Harmonic
- ros_gz (ROS 2 <-> Gazebo integration)
- Python 3
- colcon build system

---

## 4. Installation Steps

### 4.1 Install ROS 2 Jazzy

Follow the official ROS 2 Jazzy installation guide for Ubuntu 24.04:
https://docs.ros.org/en/jazzy/Installation.html

### 4.2 Install Gazebo Harmonic

```bash
sudo apt update
sudo apt install ros-jazzy-ros-gz
```

This installs Gazebo Harmonic along with the `ros_gz_sim` and `ros_gz_bridge`
packages used by the launch files in this project.

### 4.3 Install additional dependencies

```bash
sudo apt install ros-jazzy-robot-state-publisher \
                  ros-jazzy-joint-state-publisher \
                  ros-jazzy-xacro
```

### 4.4 Clone the repository

```bash
cd ~/
git clone https://github.com/<your-org>/Hospital-Navigation-System.git
cd Hospital-Navigation-System/hospital_ws
```

---

## 5. Build Commands

From the workspace root (`hospital_ws/`):

```bash
cd ~/Hospital-Navigation-System/hospital_ws

# Source ROS 2 Jazzy
source /opt/ros/jazzy/setup.bash

# Build the workspace
colcon build --symlink-install

# Source the local overlay
source install/setup.bash
```

---

## 6. Run Commands

### 6.1 Launch the hospital world in Gazebo Harmonic

```bash
ros2 launch hospital_simulation hospital_world.launch.py
```

This opens Gazebo Harmonic with `hospital_world.sdf` loaded, including all
rooms, walls, furniture, lighting, and the floor plane.

### 6.2 Spawn the hospital_robot into the world

In a second terminal (after sourcing the workspace):

```bash
ros2 launch hospital_description spawn_robot.launch.py
```

This:
- Publishes the `hospital_robot` description via `robot_state_publisher`
- Spawns the robot into the running Gazebo simulation
- Bridges `cmd_vel`, `odom`, `scan`, `camera/image_raw`, and `tf` topics
  between ROS 2 and Gazebo

### 6.3 Verify topics

```bash
ros2 topic list
```

You should see topics such as `/cmd_vel`, `/odom`, `/scan`,
`/camera/image_raw`, `/tf`, and `/clock`.

### 6.4 Drive the robot manually (optional, for testing)

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

---

## 7. Notes

- `hospital_slam` and `hospital_navigation` packages are owned and developed
  by another team member and are intentionally not included in this set of
  deliverables.
- The hospital world uses only basic SDF `<box>` and `<plane>` geometries —
  no external meshes or models are required.
