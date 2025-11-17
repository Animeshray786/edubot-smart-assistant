@echo off
echo ========================================
echo   Starting Ngrok Tunnel - Keep Open!
echo ========================================
echo.
echo Connecting to your custom domain...
echo.

cd /d "%~dp0"
ngrok http --url=elicia-conflictory-denny.ngrok-free.dev 5000

pause
