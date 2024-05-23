##############################################################################
# 
# Module: emulate_charge.py
#
# Description:
#     Emulate a PD charger with max watts 'W'.
#
# Author:
#     Vinay N, MCCI Corporation May 2024
#
#############################################################################
import usb.core

class ChargeController:
    def __init__(self, vendor_id, product_id):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
    
    def find_device(self):
        self.device = usb.core.find(idVendor=self.vendor_id, idProduct=self.product_id)
        return self.device is not None
    
    def set_emulate_charge_15w(self, watts):
        if self.device is None:
            print("Device not found")
            return False
        
        bmRequestType_setup = 0x40
        bRequest_setup = 0xEE

        data_to_send_setup = [0x01, 0x01, 0x2C, 0x91, 0x01, 0x04]
        wValue_setup = 0x0001
        
        try:
            result_setup = self.device.ctrl_transfer(bmRequestType_setup, bRequest_setup, wValue_setup, 0x0000, data_to_send_setup)
            print("Setup control transfer result for 15W:", result_setup)
            return True
        except usb.core.USBError as e:
            print(f"USBError (15W): {e}")
            return False

    def set_emulate_charge_27w(self, watts):
        if self.device is None:
            print("Device not found")
            return False
        
        bmRequestType_setup = 0x40
        bRequest_setup = 0xEE

        data_to_send_setup = [0x01, 0x02, 0x2C, 0x91, 0x01, 0x04, 0xB1, 0xD0, 0x02, 0x00]
        wValue_setup = 0x0002
        
        try:
            result_setup = self.device.ctrl_transfer(bmRequestType_setup, bRequest_setup, wValue_setup, 0x0000, data_to_send_setup)
            print("Setup control transfer result for 27W:", result_setup)
            return True
        except usb.core.USBError as e:
            print(f"USBError (27W): {e}")
            return False
    
    def set_emulate_charge_45w(self, watts):
        if self.device is None:
            print("Device not found")
            return False
        
        bmRequestType_setup = 0x40
        bRequest_setup = 0xEE

        data_to_send_setup = [0x01, 0x03, 0x2C, 0x91, 0x01, 0x04, 0x02C, 0xD1, 0x02, 0x00, 0x2C, 0xB1, 0x04, 0x00]
        wValue_setup = 0x0003
        
        try:
            result_setup = self.device.ctrl_transfer(bmRequestType_setup, bRequest_setup, wValue_setup, 0x0000, data_to_send_setup)
            print("Setup control transfer result for 45W:", result_setup)
            return True
        except usb.core.USBError as e:
            print(f"USBError (45W): {e}")
            return False

def set_charge(watts):
    VENDOR_ID = 0x045e  # Replace with your vendor ID
    PRODUCT_ID = 0x078f  # Replace with your product ID

    controller = ChargeController(VENDOR_ID, PRODUCT_ID)
    if controller.find_device():
        if watts <= 15:
            controller.set_emulate_charge_15w(watts)
        elif watts <= 27:
            controller.set_emulate_charge_27w(watts)
        elif watts <= 45:
            controller.set_emulate_charge_45w(watts)
        else:
            print("Invalid wattage specified")
    else:
        print("Device not found")
