@echo off
echo ========================================
echo Quest Test Server Startup Script
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
python -c "import flask, cv2, numpy, requests" >nul 2>&1
if errorlevel 1 (
    echo Installing missing dependencies...
    pip install flask flask-cors opencv-python numpy requests
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Dependencies check completed
echo.

:: Start server with default settings
echo Starting Quest test server...
echo Port: 8888
echo Data saving: enabled
echo.
echo Server will be available at:
echo - Server address: http://localhost:8888
echo - Health check: http://localhost:8888/health
echo - Status page: http://localhost:8888/status
echo.
echo Press Ctrl+C to stop the server
echo.

python quest_test_server.py --save-data

echo.
echo Server stopped
pause 