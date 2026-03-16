@echo off
echo ========================================
echo   AutoClapper 2.0 - Starting...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from python.org
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if templates folder exists
if not exist "templates" (
    echo WARNING: templates folder not found!
    echo Creating templates folder...
    mkdir templates
    echo.
    echo Please add your template files to the templates folder:
    echo   - script_template.docx
    echo   - clapper_blank.png
    echo.
    pause
)

REM Check if dependencies are installed by trying to import them
echo Checking Python dependencies...
python -c "import flask, flask_cors, docx, PIL" >nul 2>&1
if errorlevel 1 (
    echo Some dependencies are missing. Attempting to install...
    echo.
    
    REM Try using pip
    pip --version >nul 2>&1
    if errorlevel 1 (
        echo WARNING: pip is not available in PATH
        echo.
        echo Please install the required packages manually:
        echo   python -m pip install --break-system-packages flask flask-cors python-docx Pillow
        echo.
        echo Or try:
        echo   python -m pip install flask flask-cors python-docx Pillow
        echo.
        echo If you've already installed the packages manually, press any key to continue anyway...
        pause
    ) else (
        echo Installing/updating Python dependencies...
        pip install --break-system-packages flask flask-cors python-docx Pillow
        if errorlevel 1 (
            echo.
            echo First attempt failed, trying without --break-system-packages flag...
            pip install flask flask-cors python-docx Pillow
            if errorlevel 1 (
                echo.
                echo WARNING: Failed to install some dependencies.
                echo Please try running this command manually:
                echo   pip install flask flask-cors python-docx Pillow
                echo.
                echo Press any key to attempt to start anyway...
                pause
            ) else (
                echo.
                echo Dependencies installed successfully!
                echo.
            )
        ) else (
            echo.
            echo Dependencies installed successfully!
            echo.
        )
    )
) else (
    echo All core dependencies are installed!
    echo.
)

REM Check for optional Whisper dependency (don't let this crash the startup)
echo Checking for optional Whisper (audio transcription)...
python -c "import whisper" >nul 2>&1
if errorlevel 1 (
    echo NOTE: Audio transcription feature (Whisper) is not installed.
    echo This is optional. To enable it, run:
    echo   pip install openai-whisper
) else (
    echo Whisper is installed - audio transcription available!
)
echo.

echo Starting AutoClapper 2.0 server...
echo.
echo The server will start in this window.
echo DO NOT CLOSE THIS WINDOW while using AutoClapper!
echo.
echo The web interface will open automatically in your browser.
echo If it doesn't open, navigate to: http://localhost:5000
echo.
echo To stop the server, press Ctrl+C in this window.
echo ========================================
echo.

REM Start the server in the background and open browser
start "" "%~dp0autoclapper-interface.html"

echo Starting Python server...
python app.py

REM This pause will only run if the server stops/crashes
echo.
echo.
echo ========================================
echo Server has stopped or encountered an error.
echo ========================================
pause
