##############################################################################
# 
# Module: setup.py
#
# Description:
#     setup to install the model3501api package
# Author:
#     Vinay N MCCI, May 2024
#
##############################################################################
from setuptools import setup, find_packages

setup(
    name='model3501api',
    version='v1.0.5',
    description='API for MCCI Type C Super MUTT Model 3501',
    long_description='MCCI Model 3501 SuperMUTT Python based library for control and operation',
    long_description_content_type='text/markdown',
    author='MCCI Corporation',
    author_email='vinayn@mcci.com',
    url='https://github.com/mcci-usb/model3501lib',
    packages=find_packages(),
    install_requires=[
        'pyusb',  # Add other dependencies if necessary
    ],
)
