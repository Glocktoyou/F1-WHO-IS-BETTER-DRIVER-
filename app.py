#!/usr/bin/env python3
"""
F1 WHO IS BETTER DRIVER? - Web Application Entry Point

This is a wrapper script that imports and runs the Flask web app from the src package.
This maintains backward compatibility while keeping the source code organized.

Usage: python app.py
"""

if __name__ == "__main__":
    from src.app import app
    app.run(debug=True, host='0.0.0.0', port=5000)