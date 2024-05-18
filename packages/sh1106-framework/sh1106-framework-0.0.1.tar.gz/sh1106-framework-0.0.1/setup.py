from setuptools import setup, find_packages

setup(
name='sh1106_framework',
version='0.0.1',
author='Dan Convey',
description='A state manager, graphics, image, and custom font drawing package for the SH1106 OLED screen based on the luma.oled package. It works with Raspberry Pi and other Linux-based single-board computers.',
packages=find_packages(),
classifiers=[
"Programming Language :: Python",
"Programming Language :: Python :: 3",
"License :: OSI Approved :: Apache Software License",
"Operating System :: POSIX :: Linux",
"Operating System :: Other OS"
],
python_requires='>=3.10',
)

