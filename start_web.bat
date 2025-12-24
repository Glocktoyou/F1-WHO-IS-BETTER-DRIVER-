@echo off
echo Starting F1 Data Analysis Web Application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH. Please install Python first.
    pause
    exit /b 1
)

REM Install requirements if needed
echo Installing/updating requirements...
pip install -r requirements.txt

REM Create necessary directories
if not exist "static\plots" mkdir "static\plots"
if not exist "outputs\web" mkdir "outputs\web"

REM Start the Flask application
echo.
echo Starting web server...
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause