#!/usr/bin/env python3
"""
Manual test for tracks API functionality
"""

import sys
sys.path.insert(0, '.')

from app import app
import json

def test_tracks_api():
    with app.test_client() as client:
        print("Testing /api/tracks/2024 endpoint...")
        
        response = client.get('/api/tracks/2024')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print("Success! Response data:")
            print(json.dumps(data, indent=2))
            
            if data.get('success') and data.get('tracks'):
                print(f"\n✓ Found {len(data['tracks'])} tracks")
                for track in data['tracks'][:3]:  # Show first 3
                    print(f"  - Round {track['round']}: {track['name']} ({track['location']})")
                if len(data['tracks']) > 3:
                    print(f"  ... and {len(data['tracks']) - 3} more")
            else:
                print("✗ No tracks found in response")
        else:
            print(f"✗ Error: {response.get_data(as_text=True)}")

if __name__ == "__main__":
    test_tracks_api()