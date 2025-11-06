"""
Configuration file for application settings
Loads configuration from environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://uqoifqwvwptfepuqvvhr.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVxb2lmcXd2d3B0ZmVwdXF2dmhyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0NDc0MzEsImV4cCI6MjA3ODAyMzQzMX0.gxFPq5vQ-OAFEQHFESsn7fTwQLJHm6E01LaqX6Rp0CY')

# Flask API configuration
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# API Base URL
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')

