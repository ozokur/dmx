"""
DMX Controller for UDMX Interface
Controls a DMX device with 9 channels
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import logging
from datetime import datetime
import os
import json
import usb.core
import usb.util
import pygame

__version__ = "1.2.0"
__author__ = "DMX Controller"
__date__ = "2025-10-18"

# UDMX Device IDs
UDMX_DEVICES = [
    {'vendor': 0x16C0, 'product': 0x05DC, 'name': 'Anyma uDMX'},
    {'vendor': 0x03EB, 'product': 0x8888, 'name': 'DMXControl uDMX'},
]


class DMXController:
    def __init__(self, logger=None):
        self.dmx_data = [0] * 512  # DMX universe (512 channels)
        self.usb_device = None
        self.running = False
        self.logger = logger or logging.getLogger(__name__)
        self.frame_count = 0
        self.error_count = 0
        self.last_send_time = 0
        self.device_info = None
        
        self.logger.info("DMX Controller initialized")
        self.logger.debug(f"DMX Universe size: 512 channels")
    
    def find_udmx_devices(self):
        """Find all connected UDMX devices"""
        devices = []
        for device_info in UDMX_DEVICES:
            dev = usb.core.find(idVendor=device_info['vendor'], idProduct=device_info['product'])
            if dev is not None:
                devices.append({
                    'device': dev,
                    'name': device_info['name'],
                    'vendor': device_info['vendor'],
                    'product': device_info['product'],
                    'description': f"{device_info['name']} (VID:{device_info['vendor']:04X} PID:{device_info['product']:04X})"
                })
                self.logger.debug(f"Found UDMX device: {device_info['name']}")
        return devices
        
    def connect(self, device_index=0):
        """Connect to UDMX device via USB"""
        try:
            devices = self.find_udmx_devices()
            
            if not devices:
                self.logger.error("No UDMX devices found")
                return False
            
            if device_index >= len(devices):
                device_index = 0
            
            device_info = devices[device_index]
            self.usb_device = device_info['device']
            self.device_info = device_info
            
            self.logger.info(f"Attempting to connect to {device_info['name']}")
            
            # Try to detach kernel driver if active
            try:
                if self.usb_device.is_kernel_driver_active(0):
                    self.logger.debug("Detaching kernel driver")
                    self.usb_device.detach_kernel_driver(0)
            except:
                pass  # Not all systems need this
            
            # Set configuration
            try:
                self.usb_device.set_configuration()
            except:
                pass  # May already be configured
            
            self.running = True
            self.frame_count = 0
            self.error_count = 0
            
            self.logger.info(f"Successfully connected to {device_info['name']}")
            self.logger.debug(f"Device: VID:{device_info['vendor']:04X} PID:{device_info['product']:04X}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from UDMX device"""
        self.logger.info("Disconnecting from device")
        self.logger.info(f"Session stats - Frames sent: {self.frame_count}, Errors: {self.error_count}")
        self.running = False
        
        if self.usb_device:
            try:
                usb.util.dispose_resources(self.usb_device)
                self.logger.info("Device disconnected successfully")
            except:
                pass
            self.usb_device = None
    
    def set_channel(self, channel, value):
        """Set a DMX channel value (1-512, value 0-255)"""
        if 1 <= channel <= 512 and 0 <= value <= 255:
            old_value = self.dmx_data[channel - 1]
            self.dmx_data[channel - 1] = int(value)
            if old_value != int(value):
                self.logger.debug(f"Channel {channel}: {old_value} -> {value}")
        else:
            self.logger.warning(f"Invalid channel/value: Ch{channel}={value}")
    
    def send_dmx_frame(self):
        """Send DMX frame to UDMX device via USB"""
        if not self.usb_device:
            return
        
        try:
            start_time = time.time()
            
            # UDMX specific USB control transfer
            # Request type: 0x40 = Host to device, Vendor specific, Device recipient
            # Request: 0x02 = Set single channel or 0x01 = Set all channels
            # We'll send channels in chunks for better compatibility
            
            # Method 1: Send all channels at once (if supported)
            try:
                # Some UDMX devices support sending all 512 channels
                # Control transfer: bmRequestType, bRequest, wValue, wIndex, data
                self.usb_device.ctrl_transfer(0x40, 0x02, 512, 0, self.dmx_data[:512])
            except:
                # Method 2: Send in smaller chunks (more compatible)
                # Send first 9 channels (our active channels)
                for i in range(9):
                    self.usb_device.ctrl_transfer(0x40, 0x01, self.dmx_data[i], i, [])
            
            self.frame_count += 1
            self.last_send_time = time.time() - start_time
            
            if self.frame_count % 1000 == 0:
                self.logger.debug(f"Frames sent: {self.frame_count}, Last frame time: {self.last_send_time*1000:.2f}ms")
            
        except usb.core.USBError as e:
            self.error_count += 1
            if self.error_count % 10 == 1:  # Log every 10th error to avoid spam
                self.logger.error(f"USB Send error: {e}")
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Send error: {e}")


class DMXControllerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"DMX Controller - UDMX v{__version__}")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # Setup logging
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Starting DMX Controller v{__version__}")
        
        self.controller = DMXController(logger=self.logger)
        self.update_thread = None
        self.running = False
        self.debug_mode = tk.BooleanVar(value=False)
        self.stats_enabled = tk.BooleanVar(value=True)
        
        # Gamepad support
        self.gamepad = None
        self.gamepad_thread = None
        self.gamepad_enabled = tk.BooleanVar(value=False)
        self.init_gamepad()
        
        self.create_ui()
        self.load_config()
        
    def setup_logging(self):
        """Setup logging configuration"""
        # Create logs directory
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Create log filename with timestamp
        log_filename = f"logs/dmx_controller_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Configure root logger
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        # Keep only last 10 log files
        self.cleanup_old_logs()
    
    def cleanup_old_logs(self):
        """Keep only the 10 most recent log files"""
        try:
            log_files = sorted([f for f in os.listdir('logs') if f.endswith('.log')])
            if len(log_files) > 10:
                for old_log in log_files[:-10]:
                    os.remove(os.path.join('logs', old_log))
        except Exception as e:
            print(f"Error cleaning up logs: {e}")
    
    def init_gamepad(self):
        """Initialize gamepad support"""
        try:
            pygame.init()
            pygame.joystick.init()
            
            if pygame.joystick.get_count() > 0:
                self.gamepad = pygame.joystick.Joystick(0)
                self.gamepad.init()
                gamepad_name = self.gamepad.get_name()
                self.logger.info(f"Gamepad detected: {gamepad_name}")
                self.logger.info(f"Axes: {self.gamepad.get_numaxes()}, Buttons: {self.gamepad.get_numbuttons()}")
            else:
                self.logger.warning("No gamepad detected")
                self.gamepad = None
        except Exception as e:
            self.logger.error(f"Gamepad initialization error: {e}")
            self.gamepad = None
    
    def load_config(self):
        """Load saved configuration"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    self.debug_mode.set(config.get('debug_mode', False))
                    self.logger.info("Configuration loaded")
        except Exception as e:
            self.logger.warning(f"Could not load config: {e}")
    
    def save_config(self):
        """Save configuration"""
        try:
            config = {
                'debug_mode': self.debug_mode.get(),
                'last_port': self.port_combo.get()
            }
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            self.logger.info("Configuration saved")
        except Exception as e:
            self.logger.error(f"Could not save config: {e}")
    
    def create_ui(self):
        """Create the user interface"""
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Main control tab
        main_tab = ttk.Frame(notebook)
        notebook.add(main_tab, text="Controls")
        
        # Debug tab
        debug_tab = ttk.Frame(notebook)
        notebook.add(debug_tab, text="Debug & Logs")
        
        # Info tab
        info_tab = ttk.Frame(notebook)
        notebook.add(info_tab, text="Info")
        
        self.create_main_controls(main_tab)
        self.create_debug_tab(debug_tab)
        self.create_info_tab(info_tab)
    
    def create_main_controls(self, parent):
        """Create main control interface"""
        
        # Connection Frame
        conn_frame = ttk.LabelFrame(parent, text="Connection", padding=10)
        conn_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=0, padx=5)
        self.port_combo = ttk.Combobox(conn_frame, width=20, state="readonly")
        self.port_combo.grid(row=0, column=1, padx=5)
        self.refresh_ports()
        
        ttk.Button(conn_frame, text="Refresh", command=self.refresh_ports).grid(row=0, column=2, padx=5)
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=3, padx=5)
        
        self.status_label = ttk.Label(conn_frame, text="Status: Disconnected", foreground="red")
        self.status_label.grid(row=0, column=4, padx=10)
        
        # Stats Frame
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding=5)
        stats_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        self.frames_label = ttk.Label(stats_frame, text="Frames: 0")
        self.frames_label.grid(row=0, column=0, padx=10)
        
        self.errors_label = ttk.Label(stats_frame, text="Errors: 0")
        self.errors_label.grid(row=0, column=1, padx=10)
        
        self.fps_label = ttk.Label(stats_frame, text="FPS: 0")
        self.fps_label.grid(row=0, column=2, padx=10)
        
        # Control Frame
        control_frame = ttk.Frame(parent, padding=10)
        control_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        # Channel 1: Horizontal Rotation
        self.create_channel_control(control_frame, 0, "Channel 1: Horizontal Rotation", 1, 0, 255)
        
        # Channel 2: Vertical Rotation
        self.create_channel_control(control_frame, 1, "Channel 2: Vertical Rotation", 2, 0, 255)
        
        # Channel 3: Color
        row = 2
        ttk.Label(control_frame, text="Channel 3: Color", font=("Arial", 10, "bold")).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(10, 5))
        self.ch3_var = tk.IntVar(value=0)
        self.ch3_scale = ttk.Scale(control_frame, from_=0, to=255, orient="horizontal", 
                                   variable=self.ch3_var, command=lambda v: self.update_channel(3))
        self.ch3_scale.grid(row=row+1, column=0, sticky="ew", padx=5)
        self.ch3_label = ttk.Label(control_frame, text="0")
        self.ch3_label.grid(row=row+1, column=1, padx=5)
        ttk.Label(control_frame, text="0-139: Color selection | 140-255: Auto color switch", 
                 font=("Arial", 8)).grid(row=row+2, column=0, columnspan=2, sticky="w", padx=5)
        
        # Channel 4: Gobo
        row = 5
        ttk.Label(control_frame, text="Channel 4: Gobo", font=("Arial", 10, "bold")).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(10, 5))
        self.ch4_var = tk.IntVar(value=0)
        self.ch4_scale = ttk.Scale(control_frame, from_=0, to=255, orient="horizontal", 
                                   variable=self.ch4_var, command=lambda v: self.update_channel(4))
        self.ch4_scale.grid(row=row+1, column=0, sticky="ew", padx=5)
        self.ch4_label = ttk.Label(control_frame, text="0")
        self.ch4_label.grid(row=row+1, column=1, padx=5)
        ttk.Label(control_frame, text="0-63: Fixed | 64-127: Shaking | 128-255: Auto switch", 
                 font=("Arial", 8)).grid(row=row+2, column=0, columnspan=2, sticky="w", padx=5)
        
        # Channel 5: Strobe
        self.create_channel_control(control_frame, 8, "Channel 5: Strobe", 5, 0, 255)
        
        # Channel 6: Dimming
        self.create_channel_control(control_frame, 9, "Channel 6: Dimming", 6, 0, 255)
        
        # Channel 7: Rotation Speed
        row = 12
        ttk.Label(control_frame, text="Channel 7: Rotation Speed", font=("Arial", 10, "bold")).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(10, 5))
        self.ch7_var = tk.IntVar(value=0)
        self.ch7_scale = ttk.Scale(control_frame, from_=0, to=255, orient="horizontal", 
                                   variable=self.ch7_var, command=lambda v: self.update_channel(7))
        self.ch7_scale.grid(row=row+1, column=0, sticky="ew", padx=5)
        self.ch7_label = ttk.Label(control_frame, text="0")
        self.ch7_label.grid(row=row+1, column=1, padx=5)
        ttk.Label(control_frame, text="0-255: Up=Clockwise | Down=Reverse", 
                 font=("Arial", 8)).grid(row=row+2, column=0, columnspan=2, sticky="w", padx=5)
        
        # Channel 8: Auto-play Mode
        self.create_channel_control(control_frame, 15, "Channel 8: Auto-play Mode", 8, 0, 255)
        
        # Channel 9: Reposition
        row = 18
        ttk.Label(control_frame, text="Channel 9: Reposition", font=("Arial", 10, "bold")).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(10, 5))
        self.ch9_var = tk.IntVar(value=0)
        self.ch9_scale = ttk.Scale(control_frame, from_=0, to=255, orient="horizontal", 
                                   variable=self.ch9_var, command=lambda v: self.update_channel(9))
        self.ch9_scale.grid(row=row+1, column=0, sticky="ew", padx=5)
        self.ch9_label = ttk.Label(control_frame, text="0")
        self.ch9_label.grid(row=row+1, column=1, padx=5)
        ttk.Label(control_frame, text="250-255: Reposition (5 seconds)", 
                 font=("Arial", 8)).grid(row=row+2, column=0, columnspan=2, sticky="w", padx=5)
        
        # Quick Actions
        action_frame = ttk.LabelFrame(parent, text="Quick Actions", padding=10)
        action_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        ttk.Button(action_frame, text="All Off", command=self.all_off).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Full Brightness", command=self.full_brightness).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Reposition", command=self.reposition).pack(side="left", padx=5)
        
        # Gamepad Control
        gamepad_frame = ttk.LabelFrame(parent, text="🎮 Gamepad Control", padding=10)
        gamepad_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        if self.gamepad:
            gamepad_info = ttk.Label(gamepad_frame, text=f"✅ {self.gamepad.get_name()} detected", foreground="green")
            gamepad_info.pack(side="left", padx=5)
            
            ttk.Checkbutton(gamepad_frame, text="Enable Pan/Tilt Control (Left Stick)", 
                           variable=self.gamepad_enabled, command=self.toggle_gamepad).pack(side="left", padx=5)
            
            self.gamepad_status = ttk.Label(gamepad_frame, text="Status: Disabled", foreground="gray")
            self.gamepad_status.pack(side="left", padx=10)
        else:
            ttk.Label(gamepad_frame, text="❌ No gamepad detected", foreground="red").pack(side="left", padx=5)
            ttk.Button(gamepad_frame, text="Refresh", command=self.refresh_gamepad).pack(side="left", padx=5)
        
        # Configure grid weights
        control_frame.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
    
    def create_debug_tab(self, parent):
        """Create debug and logging interface"""
        
        # Debug controls
        control_frame = ttk.LabelFrame(parent, text="Debug Controls", padding=10)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Checkbutton(control_frame, text="Debug Mode (Verbose Logging)", 
                       variable=self.debug_mode, command=self.toggle_debug).pack(side="left", padx=5)
        
        ttk.Button(control_frame, text="Clear Logs", command=self.clear_log_display).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Export Logs", command=self.export_logs).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Refresh", command=self.update_log_display).pack(side="left", padx=5)
        
        # Channel monitor
        monitor_frame = ttk.LabelFrame(parent, text="Channel Monitor", padding=10)
        monitor_frame.pack(fill="x", padx=10, pady=5)
        
        self.channel_display = tk.Text(monitor_frame, height=5, width=80, font=("Courier", 9))
        self.channel_display.pack(fill="x", padx=5, pady=5)
        
        # Log display
        log_frame = ttk.LabelFrame(parent, text="Application Logs", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_display = scrolledtext.ScrolledText(log_frame, height=20, width=80, 
                                                     font=("Courier", 9), wrap=tk.WORD)
        self.log_display.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Start log update timer
        self.update_log_display()
        self.update_channel_monitor()
    
    def create_info_tab(self, parent):
        """Create information tab"""
        
        info_frame = ttk.Frame(parent, padding=20)
        info_frame.pack(fill="both", expand=True)
        
        # Version info
        version_text = f"""
DMX Controller for UDMX
Version: {__version__}
Date: {__date__}
Author: {__author__}

═══════════════════════════════════════

FEATURES:
• 9-Channel DMX control
• Real-time updates (~40 Hz)
• Debug logging and monitoring
• Statistics tracking
• Configuration saving

CHANNEL MAPPING:
1. Horizontal Rotation (0-255)
2. Vertical Rotation (0-255)
3. Color (0-139: Selection, 140-255: Auto)
4. Gobo (0-63: Fixed, 64-127: Shake, 128-255: Auto)
5. Strobe (0-255)
6. Dimming (0-255)
7. Rotation Speed (0-255)
8. Auto-play Mode (0-255)
9. Reposition (250-255: 5s reset)

TECHNICAL DETAILS:
• Protocol: DMX512
• Baud Rate: 250000
• Update Rate: ~40 Hz
• Universe Size: 512 channels

LOG FILES:
Located in: ./logs/
Retention: Last 10 sessions

═══════════════════════════════════════
"""
        
        info_label = tk.Label(info_frame, text=version_text, justify="left", 
                            font=("Courier", 10), bg="white", relief="solid", 
                            borderwidth=1, padx=20, pady=20)
        info_label.pack(fill="both", expand=True)
    
    def toggle_debug(self):
        """Toggle debug mode"""
        if self.debug_mode.get():
            logging.getLogger().setLevel(logging.DEBUG)
            self.logger.info("Debug mode enabled")
        else:
            logging.getLogger().setLevel(logging.INFO)
            self.logger.info("Debug mode disabled")
        self.save_config()
    
    def toggle_gamepad(self):
        """Toggle gamepad control"""
        if self.gamepad_enabled.get():
            if not self.running:
                messagebox.showwarning("Warning", "Please connect to UDMX device first!")
                self.gamepad_enabled.set(False)
                return
            
            self.logger.info("Gamepad pan/tilt control enabled")
            self.gamepad_status.config(text="Status: Active 🎮", foreground="green")
            self.start_gamepad_thread()
        else:
            self.logger.info("Gamepad pan/tilt control disabled")
            self.gamepad_status.config(text="Status: Disabled", foreground="gray")
    
    def refresh_gamepad(self):
        """Refresh gamepad detection"""
        self.init_gamepad()
        # Recreate UI to show updated status
        messagebox.showinfo("Refresh", "Gamepad status updated. Please restart the application to see changes.")
    
    def start_gamepad_thread(self):
        """Start gamepad reading thread"""
        if self.gamepad_thread is None or not self.gamepad_thread.is_alive():
            self.gamepad_thread = threading.Thread(target=self.gamepad_loop, daemon=True)
            self.gamepad_thread.start()
    
    def gamepad_loop(self):
        """Main gamepad reading loop"""
        self.logger.info("Gamepad control loop started")
        
        while self.gamepad_enabled.get() and self.running:
            try:
                pygame.event.pump()  # Process event queue
                
                if self.gamepad:
                    # Read left analog stick (PS5 DualSense)
                    # Axis 0: Left stick X (horizontal) -> Pan (Channel 1)
                    # Axis 1: Left stick Y (vertical) -> Tilt (Channel 2)
                    
                    left_x = self.gamepad.get_axis(0)  # -1.0 to 1.0
                    left_y = self.gamepad.get_axis(1)  # -1.0 to 1.0
                    
                    # Apply deadzone (ignore small movements)
                    deadzone = 0.1
                    if abs(left_x) < deadzone:
                        left_x = 0
                    if abs(left_y) < deadzone:
                        left_y = 0
                    
                    # Convert to DMX values (0-255)
                    # Map -1.0 to 1.0 -> 0 to 255
                    pan_value = int((left_x + 1.0) * 127.5)
                    tilt_value = int((left_y + 1.0) * 127.5)
                    
                    # Clamp values
                    pan_value = max(0, min(255, pan_value))
                    tilt_value = max(0, min(255, tilt_value))
                    
                    # Update DMX channels
                    self.controller.set_channel(1, pan_value)  # Horizontal
                    self.controller.set_channel(2, tilt_value)  # Vertical
                    
                    # Update GUI sliders (in main thread)
                    self.root.after(0, lambda: self.update_slider_from_gamepad(1, pan_value))
                    self.root.after(0, lambda: self.update_slider_from_gamepad(2, tilt_value))
                
                time.sleep(0.02)  # 50 Hz update rate
                
            except Exception as e:
                self.logger.error(f"Gamepad loop error: {e}")
                time.sleep(0.1)
        
        self.logger.info("Gamepad control loop stopped")
    
    def update_slider_from_gamepad(self, channel, value):
        """Update slider value from gamepad (called from main thread)"""
        try:
            var = getattr(self, f"ch{channel}_var")
            label = getattr(self, f"ch{channel}_label")
            var.set(value)
            label.config(text=str(value))
        except:
            pass
    
    def clear_log_display(self):
        """Clear the log display"""
        self.log_display.delete(1.0, tk.END)
        self.logger.info("Log display cleared")
    
    def export_logs(self):
        """Export current logs to a file"""
        try:
            export_file = f"logs/export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write(self.log_display.get(1.0, tk.END))
            messagebox.showinfo("Success", f"Logs exported to {export_file}")
            self.logger.info(f"Logs exported to {export_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export logs: {e}")
            self.logger.error(f"Failed to export logs: {e}")
    
    def update_log_display(self):
        """Update the log display with recent log entries"""
        try:
            # Get the most recent log file
            log_files = sorted([f for f in os.listdir('logs') if f.endswith('.log')])
            if log_files:
                latest_log = os.path.join('logs', log_files[-1])
                with open(latest_log, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Show last 100 lines
                    recent_lines = lines[-100:] if len(lines) > 100 else lines
                    self.log_display.delete(1.0, tk.END)
                    self.log_display.insert(1.0, ''.join(recent_lines))
                    self.log_display.see(tk.END)
        except Exception as e:
            pass
        
        # Schedule next update
        self.root.after(2000, self.update_log_display)
    
    def update_channel_monitor(self):
        """Update the channel monitor display"""
        if self.running:
            channel_info = "Active Channels:\n"
            channel_info += "Ch1:{:3d} Ch2:{:3d} Ch3:{:3d} Ch4:{:3d} Ch5:{:3d}\n".format(
                self.controller.dmx_data[0], self.controller.dmx_data[1],
                self.controller.dmx_data[2], self.controller.dmx_data[3],
                self.controller.dmx_data[4]
            )
            channel_info += "Ch6:{:3d} Ch7:{:3d} Ch8:{:3d} Ch9:{:3d}\n".format(
                self.controller.dmx_data[5], self.controller.dmx_data[6],
                self.controller.dmx_data[7], self.controller.dmx_data[8]
            )
            
            self.channel_display.delete(1.0, tk.END)
            self.channel_display.insert(1.0, channel_info)
            
            # Update stats
            if hasattr(self, 'frames_label'):
                self.frames_label.config(text=f"Frames: {self.controller.frame_count}")
                self.errors_label.config(text=f"Errors: {self.controller.error_count}")
                
                # Calculate FPS
                if self.controller.last_send_time > 0:
                    fps = 1.0 / (self.controller.last_send_time + 0.025)
                    self.fps_label.config(text=f"FPS: {fps:.1f}")
        
        # Schedule next update
        self.root.after(100, self.update_channel_monitor)
        
    def create_channel_control(self, parent, row, label_text, channel, min_val, max_val):
        """Create a standard channel control"""
        ttk.Label(parent, text=label_text, font=("Arial", 10, "bold")).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(10, 5))
        
        var = tk.IntVar(value=0)
        setattr(self, f"ch{channel}_var", var)
        
        scale = ttk.Scale(parent, from_=min_val, to=max_val, orient="horizontal", 
                         variable=var, command=lambda v, ch=channel: self.update_channel(ch))
        scale.grid(row=row+1, column=0, sticky="ew", padx=5)
        
        label = ttk.Label(parent, text="0")
        setattr(self, f"ch{channel}_label", label)
        label.grid(row=row+1, column=1, padx=5)
        
        return var, scale, label
    
    def refresh_ports(self):
        """Refresh available UDMX devices"""
        devices = self.controller.find_udmx_devices()
        
        if devices:
            device_names = [dev['description'] for dev in devices]
            self.port_combo['values'] = device_names
            self.port_combo.current(0)
            self.logger.info(f"Found {len(devices)} UDMX device(s)")
        else:
            self.port_combo['values'] = ["No UDMX devices found"]
            self.port_combo.current(0)
            self.logger.warning("No UDMX devices detected")
    
    def toggle_connection(self):
        """Connect or disconnect from UDMX device"""
        if not self.running:
            device_name = self.port_combo.get()
            if not device_name or device_name == "No UDMX devices found":
                messagebox.showerror("Error", "Please connect a UDMX device and click Refresh")
                self.logger.warning("Connection attempt without device")
                return
            
            # Get device index from combo box
            device_index = self.port_combo.current()
            
            self.logger.info(f"User initiated connection to {device_name}")
            if self.controller.connect(device_index):
                self.running = True
                self.status_label.config(text="Status: Connected", foreground="green")
                self.connect_btn.config(text="Disconnect")
                self.start_update_thread()
                self.save_config()
                messagebox.showinfo("Success", f"Connected to {device_name}")
            else:
                messagebox.showerror("Error", "Failed to connect to UDMX device.\n\nTroubleshooting:\n- Check USB cable\n- Install libusb drivers\n- Run as Administrator (Windows)\n- Check permissions (Linux)")
                self.logger.error("Connection failed")
        else:
            self.logger.info("User initiated disconnection")
            self.running = False
            self.controller.disconnect()
            self.status_label.config(text="Status: Disconnected", foreground="red")
            self.connect_btn.config(text="Connect")
    
    def start_update_thread(self):
        """Start the DMX update thread"""
        def update_loop():
            while self.running:
                self.controller.send_dmx_frame()
                time.sleep(0.025)  # ~40 Hz update rate
        
        self.update_thread = threading.Thread(target=update_loop, daemon=True)
        self.update_thread.start()
    
    def update_channel(self, channel):
        """Update a DMX channel value"""
        var = getattr(self, f"ch{channel}_var")
        label = getattr(self, f"ch{channel}_label")
        value = int(var.get())
        label.config(text=str(value))
        self.controller.set_channel(channel, value)
    
    def all_off(self):
        """Turn all channels off"""
        self.logger.info("All channels off command")
        for i in range(1, 10):
            var = getattr(self, f"ch{i}_var", None)
            if var:
                var.set(0)
                self.update_channel(i)
    
    def full_brightness(self):
        """Set full brightness"""
        self.logger.info("Full brightness command")
        self.ch6_var.set(255)  # Dimming channel
        self.update_channel(6)
    
    def reposition(self):
        """Trigger reposition function"""
        self.logger.info("Reposition command initiated (5 seconds)")
        self.ch9_var.set(255)
        self.update_channel(9)
        # Reset after 5 seconds
        self.root.after(5000, lambda: (self.ch9_var.set(0), self.update_channel(9), 
                                      self.logger.info("Reposition completed")))
    
    def on_closing(self):
        """Handle window closing"""
        self.logger.info("Application closing")
        self.gamepad_enabled.set(False)  # Stop gamepad thread
        self.running = False
        self.controller.disconnect()
        
        # Cleanup pygame
        if self.gamepad:
            try:
                pygame.joystick.quit()
                pygame.quit()
            except:
                pass
        
        self.save_config()
        self.logger.info("Goodbye!")
        self.root.destroy()


def main():
    root = tk.Tk()
    app = DMXControllerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()

