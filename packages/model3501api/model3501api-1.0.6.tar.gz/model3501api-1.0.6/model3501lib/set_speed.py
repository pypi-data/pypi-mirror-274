
##############################################################################
# 
# Module: set_speed.py
#
# Description:
#     Set to speed: s is super speed , h is high speed, l is low speed
#
# Author:
#     Vinay N, MCCI Corporation May 2024
#
##############################################################################
import usb.core

class DeviceController:
    def __init__(self, vendor_id, product_id):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
    
    def find_device(self):
        self.device = usb.core.find(idVendor=self.vendor_id, idProduct=self.product_id)
        return self.device is not None
    
    def set_device_speed(self, speed_type):
        if self.device is None:
            print("Device not found")
            return False
        
        bmRequestType = 0x40
        if speed_type == 's':
            bRequest = 0x15  # Super Speed request
        elif speed_type == 'h':
            bRequest = 0x14  # High Speed request
        elif speed_type == 'f':
            bRequest = 0x13  # Full Speed request
        else:
            print("Invalid speed type")
            return False
        
        wValue = 0x0000
        wIndex = 0x0000
        wLength = 0x0000

        result = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)

        if result == 0:
            print(f"Set {speed_type} speed successfully\n")
        else:
            print("Device is not found:\n")

def set_speed(speed_type):
    VENDOR_ID = 0x045e  # Replace with your vendor ID
    PRODUCT_ID = 0x078f  # Replace with your product ID

    controller = DeviceController(VENDOR_ID, PRODUCT_ID)
    if controller.find_device():
        controller.set_device_speed(speed_type)
