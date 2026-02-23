from setuptools import setup
import os
from glob import glob

package_name = 'diff_drive_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],

    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),

        ('share/' + package_name, ['package.xml']),

        # Install launch files
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),

        # Install config files (if any)
        (os.path.join('share', package_name, 'config'),
            glob('config/*')),
    ],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pg',
    maintainer_email='pg@todo.todo',
    description='Diff Drive Robot with Serial Interface',
    license='TODO: License declaration',

    tests_require=['pytest'],

    entry_points={
        'console_scripts': [

            # 🔹 Serial communication node
            'serial_node = diff_drive_robot.serial_node:main',
            'odom_node = diff_drive_robot.odom_node:main',
            'motor_node = diff_drive_robot.motor_node:main',

        ],
    },
)