# app.py
# Simple wrapper so Vercel finds a Flask 'app' entrypoint.

from api_server import app

# Optionally expose application also as 'application' for WSGI compatibility:
application = app
