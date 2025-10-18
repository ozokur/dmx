"""
UDMX Device Test Script
Tests USB connection to UDMX devices
"""
import usb.core
import usb.util

# UDMX Device IDs
UDMX_DEVICES = [
    {'vendor': 0x16C0, 'product': 0x05DC, 'name': 'Anyma uDMX'},
    {'vendor': 0x03EB, 'product': 0x8888, 'name': 'DMXControl uDMX'},
]

def find_all_usb_devices():
    """List all USB devices"""
    print("=== All USB Devices ===")
    devices = usb.core.find(find_all=True)
    for dev in devices:
        print(f"VID:{dev.idVendor:04X} PID:{dev.idProduct:04X} - {usb.util.get_string(dev, dev.iProduct) if dev.iProduct else 'Unknown'}")
    print()

def test_udmx_connection():
    """Test UDMX device connection"""
    print("=== UDMX Device Test ===\n")
    
    found_devices = []
    
    for device_info in UDMX_DEVICES:
        print(f"Searching for {device_info['name']}...")
        print(f"  VID: 0x{device_info['vendor']:04X}")
        print(f"  PID: 0x{device_info['product']:04X}")
        
        dev = usb.core.find(idVendor=device_info['vendor'], idProduct=device_info['product'])
        
        if dev is not None:
            print(f"  ✅ Found!")
            found_devices.append((dev, device_info))
            
            try:
                # Get device information
                print(f"  Manufacturer: {usb.util.get_string(dev, dev.iManufacturer)}")
                print(f"  Product: {usb.util.get_string(dev, dev.iProduct)}")
                print(f"  Serial: {usb.util.get_string(dev, dev.iSerialNumber)}")
            except:
                print("  (Could not read device strings)")
            
            print(f"  Bus: {dev.bus}")
            print(f"  Address: {dev.address}")
        else:
            print(f"  ❌ Not found")
        
        print()
    
    if not found_devices:
        print("❌ No UDMX devices found!\n")
        print("Troubleshooting:")
        print("1. Check USB cable connection")
        print("2. Install libusb drivers (see INSTALL_DRIVERS.md)")
        print("3. On Windows: Use Zadig to install libusb-win32 driver")
        print("4. On Linux: Check udev rules and permissions")
        print("5. Try running as Administrator/root")
        return False
    
    print(f"✅ Found {len(found_devices)} UDMX device(s)!")
    print("\nTesting communication...\n")
    
    for dev, device_info in found_devices:
        print(f"Testing {device_info['name']}...")
        
        try:
            # Try to detach kernel driver
            try:
                if dev.is_kernel_driver_active(0):
                    print("  Detaching kernel driver...")
                    dev.detach_kernel_driver(0)
            except:
                pass
            
            # Set configuration
            try:
                dev.set_configuration()
                print("  ✅ Configuration set")
            except:
                print("  ⚠️  Could not set configuration (may be OK)")
            
            # Try to send a test packet (channel 1 = value 128)
            try:
                dev.ctrl_transfer(0x40, 0x01, 128, 0, [])
                print("  ✅ Test data sent successfully!")
                print("  (Check if your DMX device responded)")
            except Exception as e:
                print(f"  ⚠️  Could not send test data: {e}")
            
            print("  ✅ Device is ready to use!")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            print("  This device may need driver installation or permissions")
        
        print()
    
    return True

def main():
    print("=" * 50)
    print("UDMX Device Connection Test")
    print("=" * 50)
    print()
    
    try:
        # Test for UDMX devices
        success = test_udmx_connection()
        
        if not success:
            print("\n" + "=" * 50)
            print("Showing all USB devices for reference:")
            print("=" * 50)
            print()
            try:
                find_all_usb_devices()
            except:
                print("Could not list USB devices")
        
        print("=" * 50)
        print("Test complete!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("\nPossible causes:")
        print("1. libusb not installed")
        print("2. pyusb not installed (pip install pyusb)")
        print("3. No USB access permissions")
        print("\nSee INSTALL_DRIVERS.md for installation instructions")

if __name__ == "__main__":
    main()

