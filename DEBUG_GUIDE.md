# Debug Guide - DMX Controller

## Logging System

### Log Files Location
All log files are stored in the `logs/` directory with timestamped filenames:
```
logs/dmx_controller_20251018_153045.log
```

### Log Levels
- **DEBUG**: Detailed information, including all channel changes
- **INFO**: General information about operations
- **WARNING**: Warning messages for non-critical issues
- **ERROR**: Error messages for failures

### Log Format
```
2025-10-18 15:30:45,123 - __main__ - INFO - Starting DMX Controller v1.0.0
2025-10-18 15:30:47,456 - __main__ - DEBUG - Channel 1: 0 -> 128
```

### Log Retention
- Automatically keeps only the last 10 log files
- Older logs are deleted automatically on startup

## Debug Mode

### Enabling Debug Mode
1. Go to the **Debug & Logs** tab
2. Check the **Debug Mode (Verbose Logging)** checkbox
3. Debug mode setting is saved automatically

### What Debug Mode Logs
- Every channel value change
- DMX frame transmission details (every 1000 frames)
- Frame timing information
- Connection details
- All user actions

### Example Debug Output
```
2025-10-18 15:31:15,789 - __main__ - DEBUG - Channel 6: 0 -> 255
2025-10-18 15:31:20,123 - __main__ - DEBUG - Frames sent: 1000, Last frame time: 1.23ms
```

## Channel Monitor

### Real-time Display
The channel monitor shows current values of all 9 DMX channels:
```
Active Channels:
Ch1:  0 Ch2:  0 Ch3:  0 Ch4:  0 Ch5:  0
Ch6:255 Ch7:128 Ch8:  0 Ch9:  0
```

### Update Rate
- Updates every 100ms
- Only active when connected to device

## Statistics Panel

### Metrics Tracked
1. **Frames**: Total number of DMX frames sent
   - Increments with each successful transmission
   - Resets on disconnect

2. **Errors**: Number of transmission errors
   - Indicates communication problems
   - Should normally be 0

3. **FPS**: Frames per second
   - Target: ~40 FPS
   - Lower values may indicate USB issues

### Interpreting Statistics

#### Good Performance
```
Frames: 12,450
Errors: 0
FPS: 39.8
```

#### Issues Detected
```
Frames: 2,100
Errors: 45
FPS: 15.2
```
**Possible causes:**
- USB cable quality
- System resource constraints
- Driver issues

## Log Export

### Exporting Logs
1. Go to **Debug & Logs** tab
2. Click **Export Logs**
3. File saved as: `logs/export_YYYYMMDD_HHMMSS.txt`

### What Gets Exported
- Last 100 lines displayed in the log viewer
- Includes timestamps and log levels
- Can be shared for troubleshooting

## Common Log Messages

### Normal Operation
```
INFO - Starting DMX Controller v1.0.0
INFO - Attempting to connect to COM3
INFO - Successfully connected to COM3
DEBUG - Port settings: 250000 8N2
INFO - All channels off command
INFO - User initiated disconnection
INFO - Session stats - Frames sent: 5432, Errors: 0
```

### Error Conditions
```
ERROR - Connection error: [Errno 2] could not open port 'COM3'
WARNING - Connection attempt without port selection
ERROR - Send error: [Errno 5] Access is denied
WARNING - Invalid channel/value: Ch10=256
```

## Troubleshooting with Logs

### Connection Issues
**Look for:**
```
ERROR - Connection error: [Errno 2] could not open port
```
**Solution:** Check port selection, USB cable, and drivers

### Frame Transmission Errors
**Look for:**
```
ERROR - Send error: [Errno 5] Access is denied
```
**Solution:** Close other applications using the port

### Performance Issues
**Look for:**
```
DEBUG - Frames sent: 1000, Last frame time: 15.67ms
```
**Normal:** < 5ms
**Issue:** > 10ms indicates performance problems

## Configuration File

### Location
`config.json` in the application directory

### Contents
```json
{
  "debug_mode": true,
  "last_port": "COM3"
}
```

### Auto-save Triggers
- Debug mode toggle
- Successful connection
- Application close

## Command Line Debugging

### Running with Console Output
```bash
python dmx_controller.py
```
Logs appear both in file and console window.

### Viewing Live Logs (Windows)
```powershell
Get-Content logs\dmx_controller_*.log -Wait -Tail 50
```

### Viewing Live Logs (Linux/Mac)
```bash
tail -f logs/dmx_controller_*.log
```

## Performance Monitoring

### Expected Values
- **Frame Time:** 0.5-2ms
- **FPS:** 38-42
- **Errors:** 0

### Warning Signs
- Frame time > 10ms
- FPS < 30
- Errors > 0

### Optimization Tips
1. Close other serial/USB applications
2. Use high-quality USB cable
3. Connect to USB 2.0/3.0 port (not hub)
4. Disable power saving on USB ports

## Advanced Debugging

### Python Logger Configuration
The application uses Python's `logging` module:
- Root logger level can be changed
- Multiple handlers (file + console)
- Format customizable in code

### Adding Custom Debug Points
Edit `dmx_controller.py` and add:
```python
self.logger.debug(f"Custom debug message: {variable}")
```

### Enabling All Debug Output
Set environment variable before running:
```bash
set PYTHONUNBUFFERED=1
python dmx_controller.py
```

## Best Practices

1. **Enable debug mode** when troubleshooting
2. **Check statistics** regularly during operation
3. **Export logs** before closing if issues occurred
4. **Review logs** after unexpected behavior
5. **Keep last 10 sessions** for historical reference

## Support Information

When reporting issues, include:
1. Exported log file
2. Screenshots of statistics panel
3. Channel monitor values when issue occurred
4. Your UDMX device model
5. Operating system version

## Quick Reference

| Feature | Location | Purpose |
|---------|----------|---------|
| Debug Mode | Debug & Logs tab | Enable verbose logging |
| Channel Monitor | Debug & Logs tab | Real-time channel values |
| Log Display | Debug & Logs tab | View recent logs |
| Statistics | Controls tab | Performance metrics |
| Export Logs | Debug & Logs tab | Save logs to file |
| Clear Logs | Debug & Logs tab | Clear display only |
| Refresh | Debug & Logs tab | Update log display |

