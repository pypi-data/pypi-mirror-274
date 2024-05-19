from setuptools import setup, find_packages

setup(
    name='onlymaze',
    version='1.0.5',
    description='A simple maze game.',
    packages=find_packages(),
    install_requires=[
        'tk',
    ],
    entry_points={
        'console_scripts': [
            'onlymaze=onlymaze.maze:main',
        ],
    },
)

