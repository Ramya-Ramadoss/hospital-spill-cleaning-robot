from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
import os


def generate_launch_description():

    pkg_share = get_package_share_directory('hospital_slam')

    # Path to custom SLAM parameters
    config = os.path.join(
        pkg_share,
        'config',
        'mapper_params_online_async.yaml'
    )

    # Path to custom RViz configuration
    rviz_config = os.path.join(
        pkg_share,
        'rviz',
        'slam.rviz'
    )

    # Launch arguments
    rviz_arg = DeclareLaunchArgument(
        'rviz',
        default_value='true',
        description='Whether to launch RViz'
    )

    # Include official slam_toolbox launch file to handle lifecycle transitions
    slam_toolbox_dir = get_package_share_directory('slam_toolbox')
    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_toolbox_dir, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'slam_params_file': config,
            'use_sim_time': 'true'
        }.items()
    )

    # RViz node
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(LaunchConfiguration('rviz')),
        output='screen'
    )

    return LaunchDescription([
        rviz_arg,
        slam_toolbox_launch,
        rviz
    ])