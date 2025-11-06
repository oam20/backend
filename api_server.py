"""
Flask API Server for System Details
Provides REST API endpoint to collect system information
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import json
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY, FLASK_HOST, FLASK_PORT, FLASK_DEBUG, API_BASE_URL

# Import functions from get_system_details
from get_system_details import collect_system_details, format_details_text, save_details_to_file

app = Flask(__name__)

# Get allowed origins from environment variable
ALLOWED_ORIGINS_ENV = os.getenv('ALLOWED_ORIGINS', '')
ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_ENV.split(',') if origin.strip()] if ALLOWED_ORIGINS_ENV else []

# Default origins for development
default_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://frontend-omega-tawny-35.vercel.app"
]

# Combine origins
allowed_origins = list(set(ALLOWED_ORIGINS + default_origins)) if ALLOWED_ORIGINS else default_origins

# Enable CORS for React frontend
# Check if running on Vercel (production)
is_vercel = os.getenv('VERCEL') is not None
is_production = os.getenv('FLASK_ENV') == 'production' or os.getenv('ENVIRONMENT') == 'production'

if is_vercel or is_production:
    # In production/Vercel, allow all origins for API access
    # This is common for public APIs
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": False
        }
    })
    print("CORS: Allowing all origins (production mode)")
else:
    # In development, use specific origins
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": False
        }
    })
    print(f"CORS: Allowing specific origins: {allowed_origins}")

# Initialize Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize Supabase client: {e}")
    supabase = None


@app.route('/api/system-details', methods=['POST'])
def get_system_details():
    """API endpoint to collect system details"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        employee_id = data.get('employee_id', '').strip()
        email = data.get('email', '').strip()
        department = data.get('department', '').strip()
        
        # Validate required fields
        if not employee_id or not email or not department:
            return jsonify({
                'error': 'Missing required fields',
                'required': ['employee_id', 'email', 'department']
            }), 400
        
        # Collect system details
        details = collect_system_details(employee_id, email, department)
        
        # Format as text
        formatted_text = format_details_text(details)
        
        # Save to file
        filename = None
        try:
            filename = save_details_to_file(formatted_text, employee_id)
            details['saved_file'] = filename
        except Exception as e:
            details['save_error'] = str(e)
        
        # Save to Supabase database
        if supabase:
            try:
                windows_info = details.get('windows', {})
                ram_info = details.get('ram', {})
                
                db_record = {
                    'employee_id': employee_id,
                    'email': email,
                    'department': department,
                    'username': details.get('username'),
                    'hostname': details.get('hostname'),
                    'system_manufacturer': details.get('system_manufacturer'),
                    'system_model': details.get('system_model'),
                    'ip_address': details.get('ip_address'),
                    'serial_number': details.get('serial_number'),
                    'windows_system': windows_info.get('system'),
                    'windows_release': windows_info.get('release'),
                    'windows_version': windows_info.get('version'),
                    'windows_platform': windows_info.get('platform'),
                    'windows_processor': windows_info.get('processor'),
                    'ram_total_gb': ram_info.get('total_gb') if 'error' not in ram_info else None,
                    'ram_used_gb': ram_info.get('used_gb') if 'error' not in ram_info else None,
                    'ram_available_gb': ram_info.get('available_gb') if 'error' not in ram_info else None,
                    'ram_free_gb': ram_info.get('free_gb') if 'error' not in ram_info else None,
                    'ram_used_percent': ram_info.get('used_percent') if 'error' not in ram_info else None,
                    'storage_details': json.dumps(details.get('storage', [])),
                    'formatted_text': formatted_text,
                    'saved_file': filename
                }
                
                result = supabase.table('system_details').insert(db_record).execute()
                details['db_id'] = result.data[0]['id'] if result.data else None
            except Exception as e:
                print(f"Error saving to Supabase: {e}")
                details['db_error'] = str(e)
        
        # Return both JSON and formatted text
        return jsonify({
            'success': True,
            'details': details,
            'formatted_text': formatted_text
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'API is running'}), 200


@app.route('/api/admin/submissions', methods=['GET'])
def get_all_submissions():
    """Admin endpoint to get all system details submissions"""
    try:
        if not supabase:
            return jsonify({'error': 'Database connection not available'}), 500
        
        # Get query parameters for pagination
        limit = request.args.get('limit', default=100, type=int)
        offset = request.args.get('offset', default=0, type=int)
        
        # Query Supabase
        result = supabase.table('system_details')\
            .select('*')\
            .order('created_at', desc=True)\
            .limit(limit)\
            .offset(offset)\
            .execute()
        
        return jsonify({
            'success': True,
            'submissions': result.data,
            'count': len(result.data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/admin/submissions/<submission_id>', methods=['GET'])
def get_submission_by_id(submission_id):
    """Get a specific submission by ID"""
    try:
        if not supabase:
            return jsonify({'error': 'Database connection not available'}), 500
        
        result = supabase.table('system_details')\
            .select('*')\
            .eq('id', submission_id)\
            .execute()
        
        if not result.data:
            return jsonify({'error': 'Submission not found'}), 404
        
        return jsonify({
            'success': True,
            'submission': result.data[0]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print(f"Starting Flask API server on http://{FLASK_HOST}:{FLASK_PORT}")
    print(f"API endpoint: {API_BASE_URL}/api/system-details")
    print(f"Debug mode: {FLASK_DEBUG}")
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)

