from setuptools import find_packages, setup

package_name = 'hospital_slam'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    (
        'share/ament_index/resource_index/packages',
        ['resource/hospital_slam'],
    ),
    (
        'share/hospital_slam',
        ['package.xml'],
    ),
    (
        'share/hospital_slam/launch',
        ['launch/slam.launch.py'],
    ),
    (
        'share/hospital_slam/config',
        ['config/mapper_params_online_async.yaml'],
    ),
    (
        'share/hospital_slam/rviz',
        ['rviz/slam.rviz'],
    ),
    (
        'share/hospital_slam/documentation',
        [
            'documentation/technical_documentation.md',
            'documentation/handoff_documentation.md',
            'documentation/performance_evaluation.md',
        ],
    ),
    (
        'share/hospital_slam/screenshots',
        [
            'screenshots/camera_view.png',
            'screenshots/gazebo_simulation.png',
            'screenshots/hospital_map.png',
            'screenshots/rviz_mapping.png',
        ],
    ),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ramya-ramadoss',
    maintainer_email='hairamya57@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
