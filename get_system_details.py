"""
System Details Fetcher
Fetches and displays system information including:
- Username
- Hostname
- Windows Version
- Storage Details
- RAM Details
"""

import os
import socket
import platform
import shutil
import sys
import subprocess
import datetime

# GUI
try:
    import tkinter as tk
    from tkinter import messagebox
    from tkinter.scrolledtext import ScrolledText
    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not installed. RAM details will be limited.")
    print("Install it with: pip install psutil\n")


def get_username():
    """Get the current username"""
    try:
        return os.getlogin()
    except:
        try:
            return os.environ.get('USERNAME', os.environ.get('USER', 'Unknown'))
        except:
            return 'Unknown'


def get_hostname():
    """Get the hostname"""
    try:
        return socket.gethostname()
    except:
        return 'Unknown'


def get_system_manufacturer():
    """Get the system manufacturer"""
    try:
        if sys.platform == 'win32':
            # Try WMIC first
            try:
                result = subprocess.run(
                    ["wmic", "computersystem", "get", "manufacturer"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                output = (result.stdout or "").strip().splitlines()
                values = [line.strip() for line in output if line and "Manufacturer" not in line]
                if values and values[0]:
                    return values[0]
            except:
                pass
            
            # PowerShell fallback
            try:
                ps_cmd = [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "(Get-CimInstance Win32_ComputerSystem).Manufacturer"
                ]
                result = subprocess.run(ps_cmd, capture_output=True, text=True, check=False)
                value = (result.stdout or "").strip()
                if value:
                    return value
            except:
                pass
        
        return 'Unknown'
    except:
        return 'Unknown'


def get_system_model():
    """Get the system model"""
    try:
        if sys.platform == 'win32':
            # Try WMIC first
            try:
                result = subprocess.run(
                    ["wmic", "computersystem", "get", "model"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                output = (result.stdout or "").strip().splitlines()
                values = [line.strip() for line in output if line and "Model" not in line]
                if values and values[0]:
                    return values[0]
            except:
                pass
            
            # PowerShell fallback
            try:
                ps_cmd = [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "(Get-CimInstance Win32_ComputerSystem).Model"
                ]
                result = subprocess.run(ps_cmd, capture_output=True, text=True, check=False)
                value = (result.stdout or "").strip()
                if value:
                    return value
            except:
                pass
        
        return 'Unknown'
    except:
        return 'Unknown'


def get_ip_address():
    """Get primary IPv4 address (non-loopback)"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # This doesn't send data; it just selects the outbound interface
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return 'Unknown'


def get_serial_number():
    """Get machine serial number on Windows using WMIC or PowerShell fallback"""
    # Try WMIC first (may be deprecated but often available)
    try:
        result = subprocess.run(
            ["wmic", "bios", "get", "serialnumber"],
            capture_output=True,
            text=True,
            check=False
        )
        output = (result.stdout or "").strip().splitlines()
        values = [line.strip() for line in output if line and "SerialNumber" not in line]
        if values:
            return values[0]
    except:
        pass

    # PowerShell fallback (works on newer Windows)
    try:
        ps_cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_BIOS).SerialNumber"
        ]
        result = subprocess.run(ps_cmd, capture_output=True, text=True, check=False)
        value = (result.stdout or "").strip()
        if value:
            return value
    except:
        pass

    return 'Unknown'


def get_windows_version():
    """Get Windows version details"""
    try:
        version_info = {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'platform': platform.platform(),
            'processor': platform.processor()
        }
        return version_info
    except:
        return {'error': 'Could not retrieve Windows version'}


def get_storage_details():
    """Get storage details for all drives"""
    storage_info = []
    try:
        # Get all drives on Windows
        drives = []
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
        
        for drive in drives:
            try:
                total, used, free = shutil.disk_usage(drive)
                storage_info.append({
                    'drive': drive,
                    'total_gb': round(total / (1024**3), 2),
                    'used_gb': round(used / (1024**3), 2),
                    'free_gb': round(free / (1024**3), 2),
                    'used_percent': round((used / total) * 100, 2)
                })
            except:
                continue
    except Exception as e:
        storage_info.append({'error': str(e)})
    
    return storage_info


def get_ram_details():
    """Get RAM details"""
    if PSUTIL_AVAILABLE:
        try:
            ram = psutil.virtual_memory()
            return {
                'total_gb': round(ram.total / (1024**3), 2),
                'available_gb': round(ram.available / (1024**3), 2),
                'used_gb': round(ram.used / (1024**3), 2),
                'free_gb': round(ram.free / (1024**3), 2),
                'used_percent': round(ram.percent, 2)
            }
        except Exception as e:
            return {'error': str(e)}
    else:
        return {'error': 'psutil not available. Install with: pip install psutil'}


def collect_system_details(employee_id: str, email: str, department: str):
    """Collect all system details and include user-provided metadata."""
    details = {
        'employee_id': employee_id,
        'email': email,
        'department': department,
        'collected_at': datetime.datetime.now().isoformat(),
        'username': get_username(),
        'hostname': get_hostname(),
        'system_manufacturer': get_system_manufacturer(),
        'system_model': get_system_model(),
        'ip_address': get_ip_address(),
        'serial_number': get_serial_number(),
        'windows': get_windows_version(),
        'storage': get_storage_details(),
        'ram': get_ram_details(),
    }
    return details


def format_details_text(details: dict) -> str:
    """Format details dict into readable multiline text."""
    lines = []
    lines.append("=" * 60)
    lines.append("SYSTEM DETAILS")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Collected At: {details.get('collected_at', '')}")
    lines.append(f"Employee ID: {details.get('employee_id', '')}")
    lines.append(f"Email: {details.get('email', '')}")
    lines.append(f"Department: {details.get('department', '')}")
    lines.append("")
    lines.append(f"Username: {details.get('username', '')}")
    lines.append(f"Hostname: {details.get('hostname', '')}")
    lines.append(f"System Manufacturer: {details.get('system_manufacturer', '')}")
    lines.append(f"System Model: {details.get('system_model', '')}")
    lines.append(f"IP Address: {details.get('ip_address', '')}")
    lines.append(f"Serial Number: {details.get('serial_number', '')}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("WINDOWS INFORMATION")
    lines.append("-" * 60)
    win = details.get('windows', {}) or {}
    lines.append(f"System: {win.get('system', 'N/A')}")
    lines.append(f"Release: {win.get('release', 'N/A')}")
    lines.append(f"Version: {win.get('version', 'N/A')}")
    lines.append(f"Platform: {win.get('platform', 'N/A')}")
    lines.append(f"Processor: {win.get('processor', 'N/A')}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("STORAGE DETAILS")
    lines.append("-" * 60)
    storage = details.get('storage', []) or []
    if storage:
        for d in storage:
            if 'error' in d:
                lines.append(f"Error: {d['error']}")
            else:
                lines.append(f"Drive: {d.get('drive', '')}")
                lines.append(f"  Total: {d.get('total_gb', 'N/A')} GB")
                lines.append(f"  Used: {d.get('used_gb', 'N/A')} GB ({d.get('used_percent', 'N/A')}%)")
                lines.append(f"  Free: {d.get('free_gb', 'N/A')} GB")
                lines.append("")
    else:
        lines.append("No storage information available")
    lines.append("-" * 60)
    lines.append("RAM DETAILS")
    lines.append("-" * 60)
    ram = details.get('ram', {}) or {}
    if 'error' not in ram:
        lines.append(f"Total RAM: {ram.get('total_gb', 'N/A')} GB")
        lines.append(f"Used RAM: {ram.get('used_gb', 'N/A')} GB ({ram.get('used_percent', 'N/A')}%)")
        lines.append(f"Available RAM: {ram.get('available_gb', 'N/A')} GB")
        lines.append(f"Free RAM: {ram.get('free_gb', 'N/A')} GB")
    else:
        lines.append(f"Error: {ram.get('error', '')}")
    lines.append("")
    lines.append("=" * 60)
    lines.append("End of System Details")
    lines.append("=" * 60)
    return "\n".join(lines)


def save_details_to_file(details_text: str, employee_id: str) -> str:
    """Save details as a .txt file and return the filename."""
    safe_emp = (employee_id or 'unknown').strip().replace(' ', '_')
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"system_details_{safe_emp}_{timestamp}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(details_text)
    return filename


def run_gui():
    if not TK_AVAILABLE:
        print("GUI not available. Please run from console or ensure Tkinter is installed.")
        return

    root = tk.Tk()
    root.title("System Details Form")

    # Form frame
    form = tk.Frame(root, padx=10, pady=10)
    form.pack(fill=tk.X)

    tk.Label(form, text="Employee ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
    emp_entry = tk.Entry(form, width=40)
    emp_entry.grid(row=0, column=1, padx=8, pady=5)

    tk.Label(form, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
    email_entry = tk.Entry(form, width=40)
    email_entry.grid(row=1, column=1, padx=8, pady=5)

    tk.Label(form, text="Department:").grid(row=2, column=0, sticky=tk.W, pady=5)
    dept_entry = tk.Entry(form, width=40)
    dept_entry.grid(row=2, column=1, padx=8, pady=5)

    # Output area
    output = ScrolledText(root, wrap=tk.WORD, height=22)
    output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def on_submit():
        employee_id = emp_entry.get().strip()
        email = email_entry.get().strip()
        department = dept_entry.get().strip()

        if not employee_id or not email or not department:
            messagebox.showwarning("Missing Data", "Please fill Employee ID, Email, and Department.")
            return
        if '@' not in email or '.' not in email:
            if not messagebox.askyesno("Confirm Email", "The email looks unusual. Continue anyway?"):
                return

        details = collect_system_details(employee_id, email, department)
        text = format_details_text(details)
        output.delete('1.0', tk.END)
        output.insert(tk.END, text)

        try:
            filename = save_details_to_file(text, employee_id)
            messagebox.showinfo("Saved", f"Details saved to {filename}")
        except Exception as e:
            messagebox.showerror("Save Failed", str(e))

    def on_copy():
        text = output.get('1.0', tk.END)
        root.clipboard_clear()
        root.clipboard_append(text)
        messagebox.showinfo("Copied", "Details copied to clipboard.")

    buttons = tk.Frame(root, padx=10, pady=5)
    buttons.pack(fill=tk.X)
    submit_btn = tk.Button(buttons, text="Submit & Gather Info", command=on_submit)
    submit_btn.pack(side=tk.LEFT)
    copy_btn = tk.Button(buttons, text="Copy Output", command=on_copy)
    copy_btn.pack(side=tk.LEFT, padx=8)

    root.mainloop()


if __name__ == "__main__":
    format_output()
    
    # Keep window open on Windows if double-clicked
    if sys.platform == 'win32':
        input("\nPress Enter to exit...")

