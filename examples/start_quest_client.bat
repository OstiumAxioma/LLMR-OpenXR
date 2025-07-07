@echo off
echo ========================================
echo Quest Test Client Startup Script
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found, please install Python 3.7+
    pause
    exit /b 1
)

:: Check dependencies
echo Checking dependencies...
python -c "import requests, numpy, cv2" >nul 2>&1
if errorlevel 1 (
    echo Installing missing dependencies...
    pip install requests numpy opencv-python
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Dependencies check completed
echo.

:: Start client
echo Starting Quest test client...
echo Connecting to server: http://localhost:8888
echo.
echo Client will send:
echo - Camera frames: 1 per second
echo - Audio frames: 10 per second  
echo - Text messages: 1 every 5 seconds
echo.
echo Press Ctrl+C to stop the client
echo.

python quest_test_client.py

echo.
echo Client stopped
pause 