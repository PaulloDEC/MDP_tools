@echo off
echo ========================================
echo   AutoTranscribe - Starting...
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
echo Starting AutoTranscribe server...
echo The web interface should open automatically.
echo.
echo DO NOT CLOSE THIS WINDOW!
echo.
echo Transcribed files will be saved to: transcriptions\
echo.

REM Open the web interface
start "" "http://localhost:5001"

REM Start the Python server
python autotranscribe_app.py

echo.
echo Server stopped.
pause
