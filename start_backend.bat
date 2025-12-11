@echo off
echo ========================================
echo Starting Bhuvi AI Assistant Backend
echo ========================================
echo.

REM Change to project directory
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if Ollama is running
echo Checking Ollama service...
curl -s http://localhost:11434 >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama is not running! Please start Ollama first.
    echo Press any key to continue anyway...
    pause >nul
)

REM Start the backend server
echo.
echo Starting backend server on http://localhost:8000
echo Backend will auto-reload on code changes
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

REM If server stops, pause to see error
echo.
echo ========================================
echo Backend server stopped!
echo ========================================
pause
