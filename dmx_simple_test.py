"""
Simple test script for DMX device without GUI
"""
import serial
import serial.tools.list_ports
import time


def list_ports():
    """List available serial ports"""
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found!")
        return None
    
    print("\nAvailable ports:")
    for i, port in enumerate(ports):
        print(f"{i}: {port.device} - {port.description}")
    
    return ports


def send_dmx_frame(serial_port, dmx_data):
    """Send a DMX frame"""
    try:
        # DMX break
        serial_port.break_condition = True
        time.sleep(0.000088)
        serial_port.break_condition = False
        
        # Mark after break
        time.sleep(0.000008)
        
        # Start code + data
        serial_port.write(bytes([0]) + bytes(dmx_data))
        
    except Exception as e:
        print(f"Error sending DMX: {e}")


def main():
    print("=== DMX UDMX Test ===")
    
    ports = list_ports()
    if not ports:
        return
    
    # Select port
    port_idx = int(input("\nSelect port number: "))
    selected_port = ports[port_idx].device
    
    print(f"\nConnecting to {selected_port}...")
    
    try:
        # Connect to UDMX
        ser = serial.Serial(
            port=selected_port,
            baudrate=250000,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_TWO,
            parity=serial.PARITY_NONE,
            timeout=1
        )
        
        print("Connected successfully!")
        
        # Initialize DMX data (512 channels)
        dmx_data = [0] * 512
        
        print("\nTest sequence starting...")
        print("Channel 6 (Dimming) will fade from 0 to 255")
        
        # Test: Fade in dimming
        for brightness in range(0, 256, 5):
            dmx_data[5] = brightness  # Channel 6 (index 5)
            send_dmx_frame(ser, dmx_data)
            print(f"Brightness: {brightness}", end="\r")
            time.sleep(0.05)
        
        print("\n\nTest complete! Holding at full brightness for 3 seconds...")
        for _ in range(120):  # Hold for 3 seconds at ~40Hz
            send_dmx_frame(ser, dmx_data)
            time.sleep(0.025)
        
        # All off
        print("Turning off...")
        dmx_data = [0] * 512
        for _ in range(40):
            send_dmx_frame(ser, dmx_data)
            time.sleep(0.025)
        
        ser.close()
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

