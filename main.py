#!/usr/bin/env python3
"""
F1 WHO IS BETTER DRIVER? - Main Entry Point

This is a wrapper script that imports and runs the main CLI from the src package.
This maintains backward compatibility while keeping the source code organized.

Usage: python main.py [arguments]
"""

if __name__ == "__main__":
    from src.main import main
    main()