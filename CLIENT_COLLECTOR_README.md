# Client-Side System Details Collector

## Problem

When the API is deployed on Vercel (Linux serverless), it cannot collect Windows-specific system information from client machines. Server-side collection will return "Unknown" values for:
- `username`
- `hostname` (will show server hostname)
- `system_manufacturer`
- `system_model`
- `serial_number`
- `storage` (will be empty or show server storage)

## Solution

Use the **client-side collector script** (`client_collector.py`) to collect system details on the Windows client machine and send them to the API.

## Usage

### Option 1: Run the script directly

```bash
python client_collector.py
```

Or specify a custom API URL:

```bash
python client_collector.py https://backend-blue-beta.vercel.app
```

The script will prompt you for:
- Employee ID
- Email
- Department

It will then collect all system details on your Windows machine and send them to the API.

### Option 2: Use in your frontend/client application

The script demonstrates how to collect system details and send them to the API. You can integrate this logic into your frontend application.

## API Request Format

When sending client-collected data, use this format:

```json
{
  "employee_id": "EMP001",
  "email": "user@example.com",
  "department": "IT",
  "system_details": {
    "username": "john.doe",
    "hostname": "DESKTOP-ABC123",
    "system_manufacturer": "Dell Inc.",
    "system_model": "OptiPlex 7090",
    "ip_address": "192.168.1.100",
    "serial_number": "ABC123XYZ",
    "os_info": {
      "system": "Windows",
      "release": "10",
      "version": "10.0.19045",
      "platform": "Windows-10-10.0.19045-SP0",
      "processor": "Intel64 Family 6 Model 158 Stepping 10, GenuineIntel"
    },
    "storage": [
      {
        "drive": "C:\\",
        "total_gb": 500.0,
        "used_gb": 250.0,
        "free_gb": 250.0,
        "used_percent": 50.0
      }
    ],
    "ram": {
      "total_gb": 16.0,
      "used_gb": 8.0,
      "available_gb": 8.0,
      "free_gb": 7.5,
      "used_percent": 50.0
    },
    "collected_at": "2025-01-15T10:30:00.123456"
  }
}
```

## Response Format

The API will return:

```json
{
  "success": true,
  "details": {
    "employee_id": "EMP001",
    "email": "user@example.com",
    "department": "IT",
    "username": "john.doe",
    "hostname": "DESKTOP-ABC123",
    "system_manufacturer": "Dell Inc.",
    "system_model": "OptiPlex 7090",
    "ip_address": "192.168.1.100",
    "serial_number": "ABC123XYZ",
    "os_info": {...},
    "storage": [...],
    "ram": {...}
  },
  "formatted_text": "...",
  "meta": {
    "client_data_provided": true,
    "serverless_environment": true
  }
}
```

If client data is not provided, the API will include a `collection_warning` in the response:

```json
{
  "details": {
    "collection_warning": "Server-side collection used in serverless environment. Data reflects server environment, not client. For accurate client data, provide 'system_details' in request body."
  }
}
```

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

The `client_collector.py` script requires:
- `requests` (for API calls)
- `get_system_details.py` (for system information collection)

## Notes

- Always run the client collector on the **client machine** (Windows), not on the server
- The script collects accurate Windows-specific information that cannot be collected from a Linux server
- For production use, integrate this collection logic into your frontend/client application

