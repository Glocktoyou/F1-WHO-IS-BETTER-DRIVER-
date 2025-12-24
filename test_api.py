#!/usr/bin/env python3

"""
Test script for F1 Data Analysis Web API endpoints
"""

import requests
import json
import sys
import time
from pathlib import Path

def test_api_endpoint(url, description):
    """Test a specific API endpoint"""
    print(f"\n=== Testing {description} ===")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)[:500]}...")
            return True
        else:
            print(f"Error Response: {response.text}")
            return False
    except Exception as e:
        print(f"Request failed: {e}")
        return False

def main():
    base_url = "http://127.0.0.1:5000"
    
    print("F1 Data Analysis Web API Test")
    print("=" * 40)
    
    # Test if server is running
    try:
        response = requests.get(base_url, timeout=5)
        print(f"✓ Server is running (Status: {response.status_code})")
    except:
        print("✗ Server is not running or not accessible")
        print("Please start the Flask app first with: python app.py")
        sys.exit(1)
    
    # Test tracks API
    success = test_api_endpoint(f"{base_url}/api/tracks/2024", "Get 2024 Tracks")
    
    if success:
        print("\n✓ API test completed successfully!")
    else:
        print("\n✗ API test failed!")

if __name__ == "__main__":
    main()