##############################################################################
# 
# Module: getrdo.py
#
# Description:
#     Read the RDO for the current power contract.
#
# Author:
#     Vinay N, MCCI Corporation May 2024
#
#############################################################################
import usb.core

class getrdoController:
    def __init__(self, vendor_id, product_id):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
    
    def find_device(self):
        self.device = usb.core.find(idVendor=self.vendor_id, idProduct=self.product_id)
        return self.device is not None
    
    def get_rdo(self):
        if self.device is None:
            print("Device not found")
            return False
        else:
            print("Device found")
        
        bmRequestType = 0x40
        bRequest = 0xE4
        wValue = 0x0000
        wIndex = 0x0000
        wLength = 0x0010
        data1 = [0x00, 0x2A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        result1 = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data1)
        print("result-1:", result1)
        
        if result1 == 16:
            bmRequestType = 0xC0
            bRequest = 0xE4
            wValue = 0x0000
            wIndex = 0x0000
            wLength = 0x0010
            result2 = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)
            hex_strings = ['0x{:02X}'.format(byte) for byte in result2]
            formatted_hex_string = ' '.join(hex_strings)
            print("Read the RDO for the current power contract:", formatted_hex_string)
        else:
            print("No RDO: no power contract in place between the system and the Type-C MUTT")

def get_rdo_status():
    VENDOR_ID = 0x045e
    PRODUCT_ID = 0x078f

    controller = getrdoController(VENDOR_ID, PRODUCT_ID)
    if controller.find_device():
        controller.get_rdo()
