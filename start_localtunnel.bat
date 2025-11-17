@echo off
REM LocalTunnel Quick Start - FREE, NO SIGNUP!
REM Run this to get instant public URL

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║       EduBot - FREE Public Access (No Signup Required!)       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if LocalTunnel is installed
where lt >nul 2>nul
if errorlevel 1 (
    echo [INFO] LocalTunnel not installed. Installing...
    echo.
    call npm install -g localtunnel
    echo.
)

REM Start LocalTunnel
echo [OK] Starting EduBot with LocalTunnel...
echo.
python start_with_localtunnel.py

pause
