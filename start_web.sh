#!/bin/bash

echo "Starting F1 Data Analysis Web Application..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed or not in PATH. Please install Python3 first."
    exit 1
fi

# Install requirements if needed
echo "Installing/updating requirements..."
pip3 install -r requirements.txt

# Create necessary directories
mkdir -p static/plots
mkdir -p outputs/web

# Start the Flask application
echo
echo "Starting web server..."
echo "Open your browser and go to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo

python3 app.py