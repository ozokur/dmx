# Changelog

All notable changes to DMX Controller will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-18

### Added
- Initial release of DMX Controller for UDMX
- 9-channel DMX control interface
- Graphical user interface with Tkinter
- Real-time DMX frame transmission (~40 Hz)
- Serial communication with UDMX devices
- Quick action buttons (All Off, Full Brightness, Reposition)
- Comprehensive logging system
  - File logging with automatic rotation
  - Console output
  - Log retention (last 10 sessions)
- Debug mode with verbose logging
- Channel monitoring and visualization
- Statistics tracking (frame count, error count, FPS)
- Configuration saving/loading
- Multi-tab interface
  - Controls tab for DMX channel sliders
  - Debug & Logs tab for monitoring
  - Info tab with documentation
- Log export functionality
- Version information display
- Automatic log cleanup

### Channel Implementation
- Channel 1: Horizontal Rotation (0-255)
- Channel 2: Vertical Rotation (0-255)
- Channel 3: Color selection and auto mode
- Channel 4: Gobo selection with shake and auto mode
- Channel 5: Strobe effect control
- Channel 6: Dimming/brightness control
- Channel 7: Rotation speed control
- Channel 8: Auto-play mode selection
- Channel 9: Reposition function

### Technical Features
- DMX512 protocol implementation
- 250000 baud rate (DMX standard)
- 512 channel universe support
- Thread-safe operation
- Error handling and recovery
- Performance monitoring

### Documentation
- Comprehensive README.md
- Installation guide
- Usage instructions
- Troubleshooting section
- Hardware setup guide
- Channel mapping table

### Testing
- Simple test script (dmx_simple_test.py)
- Port detection and listing
- Brightness fade test

## [1.1.0] - 2025-10-18

### Changed
- **BREAKING**: Switched from Serial (COM port) to USB direct connection
- Now uses PyUSB instead of PySerial
- Direct UDMX device communication via USB control transfers
- Better compatibility with UDMX hardware

### Added
- Auto-detection of UDMX devices (Anyma uDMX, DMXControl uDMX)
- USB device information display
- Better error messages for USB connection issues
- `INSTALL_DRIVERS.md` - Comprehensive driver installation guide
- `test_udmx.py` - USB connection test script
- Support for multiple UDMX device types

### Fixed
- COM port connection errors on Windows
- Better USB device handling
- Improved error recovery

### Technical Changes
- Replaced `pyserial` with `pyusb`
- USB control transfers (bmRequestType 0x40)
- Kernel driver detachment for Linux compatibility
- Device cleanup with proper resource disposal

## [Unreleased]

### Planned Features
- Scene saving and recall
- DMX sequence recording/playback
- MIDI control integration
- Network/Art-Net support
- Multi-fixture support
- Preset library
- Timeline editor
- Effect generator
- Mobile app control
- Web interface

