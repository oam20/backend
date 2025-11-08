# Web Form with Automatic System Details Collection

## Overview

This solution provides a web form that automatically collects system information when users submit the form. Users only need to fill in their details (Employee ID, Email, Department) and click Submit.

## Files

- `form-example.html` - Complete HTML form with automatic system collection
- `system-collector.js` - JavaScript library for collecting system information

## How It Works

1. User fills in the form (Employee ID, Email, Department)
2. User clicks Submit
3. JavaScript automatically collects available system information
4. Form data + system details are sent to the API
5. User sees success/error message

## Browser Limitations

Due to browser security restrictions, JavaScript **cannot** access:
- ❌ Serial number
- ❌ System manufacturer (hardware)
- ❌ System model (hardware)
- ❌ OS username
- ❌ Computer hostname
- ❌ Detailed storage information

**What JavaScript CAN collect:**
- ✅ OS type and version (from user agent)
- ✅ Browser information
- ✅ Screen resolution
- ✅ IP address (via external service)
- ✅ Browser storage quota
- ✅ RAM (if available via browser API)
- ✅ Platform/processor info

## Setup

### Option 1: Use the Example Form

1. Open `form-example.html` in a text editor
2. Update the `API_URL` constant (line ~200):
   ```javascript
   const API_URL = 'https://backend-blue-beta.vercel.app';
   ```
3. Host the files on a web server or use a static hosting service
4. Share the form URL with users

### Option 2: Integrate into Your Existing Form

1. Include `system-collector.js` in your HTML:
   ```html
   <script src="system-collector.js"></script>
   ```

2. Add this to your form submission handler:
   ```javascript
   const collector = new SystemDetailsCollector();
   const systemDetails = await collector.collect();
   
   // Add to your form data
   const payload = {
       employee_id: formData.employee_id,
       email: formData.email,
       department: formData.department,
       system_details: systemDetails
   };
   
   // Send to API
   fetch('https://backend-blue-beta.vercel.app/api/system-details', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify(payload)
   });
   ```

## For Complete Windows System Details

If you need **complete** Windows system information (serial number, manufacturer, model, etc.), you have two options:

### Option A: Hybrid Approach (Recommended)
1. Use the web form for basic collection (what's available via browser)
2. Optionally provide a small Windows executable that users can run once to collect full details
3. The executable can send the complete data to your API

### Option B: Browser Extension
Create a browser extension that has more permissions to access system information (requires user installation).

### Option C: Accept Browser Limitations
Use what's available via browser APIs and mark unavailable fields as "Not available via browser" in your database.

## Example Response

When submitted via web form, the API will receive:

```json
{
  "employee_id": "EMP001",
  "email": "user@example.com",
  "department": "IT",
  "system_details": {
    "username": "Unknown",
    "hostname": "example.com",
    "system_manufacturer": "Detected: Windows",
    "system_model": "x64 Architecture",
    "ip_address": "203.0.113.1",
    "serial_number": "Not available via browser",
    "os_info": {
      "system": "Windows",
      "release": "10",
      "version": "Mozilla/5.0...",
      "platform": "Win32",
      "processor": "8 cores"
    },
    "storage": [{
      "drive": "Browser Storage",
      "total_gb": 5.0,
      "used_gb": 0.5,
      "free_gb": 4.5,
      "used_percent": 10.0
    }],
    "ram": {
      "total_gb": 16,
      "note": "Browser API limitation - only total RAM available"
    },
    "browser": {
      "name": "Chrome",
      "version": "120",
      "language": "en-US"
    },
    "screen": {
      "width": 1920,
      "height": 1080
    }
  }
}
```

## Testing

1. Open `form-example.html` in a web browser
2. Fill in the form fields
3. Click Submit
4. Check browser console (F12) for collected data
5. Verify API response

## Deployment

### Static Hosting
- Upload `form-example.html` and `system-collector.js` to:
  - GitHub Pages
  - Netlify
  - Vercel (static)
  - Any web server

### Update API URL
Make sure to update the `API_URL` constant in `form-example.html` to point to your deployed API.

## Security Notes

- The form sends data over HTTPS (recommended)
- IP address is collected via external service (ipify.org, ipapi.co)
- No sensitive data is stored locally
- All data is sent to your API endpoint

