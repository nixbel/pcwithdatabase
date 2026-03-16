@echo off
REM Quick Start Script for Campaign Application with PostgreSQL Database

echo ========================================
echo Campaign Application - Database Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if PostgreSQL is running
echo [1/4] Checking PostgreSQL connection...
psql -U postgres -c "SELECT 1" >nul 2>&1
if errorlevel 1 (
    echo WARNING: PostgreSQL may not be running!
    echo Please start PostgreSQL and ensure it's running on port 5432
    echo.
    pause
)

REM Install/Update dependencies
echo [2/4] Installing/Updating dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Initialize database tables
echo [3/4] Initializing database tables...
python -c "from database.init_db import init_db; init_db()" 2>nul
python -c "from database.login_operations import create_login_attempts_table; create_login_attempts_table()" 2>nul

REM Start Flask application
echo [4/4] Starting Flask application...
echo.
echo ========================================
echo Application is starting...
echo ========================================
echo.
echo Access the application at: http://localhost:5000
echo.
echo Press CTRL+C to stop the application
echo ========================================
echo.

cd campaign
python app.py

pause
