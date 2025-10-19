"""
Gamepad Test Script - PS5 DualSense
Tests gamepad connectivity and axis mapping
"""
import pygame
import time
import sys

def test_gamepad():
    """Test gamepad connection and display live values"""
    
    print("=" * 60)
    print("🎮 Gamepad Test - PS5 DualSense")
    print("=" * 60)
    print()
    
    try:
        pygame.init()
        pygame.joystick.init()
    except Exception as e:
        print(f"❌ Failed to initialize pygame: {e}")
        return False
    
    gamepad_count = pygame.joystick.get_count()
    print(f"Gamepads detected: {gamepad_count}")
    
    if gamepad_count == 0:
        print("\n❌ No gamepad detected!")
        print("\nTroubleshooting:")
        print("1. Check Bluetooth connection")
        print("2. Pair DualSense (PS + Share buttons)")
        print("3. Check if gamepad is connected in System Settings")
        print("4. Try USB cable connection")
        return False
    
    # Initialize first gamepad
    gamepad = pygame.joystick.Joystick(0)
    gamepad.init()
    
    print(f"\n✅ Gamepad connected!")
    print(f"Name: {gamepad.get_name()}")
    print(f"Axes: {gamepad.get_numaxes()}")
    print(f"Buttons: {gamepad.get_numbuttons()}")
    print(f"Hats: {gamepad.get_numhats()}")
    
    print("\n" + "=" * 60)
    print("Move LEFT STICK and watch the values")
    print("This will be used for Pan/Tilt control in DMX Controller")
    print("Press Ctrl+C to exit")
    print("=" * 60)
    print()
    
    try:
        while True:
            pygame.event.pump()
            
            # Read all axes
            left_x = gamepad.get_axis(0) if gamepad.get_numaxes() > 0 else 0
            left_y = gamepad.get_axis(1) if gamepad.get_numaxes() > 1 else 0
            right_x = gamepad.get_axis(2) if gamepad.get_numaxes() > 2 else 0
            right_y = gamepad.get_axis(3) if gamepad.get_numaxes() > 3 else 0
            
            # Convert to DMX values
            pan_dmx = int((left_x + 1.0) * 127.5)
            tilt_dmx = int((left_y + 1.0) * 127.5)
            
            # Display
            print(f"\rLeft Stick - X: {left_x:+.3f} Y: {left_y:+.3f}  |  "
                  f"DMX - Pan: {pan_dmx:3d} Tilt: {tilt_dmx:3d}  ", end='')
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("✅ Test completed successfully!")
        print("=" * 60)
        print("\nIf values changed when you moved the left stick,")
        print("your gamepad is working correctly with DMX Controller!")
        return True
    except Exception as e:
        print(f"\n\n❌ Error during test: {e}")
        return False
    finally:
        try:
            pygame.joystick.quit()
            pygame.quit()
        except:
            pass

def main():
    success = test_gamepad()
    
    if not success:
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()

