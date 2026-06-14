#!/usr/bin/env python3
"""
Launch file: hospital_world.launch.py

Responsibility (Member 1):
- Start Gazebo Harmonic (gz sim) with the custom hospital_world.sdf
- Bridge the Gazebo simulation clock to ROS 2 so all nodes share /clock

Usage:
    ros2 launch hospital_simulation hospital_world.launch.py
"""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # ------------------------------------------------------------
    # Locate the hospital_world.sdf file inside this package
    # ------------------------------------------------------------
    pkg_hospital_simulation = get_package_share_directory('hospital_simulation')

    default_world_path = os.path.join(
        pkg_hospital_simulation, 'worlds', 'hospital_world.sdf'
    )

    # ------------------------------------------------------------
    # Launch arguments
    # ------------------------------------------------------------
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world_path,
        description='Full path to the Gazebo world SDF file to load'
    )

    # ------------------------------------------------------------
    # Include ros_gz_sim's gz_sim.launch.py to start Gazebo Harmonic
    # '-r' runs the simulation immediately, '-v 4' enables verbose output
    # ------------------------------------------------------------
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': [LaunchConfiguration('world'), ' -r -v 4']
        }.items()
    )

    # ------------------------------------------------------------
    # Bridge /clock from Gazebo to ROS 2 (needed for time sync
    # with robot_state_publisher, sensors, SLAM, Nav2, etc.)
    # ------------------------------------------------------------
    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='clock_bridge',
        output='screen',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ]
    )

    return LaunchDescription([
        world_arg,
        gz_sim,
        clock_bridge,
    ])