"""
Standalone version that can prompt for data if not provided via command line
"""

import sys
import os
import json
import requests
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import time
from get_system_details import collect_system_details

# Import the GUI class
from system_collector_gui import SystemCollectorGUI

def prompt_for_data():
    """Prompt user for form data if not provided"""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    employee_id = simpledialog.askstring("Employee ID", "Enter your Employee ID:")
    if not employee_id:
        return None, None, None
    
    email = simpledialog.askstring("Email", "Enter your Email:")
    if not email:
        return None, None, None
    
    department = simpledialog.askstring("Department", "Enter your Department:")
    if not department:
        return None, None, None
    
    root.destroy()
    return employee_id, email, department

def main():
    """Main entry point"""
    employee_id = None
    email = None
    department = None
    api_url = 'https://backend-blue-beta.vercel.app'
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        try:
            args = sys.argv[1].split(',')
            if len(args) >= 1:
                employee_id = args[0] if args[0] else None
            if len(args) >= 2:
                email = args[1] if args[1] else None
            if len(args) >= 3:
                department = args[2] if args[2] else None
            if len(args) >= 4:
                api_url = args[3] if args[3] else 'https://backend-blue-beta.vercel.app'
        except:
            pass
    
    # If data not provided, prompt user
    if not all([employee_id, email, department]):
        employee_id, email, department = prompt_for_data()
        if not all([employee_id, email, department]):
            messagebox.showerror("Error", "All fields are required!")
            return
    
    # Create and run GUI
    app = SystemCollectorGUI(employee_id, email, department, api_url)
    app.run()

if __name__ == '__main__':
    main()

