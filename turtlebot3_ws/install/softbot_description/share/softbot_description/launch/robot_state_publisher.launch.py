#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def generate_launch_description():


    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('softbot_description'))
    robot_description_path = xacro.process_file(
        os.path.join(
            pkg_path,
            'urdf',
            'softbot.urdf.xacro'
            )
        ).toxml()

    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
        )
 

    

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time,
             'robot_description': robot_description_path}
            ],
        )

    ld = LaunchDescription()

    ld.add_action(declare_use_sim_time_cmd)

    ld.add_action(robot_state_publisher_node)

    return ld