#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    pkg_share = get_package_share_directory('hospital_description')

    urdf_file = os.path.join(
        pkg_share,
        'urdf',
        'hospital_robot.urdf'
    )

    urdf_arg = DeclareLaunchArgument(
        'urdf_path',
        default_value=urdf_file,
        description='Path to robot URDF'
    )

    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='hospital_robot'
    )

    x_arg = DeclareLaunchArgument('x', default_value='0.0')
    y_arg = DeclareLaunchArgument('y', default_value='0.0')
    z_arg = DeclareLaunchArgument('z', default_value='0.1')

    robot_description = ParameterValue(
        Command([
            'cat',
            ' ',
            LaunchConfiguration('urdf_path')
        ]),
        value_type=str
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-name', LaunchConfiguration('robot_name'),
            '-topic', 'robot_description',
            '-x', LaunchConfiguration('x'),
            '-y', LaunchConfiguration('y'),
            '-z', LaunchConfiguration('z')
        ]
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
            '/model/hospital_robot/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'            ]
    )

    return LaunchDescription([
        urdf_arg,
        robot_name_arg,
        x_arg,
        y_arg,
        z_arg,
        robot_state_publisher,
        spawn_robot,
        bridge
    ])