# pdcaptive_cables.py
import usb.core

class PDCaptiveCablesController:
    def __init__(self, vendor_id, product_id):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
    
    def find_device(self):
        self.device = usb.core.find(idVendor=self.vendor_id, idProduct=self.product_id)
        return self.device is not None
    
    def pd_captive_cables(self):
        if self.device is None:
            print("Device not found")
            return False
        
        # Control transfer parameters for PdCaptiveCable
        bmRequestType = 0x40  # Request type: Vendor, Host-to-device, Device-to-interface
        bRequest = 0xE9       # Request code for PdCaptiveCable command
        wValue = 0x0000       # Value
        wIndex = 0x0000       # Index
        wLength = 0x0000      # Length

        # Send control transfer for PdCaptiveCable command
        result = self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)
        print("result-pd-captive-cables:", result)
        if result == 0:
            print("Switched PD support to captive cable successfully")
        else:
            print("Failed to switch PD support to captive cable")
        return result == 0

def pd_captive_cables_status():
    VENDOR_ID = 0x045e  # Replace with your vendor ID
    PRODUCT_ID = 0x078f  # Replace with your product ID

    controller = PDCaptiveCablesController(VENDOR_ID, PRODUCT_ID)
    if controller.find_device():
        controller.pd_captive_cables()
