# API Documentation - F1 WHO IS BETTER DRIVER?

This document provides detailed information about the web API endpoints and CLI interface for the F1 driver analysis tool.

## 🌐 Web API Endpoints

The Flask web application exposes several API endpoints for programmatic access to F1 data and analysis.

### Base URL
```
http://localhost:5000  # Local development
https://your-domain.com  # Production deployment
```

### Authentication
Currently, no authentication is required for API access.

---

## 📊 Data Endpoints

### Get Available Tracks
**Endpoint:** `GET /api/tracks/{year}`

**Description:** Retrieve all available F1 tracks for a given season.

**Parameters:**
- `year` (path, integer): F1 season year (e.g., 2024)

**Example Request:**
```bash
curl -X GET "http://localhost:5000/api/tracks/2024"
```

**Example Response:**
```json
{
  "year": 2024,
  "tracks": [
    {
      "round": 1,
      "track_name": "Bahrain International Circuit",
      "location": "Bahrain",
      "country": "Bahrain",
      "date": "2024-03-02"
    },
    {
      "round": 7,
      "track_name": "Circuit de Monaco",
      "location": "Monaco",
      "country": "Monaco", 
      "date": "2024-05-26"
    }
  ],
  "total_tracks": 24
}
```

**Error Response:**
```json
{
  "error": "Invalid year provided",
  "message": "Year must be between 2018 and current year"
}
```

---

### Get Session Information
**Endpoint:** `GET /api/session/{year}/{track}/{session}`

**Description:** Get detailed information about a specific F1 session.

**Parameters:**
- `year` (path, integer): F1 season year
- `track` (path, string): Track name or round number
- `session` (path, string): Session type (`FP1`, `FP2`, `FP3`, `Q`, `S`, `R`)

**Example Request:**
```bash
curl -X GET "http://localhost:5000/api/session/2024/Monaco/Q"
```

**Example Response:**
```json
{
  "session_info": {
    "year": 2024,
    "track": "Monaco",
    "session": "Qualifying",
    "date": "2024-05-25",
    "weather": "Dry",
    "track_temp": 42.5,
    "air_temp": 28.3
  },
  "drivers": [
    {
      "code": "VER",
      "full_name": "Max Verstappen",
      "team": "Red Bull Racing",
      "number": 1
    },
    {
      "code": "HAM", 
      "full_name": "Lewis Hamilton",
      "team": "Mercedes",
      "number": 44
    }
  ],
  "total_drivers": 20
}
```

---

### Get Driver Telemetry
**Endpoint:** `POST /api/telemetry`

**Description:** Retrieve telemetry data for specific driver and lap.

**Request Body:**
```json
{
  "year": 2024,
  "track": "Monaco",
  "session": "Q",
  "driver": "VER",
  "lap_type": "fastest",
  "compare_driver": "HAM"  // Optional
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:5000/api/telemetry" \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2024,
    "track": "Monaco", 
    "session": "Q",
    "driver": "VER",
    "lap_type": "fastest"
  }'
```

**Example Response:**
```json
{
  "driver_info": {
    "code": "VER",
    "full_name": "Max Verstappen",
    "lap_time": "1:10.270",
    "lap_number": 18
  },
  "telemetry": [
    {
      "distance": 0.0,
      "speed": 0,
      "throttle": 0,
      "brake": False,
      "gear": 1,
      "rpm": 12000,
      "drs": 0
    },
    {
      "distance": 25.5,
      "speed": 89,
      "throttle": 98,
      "brake": False,
      "gear": 3,
      "rpm": 11800,
      "drs": 0
    }
  ],
  "performance_metrics": {
    "max_speed": 285.4,
    "min_speed": 48.2,
    "avg_speed": 158.7,
    "max_throttle": 100,
    "total_braking_time": 8.45,
    "smoothness_index": 0.87
  }
}
```

---

## 🎨 Visualization Endpoints

### Generate Plot
**Endpoint:** `POST /api/plot`

**Description:** Generate visualization plots for F1 data analysis.

**Request Body:**
```json
{
  "year": 2024,
  "track": "Monaco",
  "session": "Q",
  "driver": "VER",
  "plot_type": "trace",
  "lap_type": "fastest",
  "compare_driver": "HAM",  // Optional, for comparison plots
  "export_format": "png"    // png, jpg, svg
}
```

**Plot Types:**
- `trace` - Telemetry trace (speed, throttle, brake)
- `compare` - Driver comparison
- `delta` - Speed delta analysis
- `gg` - G-G diagram
- `corners` - Corner analysis
- `gearmap` - Gear usage map
- `brakemap` - Brake usage map
- `trackmap` - Track visualization

**Example Request:**
```bash
curl -X POST "http://localhost:5000/api/plot" \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2024,
    "track": "Monaco",
    "session": "Q", 
    "driver": "VER",
    "plot_type": "trace",
    "lap_type": "fastest"
  }'
```

**Example Response:**
```json
{
  "plot_info": {
    "type": "trace",
    "driver": "VER",
    "track": "Monaco",
    "session": "Q",
    "lap_time": "1:10.270"
  },
  "file_info": {
    "filename": "VER_trace_20241224_142530_abc123.png",
    "url": "/static/plots/VER_trace_20241224_142530_abc123.png",
    "size": "1.2MB",
    "dimensions": "1920x1080"
  },
  "metrics": {
    "max_speed": 285.4,
    "braking_points": 12,
    "throttle_application": "92.3%"
  }
}
```

---

### Export Data
**Endpoint:** `POST /api/export`

**Description:** Export telemetry data in various formats.

**Request Body:**
```json
{
  "year": 2024,
  "track": "Monaco",
  "session": "Q",
  "driver": "VER",
  "lap_type": "fastest",
  "format": "csv",  // csv, json, excel
  "include_metrics": true
}
```

**Example Response:**
```json
{
  "export_info": {
    "filename": "VER_monaco_q_fastest_20241224.csv",
    "url": "/outputs/web/VER_monaco_q_fastest_20241224.csv",
    "size": "2.5MB",
    "rows": 15420,
    "columns": 12
  },
  "metadata": {
    "exported_at": "2024-12-24T14:25:30Z",
    "lap_time": "1:10.270",
    "track_length": 3337.0
  }
}
```

---

## 💻 CLI Interface

### Basic Usage
```bash
python main.py [options]
```

### Core Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `--year` | int | Yes | F1 season year | `2024` |
| `--track` | str | Yes | Track name or round | `Monaco`, `7` |
| `--session` | str | Yes | Session type | `Q`, `R`, `FP1` |
| `--driver` | str | Yes | Driver code (3-letter) | `VER`, `HAM` |
| `--lap` | str | No | Lap selection | `fastest` (default), `first`, `last` |

### Analysis Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `--compare` | str | No | Comparison driver | `HAM`, `LEC` |
| `--plot` | str | No | Visualization type | `trace`, `compare`, `delta` |
| `--export` | flag | No | Export telemetry to CSV | |
| `--output` | str | No | Output filename | `analysis.csv` |
| `--all-laps` | flag | No | Analyze all laps | |

### Utility Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `--list-tracks` | flag | List available tracks for year | |
| `--list-drivers` | flag | List drivers for session | |
| `--cache-info` | flag | Show cache information | |
| `--verbose` | flag | Enable verbose output | |
| `--help` | flag | Show help message | |

### CLI Examples

**Basic driver analysis:**
```bash
python main.py --year 2024 --track Monaco --session Q --driver VER --lap fastest --plot trace
```

**Compare two drivers:**
```bash
python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot compare
```

**Export telemetry data:**
```bash
python main.py --year 2024 --track Monaco --session Q --driver VER --export --output verstappen_monaco.csv
```

**Generate specific visualization:**
```bash
python main.py --year 2024 --track Monaco --session Q --driver HAM --plot gg --output hamilton_gg.png
```

**List available tracks:**
```bash
python main.py --year 2024 --list-tracks
```

**Analyze all laps for driver:**
```bash
python main.py --year 2024 --track Monaco --session R --driver VER --all-laps --export
```

### CLI Output Examples

**Successful Analysis:**
```
✅ Session loaded: 2024 Monaco GP - Qualifying
🏎️  Driver: Max Verstappen (VER) - Red Bull Racing
⏱️  Fastest lap: 1:10.270 (Lap 18)
📊 Generating telemetry trace plot...
💾 Plot saved: outputs/plots/VER_trace_20241224_142530.png

📈 Performance Metrics:
   Max Speed: 285.4 km/h
   Avg Speed: 158.7 km/h
   Throttle Usage: 92.3%
   Braking Time: 8.45s
   Smoothness Index: 0.87

✨ Analysis complete!
```

**Error Handling:**
```
❌ Error: Driver 'ABC' not found in 2024 Monaco GP Qualifying
Available drivers: VER, HAM, LEC, NOR, PER, RUS, ALO, SAI...

Use --list-drivers to see all available drivers for this session.
```

---

## 🔧 Error Codes and Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters provided |
| 404 | Not Found | Requested resource not found |
| 422 | Unprocessable Entity | Valid request but processing failed |
| 500 | Internal Server Error | Server error during processing |

### Common Error Responses

**Invalid Year:**
```json
{
  "error": "INVALID_YEAR",
  "message": "Year 2030 is not available. Available years: 2018-2024",
  "code": 400
}
```

**Driver Not Found:**
```json
{
  "error": "DRIVER_NOT_FOUND", 
  "message": "Driver 'ABC' not found in session",
  "available_drivers": ["VER", "HAM", "LEC"],
  "code": 404
}
```

**Session Load Failed:**
```json
{
  "error": "SESSION_LOAD_ERROR",
  "message": "Unable to load session data. Check internet connection or try again later",
  "code": 422
}
```

---

## 📝 Rate Limiting

Currently, no rate limiting is implemented, but consider implementing it for production deployments to prevent abuse.

**Recommended Limits:**
- API endpoints: 100 requests/hour per IP
- Data export: 10 exports/hour per IP
- Plot generation: 50 plots/hour per IP

---

## 🔌 SDK Integration

For programmatic access, you can use standard HTTP libraries:

**Python:**
```python
import requests

# Get tracks for 2024
response = requests.get('http://localhost:5000/api/tracks/2024')
tracks = response.json()

# Generate plot
plot_data = {
    'year': 2024,
    'track': 'Monaco',
    'session': 'Q',
    'driver': 'VER',
    'plot_type': 'trace'
}
response = requests.post('http://localhost:5000/api/plot', json=plot_data)
```

**JavaScript:**
```javascript
// Get session information
const response = await fetch('/api/session/2024/Monaco/Q');
const sessionData = await response.json();

// Export data
const exportData = {
  year: 2024,
  track: 'Monaco',
  session: 'Q',
  driver: 'VER',
  format: 'csv'
};

const exportResponse = await fetch('/api/export', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(exportData)
});
```

---

For more information, see the main [README.md](README.md) or [CONTRIBUTING.md](CONTRIBUTING.md) files.