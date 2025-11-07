@echo off
echo ============================================================
echo Building System Collector .exe
echo ============================================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

echo.
echo Building executable...
echo.

pyinstaller --onefile --windowed --name=SystemCollector --add-data="get_system_details.py;." --hidden-import=requests --hidden-import=psutil --hidden-import=tkinter system_collector_gui.py

if exist "dist\SystemCollector.exe" (
    echo.
    echo ============================================================
    echo Build Successful!
    echo ============================================================
    echo.
    echo Executable created at: dist\SystemCollector.exe
    echo.
    echo You can now distribute this .exe file.
) else (
    echo.
    echo ============================================================
    echo Build Failed!
    echo ============================================================
    echo.
    echo Check the error messages above.
)

pause

