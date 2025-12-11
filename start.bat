@echo off
echo ========================================
echo  Bhuvi AI Assistant - Quick Start
echo ========================================
echo.

echo [1/3] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [2/3] Checking configuration...
if not exist ".env" (
    echo WARNING: .env file not found
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env and add your GEMINI_API_KEY
    echo Get your API key from: https://makersuite.google.com/app/apikey
    echo.
    pause
)
echo.

echo [3/3] Starting backend server...
echo.
echo Backend will start on http://localhost:8000
echo Open frontend/index.html in your browser after server starts
echo.
echo Press Ctrl+C to stop the server
echo.
cd backend
python main.py

pause
