@echo off
echo Starting System Details API Backend...
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask API server...
echo API will be available at: http://localhost:5000
echo.
python api_server.py

