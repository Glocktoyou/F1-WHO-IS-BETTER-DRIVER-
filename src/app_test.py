"""
Simple test version of the F1 Analysis Web App
"""
from flask import Flask, render_template, jsonify
import os
from pathlib import Path

# Create Flask app
app = Flask(__name__)
app.secret_key = 'test-key'

# Ensure directories exist
Path('static/plots').mkdir(parents=True, exist_ok=True)
Path('outputs/web').mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    """Test homepage"""
    return render_template('index.html')

@app.route('/api/test')
def test():
    """Test API endpoint"""
    return jsonify({'success': True, 'message': 'Web application is working!'})

if __name__ == '__main__':
    print("Starting simple test version...")
    app.run(debug=True, host='127.0.0.1', port=5000)