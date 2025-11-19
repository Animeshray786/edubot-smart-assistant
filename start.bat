@echo off
REM EduBot Startup Script
REM This script ensures the server always starts cleanly

echo.
echo ============================================================
echo   EduBot - Smart Student Assistant
echo   Starting Server...
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Create logs directory if it doesn't exist
if not exist "logs" (
    echo [INFO] Creating logs directory...
    mkdir logs
)

REM Create uploads directory if it doesn't exist
if not exist "uploads" (
    echo [INFO] Creating uploads directory...
    mkdir uploads
    mkdir uploads\images
)

REM Check if .env file exists
if not exist ".env" (
    if exist ".env.example" (
        echo [INFO] Creating .env from .env.example...
        copy .env.example .env
        echo [WARNING] Please update .env with your configuration!
    ) else (
        echo [ERROR] No .env file found!
        echo Please create a .env file with your configuration.
        pause
        exit /b 1
    )
)

REM Start the server
echo.
echo [INFO] Running health check...
echo.
python healthcheck.py
if errorlevel 1 (
    echo.
    echo [ERROR] Health check failed! Fix the issues above.
    pause
    exit /b 1
)

echo.
echo [INFO] Starting Flask server...
echo.
python app.py

REM If the server stops, pause so you can see any errors
if errorlevel 1 (
    echo.
    echo [ERROR] Server stopped with an error!
    pause
)
