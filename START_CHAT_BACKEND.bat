@echo off
REM Quick start script for chat backend on Windows
REM Usage: START_CHAT_BACKEND.bat

echo 🚀 Starting Todo Chat Backend...
echo.

cd /d "%~dp0backend"

REM Check if virtual environment exists
if not exist "venv\" (
    echo ❌ Virtual environment not found!
    echo Please create it first:
    echo   cd backend
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    exit /b 1
)

echo 📋 Checking configuration...

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found
    echo    Copying from .env.example...
    copy .env.example .env >nul
    echo    ✅ Created .env - please update with your API keys
)

echo.
echo 🔥 Starting Uvicorn server...
echo    Backend will be available at: http://localhost:8000
echo    API docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Start the server
venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
