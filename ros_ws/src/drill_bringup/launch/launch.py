from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # GUI node
        Node(
            package='drill_gui',
            executable='drill_gui',
            name='drill_gui',
            output='screen',
            arguments=['--ros-args', '--log-level', 'info']
        ),
        # Communication node
        Node(
            package='drill_communication',
            executable='drill_com',
            name='drill_communication',
            output='screen',
            arguments=['--ros-args', '--log-level', 'info']
        )
    ])

