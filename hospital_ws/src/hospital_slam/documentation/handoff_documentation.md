# Handoff Documentation: SLAM Integration

**Prepared For**: Deep Reinforcement Learning (DRL) Navigation & Control Team  
**Subject**: Transitioning 2D SLAM Mapping Pipeline to Autonomous Navigation  

---

## 1. Package Integration Guide

This package provides a robust map-building pipeline. To integrate the generated maps and SLAM transforms with your DRL controller/local planner:

1. **Subscribing to `/map`**: The SLAM node publishes `nav_msgs/msg/OccupancyGrid` on `/map` at 0.5Hz - 2Hz depending on map updates.
2. **Transform Lookups**: Use the TF listener to query the transform from `map` to `base_link` for global localization.
3. **Driving Commands**: Send velocity commands to `/cmd_vel` as standard `geometry_msgs/msg/Twist`.

---

## 2. Sensor Bridge & Frame Overrides

Gazebo Sim publishes sensor topics with long nested frame names (e.g., `hospital_robot/base_link/lidar_sensor`). 

To prevent TF errors in ROS 2, we configured a custom `bridge.yaml` inside `hospital_description/config/bridge.yaml` that explicitly overrides the ROS message headers to target `lidar_link` and `camera_link` directly:
```yaml
- topic_name: "/scan"
  direction: GZ_TO_ROS
  gz_type: "gz.msgs.LaserScan"
  ros_type: "sensor_msgs/msg/LaserScan"
  lazy: false
  ros_device_frame_id: "lidar_link" # Explicitly overrides TF parent link

- topic_name: "/camera/image_raw"
  direction: GZ_TO_ROS
  gz_type: "gz.msgs.Image"
  ros_type: "sensor_msgs/msg/Image"
  lazy: false
  ros_device_frame_id: "camera_link" # Explicitly overrides TF parent link
```
> [!IMPORTANT]
> If you change sensor links in the robot URDF, you **must** update the corresponding `ros_device_frame_id` values in `bridge.yaml` to ensure the TF trees align.

---

## 3. Lifecycle Node Management

Unlike earlier ROS versions, `slam_toolbox` in ROS 2 Jazzy uses **Lifecycle Nodes** to manage resource consumption.
- If launched as a standard node, it will remain in an `Unconfigured` state and ignore sensor topics.
- Our custom `slam.launch.py` wraps the execution in a Lifecycle manager using the official `online_async_launch.py` to auto-configure and activate the node.
- To programmatically reset or pause mapping, you can use the ROS 2 service calls:
  ```bash
  ros2 service call /slam_toolbox/change_state lifecycle_msgs/srv/ChangeState "{transition: {id: 1}}"
  ```

---

## 4. Known Issues & Troubleshooting

* **RobotModel Red Warning in RViz**:
  - *Symptom*: RViz displays a red warning icon next to the `RobotModel` namespace.
  - *Solution*: **This is non-critical and can be ignored**. A KDL parser warning for root link inertia causes this, but the model still renders and SLAM maps correctly.
* **Duplicate Robots, Blinking, or Sensor Failures**:
  - *Symptom*: Duplicate robots appear on screen, or `/scan` topic is missing.
  - *Solution*: A zombie Gazebo simulation server (`gz sim server`) is running in the background. Terminate all background servers and launchers using:
    ```bash
    pkill -9 -f "gz sim" && pkill -9 -f "ros2" && pkill -9 -f "rviz"
    ```
* **Robot Does Not Move via Keyboard Teleop**:
  - *Symptom*: Driving commands are sent, but the robot remains static in Gazebo.
  - *Solution*: Check if the simulation is paused in the Gazebo GUI footer (click the play button) and make sure your command shell has focus when pressing keys.
* **QoS Durability Mismatch Warnings**: You may see RViz console warnings regarding `/tf_static` QoS durability. These can be safely ignored as standard transformations are published dynamically.
* **Message Filter Drops**: At startup, you may see `Message Filter dropping message` warnings in RViz. This is normal until the SLAM node finishes initializing and publishes the first `map` -> `odom` correction frame.

---

## 5. Next Steps for the DRL Team

1. **Load Pre-built Map**: Use `nav2_map_server`'s map server to load the saved `hospital_map.yaml` directly without running SLAM.
2. **Localization Mode**: Change `mode` in `mapper_params_online_async.yaml` from `mapping` to `localization` to run AMCL or SLAM Toolbox in localization-only mode.
3. **Sensor Range Tuning**: The Ceres solver matching distance (`minimum_travel_distance`) is currently set to `0.3` meters. For fast navigation, you may need to reduce this to `0.1` to refine pose estimations.
