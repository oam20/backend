@echo off
echo ============================================================
echo System Details Client Collector
echo ============================================================
echo.
echo This script collects system details from your Windows machine
echo and sends them to the API server.
echo.
echo Make sure you have Python installed and dependencies installed:
echo   pip install -r requirements.txt
echo.
pause

python client_collector.py https://backend-blue-beta.vercel.app

pause

