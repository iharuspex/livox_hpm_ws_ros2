from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pointcloud_to_las',
            executable='converter_node',
            name='pointcloud_to_las',
            output='screen',
            parameters=[{
                'input_topic': '/pub_pointcloud2',
            }]
        ),
    ])