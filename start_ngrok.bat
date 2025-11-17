@echo off
REM Quick Start Script for EduBot with Ngrok
REM Run this to launch EduBot with public internet access

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         EduBot - Starting with Public Internet Access         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if pyngrok is installed
python -c "import pyngrok" 2>nul
if errorlevel 1 (
    echo [ERROR] pyngrok not installed
    echo.
    echo Installing pyngrok...
    pip install pyngrok
    echo.
)

REM Start the application
echo [OK] Starting EduBot with Ngrok...
echo.
python start_with_ngrok.py

pause
