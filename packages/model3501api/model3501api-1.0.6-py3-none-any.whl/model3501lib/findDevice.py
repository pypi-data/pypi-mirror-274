##############################################################################
# 
# Module: findDevice.py
#
# Description:
#      List Type-C MUTTs by index
#
# Author:
#     Vinay N, MCCI Corporation May 2024
#
#############################################################################

import usb.core
import usb.util

class FindDeviceController:
    def __init__(self, vendor_id, product_id):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
    
    def find_device(self):
        devices_info = []

        # Find all USB devices connected to the system
        devices = usb.core.find(find_all=True)
        
        # Iterate through each device and check if it matches the target VID and PID
        for device in devices:
            # Check if the device has both VID and PID attributes
            if device.idVendor is not None and device.idProduct is not None:
                # Check if the device matches the target VID and PID
                if device.idVendor == self.vendor_id and device.idProduct == self.product_id:
                    # Perform control transfer to retrieve device descriptor
                    try:
                        bmRequestType = 0x40  # Direction: IN
                        bRequest = 0x14        # GET_DESCRIPTOR request
                        wValue = 0x0000
                        wIndex = 0x0000
                        wLength = 0x0000
                        
                        result = device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)
                        if result == 0:
                            speed = "High speed"
                        else:
                            speed = "Super speed"
                        
                        # Retrieve device information
                        manufacturer = usb.util.get_string(device, device.iManufacturer)
                        product = usb.util.get_string(device, device.iProduct)
                        firmware_version = device.bcdDevice

                        # Create a dictionary with device information including USB speed
                        device_info = {
                            'vendor_id': hex(self.vendor_id),
                            'product_id': hex(self.product_id),
                            'manufacturer': manufacturer,
                            'product': product,
                            'firmware_version': firmware_version,
                            'speed': speed
                        }
                        devices_info.append(device_info)
                    except usb.core.USBError as e:
                        print(f"Failed to retrieve device descriptor: {e}")
        
        return devices_info

def find_device_status():
    VENDOR_ID = 0x045e
    PRODUCT_ID = 0x078f
    controller = FindDeviceController(VENDOR_ID, PRODUCT_ID)
    devices = controller.find_device()

    # Print the device information directly
    if devices:
        for device in devices:
            print(f"Vendor ID: {device['vendor_id']}, Product ID: {device['product_id']}, Manufacturer: {device['manufacturer']}, Product: {device['product']}, Firmware Version: {device['firmware_version']}, Speed: {device['speed']}")
    else:
        print("No matching devices found.")

# Example usage
find_device_status()
