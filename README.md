# DMX Controller for UDMX

A Python-based DMX controller application for controlling DMX devices via UDMX interface.

**Developed by hilminoe**

> 🇹🇷 **Türkçe Kullanıcılar**: [HIZLI_BASLANGIC.md](HIZLI_BASLANGIC.md) dosyasına bakın.

## Features

- **9-Channel DMX Control** for moving head lights or similar fixtures
- **Graphical User Interface** with real-time sliders
- **Serial Communication** with UDMX device
- **Quick Actions** for common operations
- **Comprehensive Logging** with file rotation and retention
- **Debug Mode** with verbose logging and channel monitoring
- **Statistics Tracking** (frames sent, errors, FPS)
- **Configuration Management** with auto-save/load
- **Live Channel Monitor** for real-time value display
- **Log Export** functionality

## DMX Channel Mapping

| Channel | Function | Range | Description |
|---------|----------|-------|-------------|
| 1 | Horizontal Rotation | 0-255 | Pan movement |
| 2 | Vertical Rotation | 0-255 | Tilt movement |
| 3 | Color | 0-139 | Color selection |
|   |       | 140-255 | Automatic color switch (speed increasing) |
| 4 | Gobo | 0-63 | Fixed gobo |
|   |      | 64-127 | Gobo shaking |
|   |      | 128-255 | Automatic gobo switch (speed increasing) |
| 5 | Strobe | 0-255 | Strobe effect speed |
| 6 | Dimming | 0-255 | Brightness control |
| 7 | Rotation Speed | 0-255 | Clockwise/Counter-clockwise rotation |
| 8 | Auto-play Mode | 0-255 | Automatic program selection |
| 9 | Reposition | 250-255 | Reset position (5 seconds) |

## Installation

### 1. Install Python
Python 3.7 or higher required

### 2. Install libusb drivers
**This is critical for UDMX connection!**

See detailed instructions: **[INSTALL_DRIVERS.md](INSTALL_DRIVERS.md)**

**Quick Start:**
- **Windows**: Use [Zadig](https://zadig.akeo.ie/) to install libusb-win32 driver
- **Linux**: `sudo apt-get install libusb-1.0-0-dev` + udev rules
- **macOS**: `brew install libusb`

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Test UDMX connection
```bash
python test_udmx.py
```

## Usage

### GUI Application

Run the main GUI application:
```bash
python dmx_controller.py
```

**Steps:**
1. Connect UDMX device via USB
2. Click "Refresh" to detect devices
3. Select your UDMX device from the dropdown
4. Click "Connect"
5. Use the sliders to control each DMX channel
6. Use quick action buttons for common operations

**Tabs:**
- **Controls**: Main DMX channel controls with sliders
- **Debug & Logs**: Real-time logging, channel monitor, and debug controls
- **Info**: Version information and documentation

### Simple Test Script

For testing without GUI:
```bash
python dmx_simple_test.py
```

This script will:
- List available serial ports
- Connect to your UDMX device
- Run a simple brightness fade test

## Hardware Setup

1. **Install libusb drivers** (see [INSTALL_DRIVERS.md](INSTALL_DRIVERS.md))
2. **Connect UDMX** interface to your computer via USB (directly, not via hub)
3. **Connect DMX device** to UDMX output
4. **Set DMX address** on your fixture to channel 1
5. **Power on** your DMX device
6. **Run test**: `python test_udmx.py`

## UDMX Interface

This application works with UDMX (USB-DMX) interfaces via direct USB connection.

### Supported Devices
- ✅ **Anyma uDMX** (VID:16C0 PID:05DC)
- ✅ **DMXControl uDMX** (VID:03EB PID:8888)
- ✅ Compatible UDMX clones with FTDI FT245RL chip

### Required Drivers

**libusb drivers are REQUIRED!** See [INSTALL_DRIVERS.md](INSTALL_DRIVERS.md) for:
- Windows: Zadig installation guide
- Linux: libusb-dev and udev rules
- macOS: Homebrew installation

## Troubleshooting

### Connection Issues

**"No UDMX devices found":**
- Check USB cable connection
- Install libusb drivers (see [INSTALL_DRIVERS.md](INSTALL_DRIVERS.md))
- Try a different USB port (direct to PC, not via hub)
- Run `python test_udmx.py` to diagnose

**"Failed to connect to UDMX device":**
- **Windows**: Install driver with Zadig (libusb-win32)
- **Windows**: Run as Administrator
- **Linux**: Check udev rules and user permissions
- **Linux**: Add user to `plugdev` group
- Close any other applications using the device

**"Access Denied" or "Permission Denied":**
- **Windows**: Run as Administrator
- **Linux**: Fix udev rules (see INSTALL_DRIVERS.md)
- **Linux**: `sudo usermod -a -G plugdev $USER` then logout/login

### Device Not Responding

1. **Check DMX address** on your fixture
2. **Verify DMX cable** connections
3. **Test with Channel 6** (Dimming) - easiest to see results
4. **Check if device is in DMX mode** (not standalone mode)

### Performance Issues

- Reduce update rate in the code if needed
- Close unnecessary applications
- Check USB cable quality

## Debug Features

### Logging
All operations are logged to files in the `logs/` directory:
- Automatic log rotation
- Retention of last 10 sessions
- Timestamps on all entries
- Error tracking

### Debug Mode
Enable debug mode in the "Debug & Logs" tab for:
- Verbose logging of all channel changes
- Frame transmission details
- Performance metrics
- Real-time channel value monitoring

### Statistics
Track application performance:
- **Frames**: Total DMX frames sent
- **Errors**: Count of transmission errors
- **FPS**: Current frames per second

### Channel Monitor
Real-time display of all 9 channel values in the debug tab.

### Log Export
Export current session logs to a timestamped file.

For detailed debugging information, see [DEBUG_GUIDE.md](DEBUG_GUIDE.md).

## Code Structure

- `dmx_controller.py` - Main GUI application
- `dmx_simple_test.py` - Simple command-line test
- `requirements.txt` - Python dependencies
- `CHANGELOG.md` - Version history and changes
- `DEBUG_GUIDE.md` - Comprehensive debugging guide
- `config.json` - Saved configuration (auto-generated)
- `logs/` - Log files directory (auto-generated)

## Technical Details

- **Version:** 1.3.0
- **Protocol:** USB direct (no serial)
- **Update Rate:** ~40 Hz
- **DMX Universe:** 512 channels
- **USB Control Transfer:** 0x40 (vendor specific)
- **Logging:** File + Console, auto-rotation
- **Config Storage:** JSON format
- **Dependencies:** pyusb, libusb

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## License

MIT License - Feel free to modify and use for your projects.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Safety Notes

⚠️ **Important:**
- Do not look directly into laser or high-intensity lights
- Ensure proper electrical grounding
- Follow manufacturer safety guidelines for your DMX fixtures
- Strobe effects may trigger photosensitive epilepsy