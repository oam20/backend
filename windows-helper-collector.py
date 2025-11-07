"""
Windows Helper - Collects Full System Details
This script can be packaged as an executable and run once to collect complete Windows system information.
Users can run this once, and it will collect all system details that browsers cannot access.
"""

import json
import sys
import webbrowser
from get_system_details import collect_system_details

def collect_and_open_form():
    """Collect system details and open form with pre-filled data"""
    try:
        print("=" * 60)
        print("Windows System Details Collector")
        print("=" * 60)
        print("\nCollecting system information...")
        
        # Collect system details
        # We'll use placeholder values for employee_id, email, department
        # These will be filled by the user in the web form
        details = collect_system_details("TEMP", "temp@temp.com", "TEMP")
        
        # Extract system details
        system_details = {
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
        
        # Save to a temporary file that the web form can read
        import tempfile
        import os
        
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, 'system_details_temp.json')
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(system_details, f, indent=2)
        
        print("\n✅ System details collected and saved!")
        print(f"📁 Details saved to: {temp_file}")
        print("\n" + "=" * 60)
        print("Next Steps:")
        print("1. Fill out the web form")
        print("2. The form will automatically load your system details")
        print("3. Submit the form")
        print("=" * 60)
        
        # Optionally open the form URL
        form_url = input("\nEnter your form URL (or press Enter to skip): ").strip()
        if form_url:
            webbrowser.open(form_url)
        
        return system_details
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def save_to_clipboard():
    """Save system details to clipboard for easy pasting"""
    try:
        details = collect_system_details("TEMP", "temp@temp.com", "TEMP")
        system_details = {
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
        
        json_str = json.dumps(system_details, indent=2)
        
        try:
            import pyperclip
            pyperclip.copy(json_str)
            print("✅ System details copied to clipboard!")
            print("You can paste this into the form's system_details field.")
        except ImportError:
            print("⚠️  pyperclip not installed. Install with: pip install pyperclip")
            print("\nSystem details JSON:")
            print(json_str)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == '__main__':
    print("\nChoose an option:")
    print("1. Collect and save to temp file (for web form integration)")
    print("2. Collect and copy to clipboard")
    print("3. Just collect and display")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        collect_and_open_form()
    elif choice == '2':
        save_to_clipboard()
    elif choice == '3':
        details = collect_system_details("TEMP", "temp@temp.com", "TEMP")
        print("\n" + json.dumps(details, indent=2))
    else:
        print("Invalid choice. Running default collection...")
        collect_and_open_form()

