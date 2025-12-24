"""
F1 Data Analysis Web Application

A Flask-based web interface for F1 telemetry data analysis and visualization.
Provides an interactive dashboard for users to explore F1 data without CLI.
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import fastf1
import pandas as pd
import numpy as np
import os
import json
import uuid
from pathlib import Path
from datetime import datetime
import traceback
import logging
from threading import Lock

# Import our existing modules
from .data_acquisition import F1DataLoader
from .performance_metrics import DriverPerformanceAnalyzer
from .visualization import (
    plot_throttle_brake_trace,
    plot_driver_comparison,
    plot_speed_delta,
    plot_gg_diagram,
    plot_corner_analysis,
    plot_gear_usage_map,
    plot_brake_usage_map,
    plot_colored_track_map
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = 'f1-analysis-secret-key-change-in-production'

# Global data loader instance
data_loader = F1DataLoader(cache_dir='cache')
loader_lock = Lock()

# Ensure output directories exist
Path('outputs/web').mkdir(parents=True, exist_ok=True)
Path('static/plots').mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/tracks/<int:year>')
def get_tracks(year):
    """Get available tracks for a given year"""
    try:
        schedule = fastf1.get_event_schedule(year)
        tracks = []
        for idx, row in schedule.iterrows():
            # Skip pre-season testing and other non-race events
            if row.get('EventFormat', '').lower() == 'testing':
                continue
                
            # Handle different possible column names
            event_name = row.get('EventName', row.get('Event', ''))
            location = row.get('Location', row.get('Country', ''))
            round_number = row.get('RoundNumber', row.get('Round', idx + 1))
            
            # Skip events with round number 0 (usually testing)
            if int(round_number) <= 0:
                continue
            
            tracks.append({
                'round': int(round_number),
                'name': str(event_name),
                'location': str(location),
                'date': str(row.get('EventDate', ''))
            })
        
        # Sort by round number
        tracks.sort(key=lambda x: x['round'])
        return jsonify({'success': True, 'tracks': tracks})
    except Exception as e:
        logger.error(f"Error getting tracks for {year}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/drivers')
def get_drivers():
    """Get available drivers for the current session"""
    try:
        if data_loader.session is None:
            return jsonify({'success': False, 'error': 'No session loaded'})
        
        drivers = data_loader.get_all_drivers()
        if not drivers:
            return jsonify({'success': False, 'error': 'No drivers found in session'})
        
        return jsonify({'success': True, 'drivers': drivers})
    except Exception as e:
        logger.error(f"Error getting drivers: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/load_session', methods=['POST'])
def load_session():
    """Load F1 session data"""
    try:
        data = request.json
        year = int(data['year'])
        track = data['track']
        session_type = data['session']
        
        with loader_lock:
            session = data_loader.load_session(year, track, session_type)
            session_info = data_loader.get_session_info()
            drivers = data_loader.get_all_drivers()
        
        return jsonify({
            'success': True,
            'session_info': session_info,
            'drivers': drivers
        })
    except Exception as e:
        logger.error(f"Error loading session: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """Perform data analysis and generate visualizations"""
    try:
        data = request.json
        driver = data['driver'].upper()
        lap_type = data.get('lap_type', 'fastest')
        plot_type = data.get('plot_type', 'trace')
        compare_driver = data.get('compare_driver', '').upper() if data.get('compare_driver') else None
        
        if data_loader.session is None:
            return jsonify({'success': False, 'error': 'No session loaded'})
        
        if not data_loader.validate_driver_code(driver):
            return jsonify({'success': False, 'error': f'Driver {driver} not found in session'})
        
        # Generate unique filename for this analysis
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plot_id = f"{driver}_{plot_type}_{timestamp}_{uuid.uuid4().hex[:8]}"
        plot_path = f"static/plots/{plot_id}.png"
        
        # Get driver lap and telemetry
        lap = data_loader.get_driver_lap(driver, lap_type=lap_type)
        telemetry = data_loader.get_telemetry(lap)
        
        # Generate visualization based on plot type
        if plot_type == 'trace':
            # Create lap info for trace plot
            lap_info = {
                'lap_number': lap.get('LapNumber', '?'),
                'lap_time': lap.get('LapTime', '?'),
                'sector1_end': telemetry['Distance'].max() / 3,
                'sector2_end': 2 * telemetry['Distance'].max() / 3,
                'sector3_end': telemetry['Distance'].max()
            }
            
            # Assign sectors to telemetry
            if 'Sector' not in telemetry:
                telemetry = telemetry.copy()
                telemetry['Sector'] = 1
                telemetry.loc[telemetry['Distance'] > lap_info['sector1_end'], 'Sector'] = 2
                telemetry.loc[telemetry['Distance'] > lap_info['sector2_end'], 'Sector'] = 3
            
            plot_throttle_brake_trace(telemetry, lap_info, driver, save_path=plot_path)
            
        elif plot_type == 'compare' and compare_driver:
            if not data_loader.validate_driver_code(compare_driver):
                return jsonify({'success': False, 'error': f'Compare driver {compare_driver} not found'})
            
            lap2 = data_loader.get_driver_lap(compare_driver, lap_type=lap_type)
            telemetry2 = data_loader.get_telemetry(lap2)
            plot_driver_comparison(telemetry, telemetry2, driver, compare_driver, save_path=plot_path)
            
        elif plot_type == 'delta' and compare_driver:
            if not data_loader.validate_driver_code(compare_driver):
                return jsonify({'success': False, 'error': f'Compare driver {compare_driver} not found'})
            
            lap2 = data_loader.get_driver_lap(compare_driver, lap_type=lap_type)
            telemetry2 = data_loader.get_telemetry(lap2)
            plot_speed_delta(telemetry, telemetry2, driver, compare_driver, save_path=plot_path)
            
        elif plot_type == 'gg':
            if 'GforceLat' not in telemetry or 'GforceLong' not in telemetry:
                return jsonify({'success': False, 'error': 'G-force data not available for this session'})
            plot_gg_diagram(telemetry, driver, save_path=plot_path)
            
        elif plot_type == 'corners':
            # Generate corner locations (simplified)
            n_corners = 10
            dists = telemetry['Distance']
            corner_locations = [dists.min() + i * (dists.max() - dists.min()) / n_corners for i in range(1, n_corners+1)]
            plot_corner_analysis(telemetry, corner_locations, driver, save_path=plot_path)
            
        elif plot_type == 'gearmap':
            plot_gear_usage_map(telemetry, driver, save_path=plot_path)
            
        elif plot_type == 'brakemap':
            plot_brake_usage_map(telemetry, driver, save_path=plot_path)
            
        elif plot_type == 'trackmap':
            color_by = data.get('color_by', 'nGear')
            plot_colored_track_map(data_loader.session, telemetry, color_by=color_by, driver_label=driver, save_path=plot_path)
        
        else:
            return jsonify({'success': False, 'error': f'Unknown plot type: {plot_type}'})
        
        # Calculate performance metrics with safe numeric conversion
        def safe_round(value, decimals=2):
            """Safely round numeric values, handle numpy types and NaN"""
            try:
                if pd.isna(value) or value is None:
                    return 0.0
                # Convert numpy types to Python types
                if hasattr(value, 'item'):
                    value = value.item()
                # Handle boolean values
                if isinstance(value, (bool, np.bool_)):
                    return float(value)
                return round(float(value), decimals)
            except (TypeError, ValueError, AttributeError):
                return 0.0

        analyzer = DriverPerformanceAnalyzer(telemetry)
        metrics = {
            'full_throttle_percentage': safe_round(analyzer.full_throttle_percentage()),
            'coasting_time_percentage': safe_round(analyzer.coasting_time_percentage()),
            'throttle_smoothness': safe_round(analyzer.throttle_smoothness()),
            'max_speed': safe_round(telemetry['Speed'].max()),
            'min_speed': safe_round(telemetry['Speed'].min()),
            'avg_speed': safe_round(telemetry['Speed'].mean()),
            'max_brake': safe_round(telemetry['Brake'].max()),
            'max_throttle': safe_round(telemetry['Throttle'].max())
        }
        
        return jsonify({
            'success': True,
            'plot_url': f'/{plot_path}',
            'metrics': metrics,
            'lap_info': {
                'lap_number': str(lap.get('LapNumber', '?')),
                'lap_time': str(lap.get('LapTime', '?')),
                'driver': driver
            }
        })
        
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/export_csv', methods=['POST'])
def export_csv():
    """Export telemetry data to CSV"""
    try:
        data = request.json
        driver = data['driver'].upper()
        lap_type = data.get('lap_type', 'fastest')
        
        if data_loader.session is None:
            return jsonify({'success': False, 'error': 'No session loaded'})
        
        # Get telemetry
        lap = data_loader.get_driver_lap(driver, lap_type=lap_type)
        telemetry = data_loader.get_telemetry(lap)
        
        # Export to CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{driver.lower()}_{timestamp}.csv"
        csv_path = data_loader.export_to_csv(telemetry, filename, output_dir='outputs/web')
        
        return jsonify({
            'success': True,
            'download_url': f'/download/{filename}',
            'filename': filename
        })
        
    except Exception as e:
        logger.error(f"Error exporting CSV: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<filename>')
def download_file(filename):
    """Download exported CSV files"""
    try:
        file_path = Path('outputs/web') / filename
        if file_path.exists():
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error='Internal server error'), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)