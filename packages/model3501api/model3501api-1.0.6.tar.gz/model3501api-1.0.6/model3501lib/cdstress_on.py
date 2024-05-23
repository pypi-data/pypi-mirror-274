##############################################################################
# 
# Module: cdstress_on.py
#
# Description:
#     Enable connect disconnect stress.
#
# Author:
#     Vinay N, MCCI Corporation May 2024
#
#############################################################################
import usb.core

class CDstressONController:
    def __init__(self, vendor_id, product_id):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
    
    def find_device(self):
        self.device = usb.core.find(idVendor=self.vendor_id, idProduct=self.product_id)
        return self.device is not None
    
    def set_cdstree_on(self):
        if self.device is None:
            print("Device not found")
            return False
        
        # Enable connect disconnect stress
        bmRequestType = 0x40
        bRequest = 0xE8
        wValue = 0x00
        wIndex = 0x1
        wLength = 0x00

        # Send control transfer
        result = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)
        print("result_cd_stress:", result)
        return result == 0
    
    def setup_cd_stress_on(self):
        if self.find_device():
            if self.set_cdstree_on():
                print("CD Stress On command sent successfully")
            else:
                print("Failed to send CD Stress On command")
        else:
            print("Device not found")

def onset_cdstress():
    VENDOR_ID = 0x045e  # Replace with your vendor ID
    PRODUCT_ID = 0x078f  # Replace with your product ID

    controller = CDstressONController(VENDOR_ID, PRODUCT_ID)
    controller.setup_cd_stress_on()
