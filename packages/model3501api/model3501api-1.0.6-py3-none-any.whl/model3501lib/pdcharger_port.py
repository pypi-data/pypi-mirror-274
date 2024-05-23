##############################################################################
# 
# Module: pdcharger_port.py
#
# Description:
#     Switch PD to charger receptacle.
#
# Author:
#     Vinay N, MCCI Corporation May 2024
#
#############################################################################
import usb.core

class PDChargerPortController:
    def __init__(self, vendor_id, product_id):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
    
    def find_device(self):
        self.device = usb.core.find(idVendor=self.vendor_id, idProduct=self.product_id)
        return self.device is not None
    
    def pd_charger_port(self):
        if self.device is None:
            print("Device not found")
            return False
        
        # Control transfer parameters for PD Charger Port
        bmRequestType = 0x40  # Request type: Vendor, Host-to-device, Device-to-interface
        bRequest = 0xE9       # Request code for PD Charger Port command
        wValue = 0x0000       # Value
        wIndex = 0x0001       # Index
        wLength = 0x0000      # Length

        # Send control transfer for PD Charger Port command
        result = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)
        print("result-pd-charger-port:", result)
        if result == 0:
            print("Switched PD to charger receptacle successfully")
        else:
            print("Failed to switch PD to charger receptacle")
        return result == 0

def pd_charger_port_status():
    VENDOR_ID = 0x045e  # Replace with your vendor ID
    PRODUCT_ID = 0x078f  # Replace with your product ID

    controller = PDChargerPortController(VENDOR_ID, PRODUCT_ID)
    if controller.find_device():
        controller.pd_charger_port()
