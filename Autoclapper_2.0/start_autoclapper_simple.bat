@echo off
echo ========================================
echo   AutoClapper 2.0 - Quick Start
echo   (Skips optional checks)
echo ========================================
echo.

REM Check if Python is installed
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Starting server...
echo The web interface should open automatically.
echo.
echo DO NOT CLOSE THIS WINDOW!
echo.

REM Open the web interface
start "" "%~dp0autoclapper-interface.html"

REM Start the Python server
python app.py

echo.
echo Server stopped.
pause
