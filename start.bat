@echo off
echo ========================================
echo Medical Q&A Chatbot - Quick Start
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found!
echo.

echo Setting up virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running setup...
python setup.py

echo.
echo Starting Medical Chatbot...
echo The application will open in your default browser.
echo Press Ctrl+C to stop the application.
echo.

streamlit run app.py

pause