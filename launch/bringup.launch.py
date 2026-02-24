from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    use_sim_time = True

    diff_drive_pkg = get_package_share_directory('diff_drive_robot')
    nav2_pkg = get_package_share_directory('nav2_bringup')

    diff_drive_share = FindPackageShare('diff_drive_robot')
    nav2_share = FindPackageShare('nav2_bringup')

    ekf_config = os.path.join(diff_drive_pkg, 'config', 'ekf.yaml')


      # 1Robot + mapping
    robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                diff_drive_share,
                'launch',
                'robot.launch.py'
            ])
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )


    # ---------------- Nodes ----------------
    serial_node = Node(
        package='diff_drive_robot',
        executable='serial_node.py',
        name='serial_node',
        output='screen'
    )

    motor_node = Node(
        package='diff_drive_robot',
        executable='motor_node.py',
        name='motor_node',
        output='screen'
    )

    odom_node = Node(
        package='diff_drive_robot',
        executable='odom_node.py',
        name='odom_node',
        output='screen'
    )

    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config]
    )

    lidar_node = Node(
        package='rplidar_ros',
        executable='rplidar_composition',
        name='rplidar_node',
        output='screen',
        parameters=[{
            'serial_port': '/dev/ttyUSB1',
            'serial_baudrate': 115200,
            'frame_id': 'laser'
        }]
    )


    # Nav2 bringup
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                nav2_pkg,
                'launch',
                'bringup_launch.py'
            ])
        ),
        launch_arguments={
            'map': '/home/pg/my_map.yaml',
            'use_sim_time': 'true',
             'params_file': PathJoinSubstitution([
                diff_drive_pkg,
                'config',
                'nav2_params.yaml'
                ])
        }.items()
    )

    # RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=[
            '-d',
            '/opt/ros/jazzy/share/nav2_bringup/rviz/nav2_default_view.rviz'
        ],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )




    return LaunchDescription([
        robot_launch,
        serial_node,
        odom_node,
        ekf_node,
        motor_node,
        lidar_node,
        nav2_launch,
        rviz,
    ])