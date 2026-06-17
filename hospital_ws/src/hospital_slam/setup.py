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
