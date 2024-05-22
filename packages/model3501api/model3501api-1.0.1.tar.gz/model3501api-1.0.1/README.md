# cricketlib

This is a Python library to control MCCI USB Switches and supports to Cricket UI.
<!--
  This TOC uses the VS Code markdown TOC extension AlanWalk.markdown-toc.
  We strongly recommend updating using VS Code, the markdown-toc extension and the
  bierner.markdown-preview-github-styles extension. Note that if you are using
  VS Code 1.29 and Markdown TOC 1.5.6, https://github.com/AlanWalk/markdown-toc/issues/65# cricketlib

This is a Python library to s the MCCI USB Switches (switch 3201,2301, 3141, 3142, 2101) and supports to Cricket UI.


<!--
  This TOC uses the VS Code markdown TOC extension AlanWalk.markdown-toc.
  We strongly recommend updating using VS Code, the markdown-toc extension and the
  bierner.markdown-preview-github-styles extension. Note that if you are using
  VS Code 1.29 and Markdown TOC 1.5.6, https://github.com/AlanWalk/markdown-toc/issues/65
  applies -- you must change your line-ending to some non-auto value in Settings>
  Text Editor>Files.  `\n` works for me.
-->
<!-- markdownlint-disable MD033 MD004 -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->
<!-- TOC depthFrom:2 updateOnSave:true -->

- [Introduction](#introduction)
- [Install python](#install-python37-32-bit-package)
- [Prerequisites for running or building](#prerequisites-for-running-or-building)
- [Installing cricketlib Packages](#installing-cricketlib-packages)
- [package usage](#package-usage)

- [Release History](#release-history)

## Introduction
This repository is supports the `Cricket UI` and switching the MCCI USB Switches.

### Install Python3.7 (32-bit) package 
install python package from [python.org](https://www.python.org/ftp/python/3.7.8/python-3.7.8.exe)


### Install Python3.7 (64-bit) package
install python package from [python.org](https://www.python.org/ftp/python/3.7.8/python-3.7.8-amd64.exe)

### Install pip package
```shell
pip --version
python -m pip install --upgrade pip
```

### Prerequisites for running or building

<strong>On Windows:</strong>

Development environment
* OS - Windows 10 and 11 64 bit
* Python - 3.7.8
* pyserial - 3.5
* pyusb - 1.2.1
* hidapi - 0.11.2

```shell
pip install pyserial
pip install pyusb
pip install hidapi==0.11.2
```

<strong>On Linux:</strong>

Development environment
* OS - Ubuntu 20.04 and Ubuntu 22.04 64 bit
* Python - 3.9.10
* pyserial - 3.4
* pyusb - 1.0.2
* libusb - 1.0.22b9
* libusb1 - 3.0.0
* hidapi - 0.11.2


```shell
sudo apt-get install python3-pip
sudo pip3 install pyserial
sudo pip3 install pyusb
sudo pip3 install libusb
sudo pip3 install libusb1
sudo pip3 install hidapi==0.11.2
```

<strong>On Mac:</strong>

Development environment
* OS - Mac OS - Catalina 10.15.7 64 bit
* Python - 3.6.9
* pyserial - 3.4
* pyusb - 1.0.2
* libusb - 1.0.22b9
* libusb1 - 3.0.0
* hidapi - 0.10.1 for Mac OS

```shell
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install pyserial
sudo pip3 install pyusb
brew install libusb
sudo pip3 install libusb1
brew install hidapi - Only for Mac OS
```
### Installing cricketlib Packages

1.  Clone the repository from [github](https://github.com/mcci-usb/cricketlib)

2.  Open a `cmd terminal` and change directory to  `{path_to_repository}/cricketlib`. using `cd` into the root directory where setup.py is located

3.  To install the library in your local Python setup, enter the command in Windows OS
```bash
python setup.py install
```
4.  To install the library in your local Python setup, enter the command in Linux OS.
```bash
sudo python3 setup.py install
```
5.  To install the library in your local Python setup, enter the command in `Mac OS`
```bash
sudo python3 setup.py install
```

Please navigate to dist/ directory and you will find the files .egg file.
Example: `cricketapi-1.5.0-py3.7.egg`

## package usage
Create a Python file named `Simpletest.py` and open in text editor and import the `cricketlib` modules.

```python
# avalaible list of MCCI Switches with port number
from cricketlib import searchswitch
```

```python
# import lib for switch 3142, switch3201, switch 2101, 2301
from cricketlib import switch3141
from cricketlib import switch3201
from cricketlib import switch2101 as S2101
from cricketlib import switch2301
```
```python
# found a list of available switches.
# using the port number open the switch.
dev_list = searchswitch.get_switches()
print(dev_list)
```
```python
# Serial Communication---
# windows Platform
# here COM5, COM8, COM13...etc are exapmple ports.
sw1 = switch3201.Switch3201('COM5') 
(or)
sw1 = switch3141.Switch3141('COM8')
(or)
sw1 = switch2101.Switch2101('0002CC0014FF')
(or)
sw1 = switch2301.Switch2301('COM13')
```
```python
# ---Linux Platform Serial Communication---
# here /dev/ttyACMO, /dev/ttyACMO.etc are exapmple ports number.
sw1 = switch3201.Switch3201('/dev/ttyACMO') 
(or)
sw1 = switch3141.Switch3141('/dev/ttyACMO')
```
### Connect the USB Switch to particular port number.
``` python
# Connect the USB Switch
sw1.connect()
```
### port on command using parameters depends upon switches
```python
# port on with port number
# sw1.port_on(1) first port ON
# sw1.port_on(2) second port ON
# sw1.port_on(3) third port 
# sw1.port_on(4) fourth port ON
# for switch3201, switch2301 have 4 ports
# for switch3141, switch3142 have 2 ports
# for switch2101 have 1 port

sw1.port_on(1)
```
### Switching the port OFF
```python
# port off with port number default empty or 0.
sw1.port_off()
```
### Requested commands

### Set Speed information 
```python
# Set High Speed
sw1.set_speed("HS")
# Set Super Speed
sw1.set_speed("SS")
```
### Get Status
```python
# Get the status of current port number.
sw1.get_status()
```
### Get the Volts and Amps information
```python
# get the voltage reading only for switch 3201, switch2301 and Switch3142
sw1.get_volts()
# get the amps reading only for switch 3201, switch2301 and switch3142
sw1.get_amps()
```
### Switch 2101 ports switching
```
sw3 = S2101.Switch2101('0002CC0014FF')
sw3.connect()
sw3.port_on("ss")
time.sleep(2)
sw3.port_off()
time.sleep(1)
sw3.port_on("hs")
time.sleep(1)
sw3.port_off()
```
## Release History
- v1.0.5 update hidapi package.
- v1.0.4 Support for Switch 2101 port status and implenting hidapi for windows and linux
- v1.0.3 Support python 64-bit
- v1.0.2 update speed change in switch2101
- v1.0.0 initial release