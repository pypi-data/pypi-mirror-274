##############################################################################
# 
# Module: reconnect.py
#
# Description:
#     Disconnect and reconnect the Type-C MUTT one time with
#     optional wait times (in ms), X before disconnect, and Y before reconnect.
#
# Author:
#     Vinay N, MCCI Corporation May 2024
#
#############################################################################
import usb.core
import usb.util

class ReconnectController:
    def __init__(self, vendor_id, product_id):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None

    def find_device(self):
        self.device = usb.core.find(idVendor=self.vendor_id, idProduct=self.product_id)
        return self.device is not None

    def disconnect_and_reconnect(self, delay_disconnect_ms, delay_reconnect_ms):
        if self.device is None:
            print("Device not found")
            return False
        
        # Set configuration
        self.device.set_configuration()
        
        # Setup packet details
        bmRequestType = 0x40  # Request type: Vendor, Host-to-device, Device-to-interface
        bRequest = 0x10       # Request code
        wLength = 0x00

        # Send control transfer for disconnect
        self.device.ctrl_transfer(bmRequestType, bRequest, delay_disconnect_ms, delay_reconnect_ms, wLength)
        print(f"Device disconnected for {delay_disconnect_ms}ms and reconnected for {delay_reconnect_ms}ms")
        return True

def reconnect_status(delay_disconnect_ms, delay_reconnect_ms):
    VENDOR_ID = 0x045e  # Replace with your vendor ID
    PRODUCT_ID = 0x078f  # Replace with your product ID

    controller = ReconnectController(VENDOR_ID, PRODUCT_ID)
    if controller.find_device():
        controller.disconnect_and_reconnect(delay_disconnect_ms, delay_reconnect_ms)
