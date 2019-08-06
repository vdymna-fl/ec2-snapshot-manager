from setuptools import setup

setup(
    name='EC2 Snapshot Manager',
    version = '0.1',
    author='Vitaliy Dymna',
    description='Small python CLI to manage AWS EC2 instance snapshots',
    license='GPLv3',
    packages=['ec2_manager'],
    url="",
    install_requires=[
        'boto3',
        'click'
    ],
    entry_points='''
        [console_scripts]
        ec2-manager=ec2_manager.ec2_manager:cli
    '''
)