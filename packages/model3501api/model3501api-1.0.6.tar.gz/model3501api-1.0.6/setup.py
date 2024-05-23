##############################################################################
# 
# Module: setup.py
#
# Description:
#     setup to install the cricklib package
#
# Author:
#     MCCI , MCCI   May 2024
#
##############################################################################

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='model3501api',
    version='v1.0.6',
    description='API for MCCI Type C Super MUTT Model 3501.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='MCCI Corporation',
    author_email='vinayn@mcci.com',
    url='https://github.com/mcci-usb/model3501lib',
    packages=find_packages(),
    install_requires=[
        'pyusb',  # Add other dependencies if necessary
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: zlib/libpng License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)


