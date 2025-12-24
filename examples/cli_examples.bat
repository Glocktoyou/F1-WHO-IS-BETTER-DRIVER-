@echo off
REM F1 WHO IS BETTER DRIVER? - CLI Usage Examples (Windows)
REM This batch script demonstrates various CLI commands for F1 analysis

echo 🏎️  F1 WHO IS BETTER DRIVER? - CLI Examples
echo ===========================================
echo.

REM Example 1: Basic driver analysis
echo 📊 Example 1: Basic Driver Telemetry Analysis
echo ----------------------------------------------
echo Command: python main.py --year 2024 --track Monaco --session Q --driver VER --lap fastest --plot trace
echo.
python main.py --year 2024 --track Monaco --session Q --driver VER --lap fastest --plot trace
echo.

pause

REM Example 2: Driver comparison
echo 🆚 Example 2: Driver Comparison
echo --------------------------------
echo Command: python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot compare
echo.
python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot compare
echo.

pause

REM Example 3: Speed delta analysis
echo 📈 Example 3: Speed Delta Analysis
echo ----------------------------------
echo Command: python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot delta
echo.
python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot delta
echo.

pause

REM Example 4: Data export
echo 💾 Example 4: Export Telemetry Data
echo -----------------------------------
echo Command: python main.py --year 2024 --track Monaco --session Q --driver VER --export --output verstappen_monaco.csv
echo.
python main.py --year 2024 --track Monaco --session Q --driver VER --export --output verstappen_monaco.csv
echo.

pause

REM Example 5: List tracks
echo 📋 Example 5: List Available Tracks
echo -----------------------------------
echo Command: python main.py --year 2024 --list-tracks
echo.
python main.py --year 2024 --list-tracks
echo.

pause

echo.
echo ✨ CLI Examples Complete!
echo.
echo 💡 Additional Tips:
echo    • Use --help for full parameter list
echo    • Check outputs\ directory for generated files
echo    • Try different years, tracks, and drivers
echo.
echo 🌐 Start the web interface: python app.py

pause