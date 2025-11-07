"""
Client-Side System Details Collector
Collects system information on the client machine and sends it to the API.
Run this script on Windows machines to collect accurate system details.
"""

import requests
import json
import sys
from get_system_details import collect_system_details

def send_to_api(api_url, employee_id, email, department):
    """Collect system details and send to API"""
    try:
        # Collect system details on client machine
        print("Collecting system details...")
        details = collect_system_details(employee_id, email, department)
        
        # Prepare request payload with client-collected data
        payload = {
            'employee_id': employee_id,
            'email': email,
            'department': department,
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
        print(f"Sending data to {api_url}...")
        response = requests.post(
            f"{api_url}/api/system-details",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Success! System details sent to API.")
            print(f"\nResponse: {json.dumps(result, indent=2)}")
            return result
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Network error: {e}")
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


if __name__ == '__main__':
    # Default API URL (can be overridden via command line)
    API_URL = 'https://backend-blue-beta.vercel.app'
    
    if len(sys.argv) > 1:
        API_URL = sys.argv[1]
    
    print("=" * 60)
    print("System Details Client Collector")
    print("=" * 60)
    print(f"API URL: {API_URL}\n")
    
    # Get user input
    employee_id = input("Enter Employee ID: ").strip()
    email = input("Enter Email: ").strip()
    department = input("Enter Department: ").strip()
    
    if not all([employee_id, email, department]):
        print("\n❌ Error: All fields are required!")
        sys.exit(1)
    
    # Send to API
    result = send_to_api(API_URL, employee_id, email, department)
    
    if result:
        print("\n" + "=" * 60)
        print("Collection complete!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Collection failed!")
        print("=" * 60)
        sys.exit(1)

