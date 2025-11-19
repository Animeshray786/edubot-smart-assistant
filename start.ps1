# EduBot Startup Script (PowerShell)
# This script ensures the server always starts cleanly

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  EduBot - Smart Student Assistant" -ForegroundColor Green
Write-Host "  Starting Server..." -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[INFO] $pythonVersion detected" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher" -ForegroundColor Yellow
    pause
    exit 1
}

# Check if virtual environment exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

# Create logs directory if it doesn't exist
if (-not (Test-Path "logs")) {
    Write-Host "[INFO] Creating logs directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

# Create uploads directory if it doesn't exist
if (-not (Test-Path "uploads")) {
    Write-Host "[INFO] Creating uploads directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "uploads" | Out-Null
    New-Item -ItemType Directory -Path "uploads\images" | Out-Null
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host "[INFO] Creating .env from .env.example..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host "[WARNING] Please update .env with your configuration!" -ForegroundColor Yellow
    } else {
        Write-Host "[ERROR] No .env file found!" -ForegroundColor Red
        Write-Host "Please create a .env file with your configuration." -ForegroundColor Yellow
        pause
        exit 1
    }
}

# Start the server
Write-Host "`n[INFO] Running health check...`n" -ForegroundColor Green
python healthcheck.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[ERROR] Health check failed! Fix the issues above." -ForegroundColor Red
    pause
    exit 1
}

Write-Host "`n[INFO] Starting Flask server...`n" -ForegroundColor Green
python app.py

# If the server stops, pause so you can see any errors
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[ERROR] Server stopped with an error!" -ForegroundColor Red
    pause
}
