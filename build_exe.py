"""
Build script to create .exe file from system_collector_gui.py
Requires PyInstaller: pip install pyinstaller
"""

import subprocess
import sys
import os

def build_exe():
    """Build the .exe file using PyInstaller"""
    print("=" * 60)
    print("Building System Collector .exe")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("\n❌ PyInstaller not found!")
        print("Please install it first:")
        print("  pip install pyinstaller")
        return False
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Single executable file
        '--windowed',                   # No console window (GUI only)
        '--name=SystemCollector',       # Output name
        '--icon=NONE',                  # No icon (you can add one later)
        '--add-data=get_system_details.py;.',  # Include required module
        '--hidden-import=requests',      # Include requests
        '--hidden-import=psutil',       # Include psutil if available
        '--hidden-import=tkinter',     # Include tkinter
        'system_collector_gui.py'
    ]
    
    print("\nRunning PyInstaller...")
    print("Command:", ' '.join(cmd))
    print("\nThis may take a few minutes...\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        print(f"\nExecutable created at: dist/SystemCollector.exe")
        print("\nYou can now distribute this .exe file.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed!")
        print(f"Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == '__main__':
    success = build_exe()
    sys.exit(0 if success else 1)

