# Hospital SLAM Package

This package implements 2D SLAM mapping for the hospital cleaning robot in Gazebo Harmonic using ROS 2 Jazzy and `slam_toolbox`. It is configured to handle the sensor bridges, override coordinates frames, run mapping in RViz, and save the occupancy grid map.

---

## 1. Package Structure

```
hospital_slam/
├── config/
│   └── mapper_params_online_async.yaml   # Configured slam_toolbox parameters
├── launch/
│   └── slam.launch.py                    # Node launcher (SLAM + RViz2)
├── maps/
│   ├── hospital_map.pgm                  # Generated grid map image
│   └── hospital_map.yaml                 # Grid map metadata
├── rviz/
│   └── slam.rviz                         # Custom RViz layout configuration
├── screenshots/                          # Verification images
│   ├── camera_view.png
│   ├── gazebo_simulation.png
│   ├── hospital_map.png
│   └── rviz_mapping.png
├── documentation/                        # Project reports & handoff files
│   ├── technical_documentation.md
│   ├── handoff_documentation.md
│   └── performance_evaluation.md
├── package.xml
└── setup.py
```

---

## 2. Dependencies

- ROS 2 Jazzy Jalisco
- `slam_toolbox` (Lifecycle node implementation)
- `nav2_map_server` (For saving/loading maps)
- `rviz2` (For visualization)

---

## 3. Quick Start Launch Sequence

Make sure you have built the workspace and sourced the setup bash files:

```bash
cd ~/Projects/hospital-spill-cleaning-robot/hospital_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

### Step 1: Launch the Hospital World
Start the Gazebo simulation environment:
```bash
ros2 launch hospital_simulation hospital_world.launch.py
```

### Step 2: Spawn the Robot and Bridge Sensors
In a new terminal:
```bash
source install/setup.bash
ros2 launch hospital_description spawn_robot.launch.py
```

### Step 3: Start SLAM and RViz
In a third terminal:
```bash
source install/setup.bash
ros2 launch hospital_slam slam.launch.py
```
This loads our custom Ceres solver parameters, transitions the SLAM node from *Configure* to *Activate*, and automatically opens RViz2 displaying the map, scans, and robot model.

---

## 4. Mapping & Map Saving Workflow

1. Teleoperate the robot or run a script to drive it through the rooms to scan the hospital walls:
   ```bash
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```
2. Once the map is fully populated in RViz, save the occupancy grid map:
   ```bash
   ros2 run nav2_map_server map_saver_cli -f ~/Projects/hospital-spill-cleaning-robot/hospital_ws/src/hospital_slam/maps/hospital_map
   ```

---

## 5. Further Reading

For full details, please refer to:
- [Technical Documentation](documentation/technical_documentation.md)
- [Handoff Documentation (DRL Team)](documentation/handoff_documentation.md)
- [Performance Evaluation](documentation/performance_evaluation.md)
