# System Details API - Backend

Flask REST API backend for collecting and storing system information.

## Features

- RESTful API endpoints for system information collection
- Supabase database integration
- Automatic system details gathering (username, hostname, IP, serial number, Windows info, storage, RAM, etc.)
- Admin endpoints for viewing all submissions

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## Installation

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   - A `.env` file is already created with default values
   - To use your own Supabase project, edit `backend/.env`:
     ```
     SUPABASE_URL=your_supabase_url
     SUPABASE_KEY=your_supabase_anon_key
     FLASK_HOST=0.0.0.0
     FLASK_PORT=5000
     FLASK_DEBUG=True
     API_BASE_URL=http://localhost:5000
     ```
   - See `ENV_SETUP.md` in the root directory for detailed configuration

## Running the Server

### Windows
```bash
python api_server.py
```

Or double-click `start_backend.bat`

### Linux/Mac
```bash
python3 api_server.py
```

The API server will start on `http://localhost:5000`

## ⚠️ Important: Client-Side Collection Required

**When deployed on serverless platforms (Vercel, AWS Lambda, etc.), the API cannot collect Windows-specific system information from client machines.**

The API will return "Unknown" values for:
- `username`
- `system_manufacturer`
- `system_model`
- `serial_number`
- `storage` (empty array)

**Solution:** Use the client-side collector (`client_collector.py`) to collect system details on the Windows client machine and send them to the API. See `CLIENT_COLLECTOR_README.md` for details.

## API Endpoints

### `POST /api/system-details`
Collect system information for a user submission.

**Request Body (without client data - server-side collection):**
```json
{
  "employee_id": "EMP001",
  "email": "user@example.com",
  "department": "IT"
}
```

**Request Body (with client data - recommended for deployed APIs):**
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
    "os_info": {...},
    "storage": [...],
    "ram": {...}
  }
}
```

**Response:**
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
    "windows": {...},
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

**Note:** If `client_data_provided` is `false` and `serverless_environment` is `true`, the response will include a `collection_warning` indicating that server-side collection was used and data may be inaccurate.

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

### `GET /api/admin/submissions`
Get all system details submissions (Admin).

**Query Parameters:**
- `limit` (optional, default: 100): Number of records to return
- `offset` (optional, default: 0): Number of records to skip

**Response:**
```json
{
  "success": true,
  "submissions": [...],
  "count": 10
}
```

### `GET /api/admin/submissions/<id>`
Get a specific submission by ID.

**Response:**
```json
{
  "success": true,
  "submission": {...}
}
```

## Client-Side Collection

For accurate system details when the API is deployed on serverless platforms:

1. **Run the client collector on Windows machines:**
   ```bash
   python client_collector.py
   ```
   Or double-click `run_client_collector.bat`

2. **Or integrate into your frontend/client application:**
   - See `client_collector.py` for example code
   - Collect system details on the client machine
   - Send them in the `system_details` field of the API request

See `CLIENT_COLLECTOR_README.md` for detailed instructions.

## Project Structure

```
backend/
├── api_server.py              # Flask API server
├── get_system_details.py      # Core system info functions
├── client_collector.py        # Client-side collector script
├── config.py                  # Supabase configuration
├── requirements.txt           # Python dependencies
├── start_backend.bat          # Windows start script
├── run_client_collector.bat   # Client collector launcher
├── CLIENT_COLLECTOR_README.md # Client collector documentation
└── README.md                  # This file
```

## Environment Variables

Create a `.env` file in the backend directory to override default Supabase settings:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here
```

## Notes

- The server runs on port 5000 by default
- CORS is enabled for local development
- System details are saved to both text files and Supabase database
- Text files are saved in the backend directory

