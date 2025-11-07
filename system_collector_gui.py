"""
System Details Collector - GUI Application
Creates a popup window that collects system information and sends to API
Can be packaged as .exe using PyInstaller
"""

import sys
import os
import json
import requests
import tkinter as tk
from tkinter import messagebox
import threading
import time
from get_system_details import collect_system_details

class SystemCollectorGUI:
    def __init__(self, employee_id=None, email=None, department=None, api_url=None):
        self.employee_id = employee_id
        self.email = email
        self.department = department
        self.api_url = api_url or 'https://backend-blue-beta.vercel.app'
        self.collected_data = None
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("System Requirements Lab")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Center window on screen
        self.center_window()
        
        # Set window icon (if available)
        try:
            # You can add an icon file here
            pass
        except:
            pass
        
        # Create UI
        self.create_ui()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = tk.Frame(main_frame, bg='white')
        title_frame.pack(pady=20)
        
        # Icon/Logo (simplified - you can add an image here)
        icon_label = tk.Label(
            title_frame,
            text="💻",
            font=('Arial', 24),
            bg='white'
        )
        icon_label.pack()
        
        # Main heading
        heading_label = tk.Label(
            title_frame,
            text="Hardware Detection",
            font=('Arial', 20, 'bold'),
            fg='#333333',
            bg='white'
        )
        heading_label.pack(pady=10)
        
        # Laptop icon with checkboxes
        laptop_frame = tk.Frame(main_frame, bg='white')
        laptop_frame.pack(pady=20)
        
        # Simplified laptop representation
        laptop_canvas = tk.Canvas(
            laptop_frame,
            width=200,
            height=150,
            bg='white',
            highlightthickness=0
        )
        laptop_canvas.pack()
        
        # Draw laptop shape
        laptop_canvas.create_rectangle(30, 20, 170, 100, fill='#f0f0f0', outline='#cccccc', width=2)
        laptop_canvas.create_rectangle(20, 100, 180, 110, fill='#e0e0e0', outline='#cccccc', width=2)
        
        # Checkboxes on screen
        checkbox_size = 15
        checkbox_y = 50
        
        # Checkbox 1 (completed)
        laptop_canvas.create_rectangle(50, checkbox_y, 50 + checkbox_size, checkbox_y + checkbox_size, 
                                     fill='#4CAF50', outline='#4CAF50', width=2)
        laptop_canvas.create_text(50 + checkbox_size//2, checkbox_y + checkbox_size//2, 
                                 text='✓', fill='white', font=('Arial', 10, 'bold'))
        
        # Checkbox 2 (completed)
        laptop_canvas.create_rectangle(90, checkbox_y, 90 + checkbox_size, checkbox_y + checkbox_size, 
                                     fill='#4CAF50', outline='#4CAF50', width=2)
        laptop_canvas.create_text(90 + checkbox_size//2, checkbox_y + checkbox_size//2, 
                                 text='✓', fill='white', font=('Arial', 10, 'bold'))
        
        # Checkbox 3 (in progress)
        laptop_canvas.create_rectangle(130, checkbox_y, 130 + checkbox_size, checkbox_y + checkbox_size, 
                                     fill='white', outline='#2196F3', width=2)
        # Animated dot
        self.progress_dot = laptop_canvas.create_oval(135, checkbox_y + 3, 140, checkbox_y + 8, 
                                                     fill='#2196F3', outline='')
        
        # Status message
        self.status_label = tk.Label(
            main_frame,
            text="Taking a Look...",
            font=('Arial', 16, 'bold'),
            fg='#333333',
            bg='white'
        )
        self.status_label.pack(pady=10)
        
        # Description
        desc_label = tk.Label(
            main_frame,
            text="We're identifying the hardware and software components\non your computer. No personal information is being collected.",
            font=('Arial', 10),
            fg='#666666',
            bg='white',
            justify=tk.CENTER
        )
        desc_label.pack(pady=10)
        
        # Progress bar
        self.progress_frame = tk.Frame(main_frame, bg='white')
        self.progress_frame.pack(pady=10)
        
        self.progress_bar = tk.Canvas(
            self.progress_frame,
            width=300,
            height=6,
            bg='#e0e0e0',
            highlightthickness=0
        )
        self.progress_bar.pack()
        self.progress_rect = self.progress_bar.create_rectangle(0, 0, 0, 6, fill='#4CAF50', outline='')
        
        # Cancel button
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(pady=20)
        
        self.cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel_collection,
            font=('Arial', 11),
            bg='#f5f5f5',
            fg='#333333',
            relief=tk.FLAT,
            padx=30,
            pady=8,
            cursor='hand2'
        )
        self.cancel_button.pack()
        
        # Version label
        version_label = tk.Label(
            main_frame,
            text="v 1.0.0",
            font=('Arial', 8),
            fg='#999999',
            bg='white'
        )
        version_label.pack(side=tk.BOTTOM, pady=5)
        
        # Start collection in background
        self.collection_thread = None
        self.is_collecting = True
        self.start_collection()
    
    def animate_progress(self):
        """Animate the progress bar"""
        if not self.is_collecting:
            return
        
        # Animate progress bar
        current_width = self.progress_bar.coords(self.progress_rect)[2]
        if current_width < 300:
            new_width = min(current_width + 5, 300)
            self.progress_bar.coords(self.progress_rect, 0, 0, new_width, 6)
        else:
            self.progress_bar.coords(self.progress_rect, 0, 0, 0, 6)
        
        self.root.after(50, self.animate_progress)
    
    def start_collection(self):
        """Start collecting system details in background thread"""
        self.animate_progress()
        self.collection_thread = threading.Thread(target=self.collect_system_details, daemon=True)
        self.collection_thread.start()
    
    def collect_system_details(self):
        """Collect system details (runs in background thread)"""
        try:
            # Update status
            self.root.after(0, lambda: self.status_label.config(text="Collecting system information..."))
            time.sleep(0.5)
            
            # Collect details
            self.root.after(0, lambda: self.status_label.config(text="Gathering hardware details..."))
            time.sleep(0.5)
            
            # Collect system details
            details = collect_system_details(
                self.employee_id or "AUTO",
                self.email or "auto@system.local",
                self.department or "AUTO"
            )
            
            self.collected_data = details
            
            # Update status
            self.root.after(0, lambda: self.status_label.config(text="Sending to server..."))
            time.sleep(0.5)
            
            # Send to API
            self.send_to_api(details)
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Error collecting data: {str(e)}"))
    
    def send_to_api(self, details):
        """Send collected data to API"""
        try:
            # Prepare payload
            payload = {
                'employee_id': self.employee_id or details.get('employee_id', 'AUTO'),
                'email': self.email or details.get('email', 'auto@system.local'),
                'department': self.department or details.get('department', 'AUTO'),
                'system_details': {
                    'username': details.get('username'),
                    'hostname': details.get('hostname'),
                    'system_manufacturer': details.get('system_manufacturer'),
                    'system_model': details.get('system_model'),
                    'ip_address': details.get('ip_address'),
                    'serial_number': details.get('serial_number'),
                    'os_info': details.get('os_info') or details.get('windows', {}),
                    'storage': details.get('storage', []),
                    'ram': details.get('ram', {}),
                    'collected_at': details.get('collected_at')
                }
            }
            
            # Send to API
            response = requests.post(
                f"{self.api_url}/api/system-details",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.root.after(0, self.show_success)
                else:
                    self.root.after(0, lambda: self.show_error(result.get('error', 'Unknown error')))
            else:
                self.root.after(0, lambda: self.show_error(f"Server error: {response.status_code}"))
                
        except requests.exceptions.RequestException as e:
            self.root.after(0, lambda: self.show_error(f"Network error: {str(e)}"))
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Error: {str(e)}"))
    
    def show_success(self):
        """Show success message and close"""
        self.is_collecting = False
        self.status_label.config(text="Collection Complete!")
        self.progress_bar.coords(self.progress_rect, 0, 0, 300, 6)
        
        messagebox.showinfo(
            "Success",
            "System information has been collected and sent successfully!",
            parent=self.root
        )
        
        self.root.after(1000, self.root.destroy)
    
    def show_error(self, error_msg):
        """Show error message"""
        self.is_collecting = False
        self.status_label.config(text="Error occurred")
        
        messagebox.showerror(
            "Error",
            f"Failed to collect or send system information:\n\n{error_msg}",
            parent=self.root
        )
        
        self.root.after(2000, self.root.destroy)
    
    def cancel_collection(self):
        """Cancel collection and close window"""
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel?"):
            self.is_collecting = False
            self.root.destroy()
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    employee_id = None
    email = None
    department = None
    api_url = None
    
    # Try to read from data file (created by form)
    data_file = os.path.join(os.path.expanduser('~'), 'system_collector_data.json')
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                employee_id = data.get('employee_id')
                email = data.get('email')
                department = data.get('department')
                api_url = data.get('api_url', 'https://backend-blue-beta.vercel.app')
            # Delete the file after reading
            try:
                os.remove(data_file)
            except:
                pass
        except Exception as e:
            print(f"Error reading data file: {e}")
    
    # Check for command line arguments (alternative method)
    if not all([employee_id, email, department]) and len(sys.argv) > 1:
        try:
            # Parse arguments: employee_id,email,department,api_url
            args = sys.argv[1].split(',')
            if len(args) >= 1:
                employee_id = args[0] if args[0] else employee_id
            if len(args) >= 2:
                email = args[1] if args[1] else email
            if len(args) >= 3:
                department = args[2] if args[2] else department
            if len(args) >= 4:
                api_url = args[3] if args[3] else api_url
        except:
            pass
    
    # If still no data, prompt user
    if not all([employee_id, email, department]):
        import tkinter as tk
        from tkinter import simpledialog
        
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        employee_id = simpledialog.askstring("Employee ID", "Enter your Employee ID:")
        if not employee_id:
            root.destroy()
            return
        
        email = simpledialog.askstring("Email", "Enter your Email:")
        if not email:
            root.destroy()
            return
        
        department = simpledialog.askstring("Department", "Enter your Department:")
        if not department:
            root.destroy()
            return
        
        root.destroy()
    
    # Create and run GUI
    app = SystemCollectorGUI(employee_id, email, department, api_url)
    app.run()


if __name__ == '__main__':
    main()

