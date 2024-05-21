from setuptools import setup, find_packages

# Project description
description_text = """
MCCI’s Model 3501 Type-C SuperMUTT allows for extensive automatic testing of USB hosts that implement support for USB 3.1 gen1, USB-C™ Power Delivery, and DisplayPort alternate mode, based on the Microsoft SuperMutt.
"""

setup(
    name='model3501api',
    version='v1.0.0',
    description='API for MCCI Type-C SuperMUTT Model3501',
    long_description=description_text,
    author='MCCI Corporation',
    author_email='vinayn@mcci.com',
    packages=find_packages(),
    install_requires=[
        'pyusb',  # Add other dependencies if necessary
    ],
    url='https://github.com/mcci-usb/cricketlib',
)
