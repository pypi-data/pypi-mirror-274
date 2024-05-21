from setuptools import setup, find_packages

setup(
    name='YourPackageName',
    version='1.0.0',
    author='Your Name',
    author_email='your@email.com',
    description='Description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/yourproject',
    packages=find_packages(),
    install_requires=[
        'pyusb',  # Assuming you'll use pyusb to interact with USB devices
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
