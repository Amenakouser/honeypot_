@echo off
echo ========================================
echo AI Honeypot System - Setup Script
echo ========================================
echo.

echo [1/5] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.11+
    pause
    exit /b 1
)

echo.
echo [2/5] Setting up Python virtual environment...
cd backend
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists!
)

echo.
echo [3/5] Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo [4/5] Checking Node.js...
cd ..\frontend
node --version
if errorlevel 1 (
    echo ERROR: Node.js not found! Please install Node.js 18+
    pause
    exit /b 1
)

echo.
echo [5/5] Installing Node dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo IMPORTANT: Before running, please:
echo 1. Edit .env file and add your OPENAI_API_KEY
echo 2. Run 'run-backend.bat' in one terminal
echo 3. Run 'run-frontend.bat' in another terminal
echo 4. Open http://localhost:5173 in your browser
echo.
pause
