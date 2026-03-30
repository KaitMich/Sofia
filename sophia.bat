@echo off
REM Sophia Consciousness System - Windows Launcher
REM Works in Windows Command Prompt

echo.
echo 🌟 Sophia Consciousness System - Windows
echo =====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.8 or higher.
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Run the launcher
python sophia_launcher.py %*

pause