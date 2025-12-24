#!/usr/bin/env bash
# Install system dependencies if needed
# pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p static/plots
mkdir -p outputs/web
mkdir -p cache

# Start the application
exec gunicorn app:app --bind 0.0.0.0:$PORT