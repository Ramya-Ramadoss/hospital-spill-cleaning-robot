#!/usr/bin/env python3
"""
Launch file: spawn_robot.launch.py

Responsibility (Member 1):
- Publish the hospital_robot URDF via robot_state_publisher
- Spawn hospital_robot into the running Gazebo Harmonic world
- Bridge cmd_vel / odom / tf topics between ROS 2 and Gazebo

Usage:
    ros2 launch hospital_description spawn_robot.launch.py

Note: Run hospital_world.launch.py first so Gazebo is already running.
"""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():

    # ------------------------------------------------------------
    # Locate the robot URDF file inside this package
    # ------------------------------------------------------------
    pkg_hospital_description = get_package_share_directory('hospital_description')

    default_urdf_path = os.path.join(
        pkg_hospital_description, 'urdf', 'hospital_robot.urdf'
    )

    # ------------------------------------------------------------
    # Launch arguments
    # ------------------------------------------------------------
    urdf_arg = DeclareLaunchArgument(
        'urdf_path',
        default_value=default_urdf_path,
        description='Full path to the hospital_robot URDF file'
    )

    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='hospital_robot',
        description='Name of the robot entity inside Gazebo'
    )

    x_pose_arg = DeclareLaunchArgument('x', default_value='0.0')
    y_pose_arg = DeclareLaunchArgument('y', default_value='0.0')
    z_pose_arg = DeclareLaunchArgument('z', default_value='0.1')

    # ------------------------------------------------------------
    # Read the URDF file content into the robot_description parameter
    # ------------------------------------------------------------
    robot_description = Command(['cat ', LaunchConfiguration('urdf_path')])

    # ------------------------------------------------------------
    # robot_state_publisher: publishes /robot_description and TF
    # ------------------------------------------------------------
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,
        }]
    )

    # ------------------------------------------------------------
    # Spawn the robot into Gazebo Harmonic using ros_gz_sim "create"
    # Reads the URDF from the /robot_description topic
    # ------------------------------------------------------------
    spawn_entity_node = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_hospital_robot',
        output='screen',
        arguments=[
            '-name', LaunchConfiguration('robot_name'),
            '-topic', 'robot_description',
            '-x', LaunchConfiguration('x'),
            '-y', LaunchConfiguration('y'),
            '-z', LaunchConfiguration('z'),
        ]
    )

    # ------------------------------------------------------------
    # ROS <-> Gazebo bridge for robot control / sensor topics
    # ------------------------------------------------------------
    ros_gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='hospital_robot_bridge',
        output='screen',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
        ],
        remappings=[
            ('/cmd_vel', '/cmd_vel'),
            ('/odom', '/odom'),
        ]
    )

    return LaunchDescription([
        urdf_arg,
        robot_name_arg,
        x_pose_arg,
        y_pose_arg,
        z_pose_arg,
        robot_state_publisher_node,
        spawn_entity_node,
        ros_gz_bridge_node,
    ])