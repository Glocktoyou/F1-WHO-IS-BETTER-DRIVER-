# F1 WHO IS BETTER DRIVER? - Examples

This directory contains example scripts and usage patterns to help you get started with the F1 analysis tool.

## 📁 Files Overview

| File | Description | Usage |
|------|-------------|-------|
| `basic_usage.py` | Python examples demonstrating core functionality | `python examples/basic_usage.py` |
| `cli_examples.sh` | Bash script with CLI command examples | `./examples/cli_examples.sh` |
| `cli_examples.bat` | Windows batch script with CLI examples | `examples\cli_examples.bat` |

## 🚀 Quick Start Examples

### 1. Basic Driver Analysis
Analyze a single driver's performance in a session:

```bash
# CLI approach
python main.py --year 2024 --track Monaco --session Q --driver VER --lap fastest --plot trace

# Python code approach
from src.data_acquisition import F1DataLoader
data_manager = F1DataLoader()
session = data_manager.load_session(2024, "Monaco", "Q")
driver_data = data_manager.get_driver_data(session['session'], "VER", "fastest")
```

### 2. Driver Comparison
Compare two drivers on the same track:

```bash
# CLI
python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot compare

# Python code
from src.performance_metrics import DriverPerformanceAnalyzer
analyzer = DriverPerformanceAnalyzer()
comparison = analyzer.compare_drivers(ver_data, ham_data, "VER", "HAM")
```

### 3. Data Export
Export telemetry data for external analysis:

```bash
# CLI
python main.py --year 2024 --track Monaco --session Q --driver VER --export --output data.csv

# Python code
driver_data['telemetry'].to_csv('verstappen_telemetry.csv', index=False)
```

## 📊 Visualization Examples

### Available Plot Types

| Plot Type | Command | Description |
|-----------|---------|-------------|
| **Telemetry Trace** | `--plot trace` | Speed, throttle, brake traces |
| **Driver Comparison** | `--plot compare` | Side-by-side driver analysis |
| **Speed Delta** | `--plot delta` | Speed differences between drivers |
| **G-G Diagram** | `--plot gg` | Lateral vs longitudinal forces |
| **Corner Analysis** | `--plot corners` | Corner-by-corner performance |
| **Gear Map** | `--plot gearmap` | Track colored by gear usage |
| **Brake Map** | `--plot brakemap` | Track colored by braking intensity |
| **Track Map** | `--plot trackmap` | General track visualization |

### Example Commands

```bash
# Generate telemetry trace for Max Verstappen
python main.py --year 2024 --track Monaco --session Q --driver VER --plot trace

# Compare Verstappen vs Hamilton speed delta
python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot delta

# Create G-G diagram for Lewis Hamilton
python main.py --year 2024 --track Monaco --session Q --driver HAM --plot gg

# Generate gear usage map for the track
python main.py --year 2024 --track Monaco --session Q --driver VER --plot gearmap
```

## 🎯 Common Use Cases

### 1. Qualifying Analysis
Compare pole position performance:

```bash
# See who was faster in Q3
python main.py --year 2024 --track Monaco --session Q --driver VER --compare LEC --plot compare

# Analyze the pole lap in detail
python main.py --year 2024 --track Monaco --session Q --driver VER --lap fastest --plot trace
```

### 2. Race Strategy Analysis
Analyze race performance:

```bash
# Race winner's performance
python main.py --year 2024 --track Monaco --session R --driver VER --lap fastest --plot trace

# Compare race pace
python main.py --year 2024 --track Monaco --session R --driver VER --compare HAM --plot delta
```

### 3. Track-Specific Analysis
Different tracks require different approaches:

```bash
# High-speed circuit (Monza)
python main.py --year 2024 --track Monza --session Q --driver VER --plot trace

# Technical circuit (Monaco)
python main.py --year 2024 --track Monaco --session Q --driver VER --plot gg

# Mixed circuit (Silverstone)
python main.py --year 2024 --track Silverstone --session Q --driver VER --plot corners
```

## 🔧 Advanced Usage

### 1. Batch Analysis
Analyze multiple drivers or sessions:

```bash
# Create a script for multiple drivers
for driver in VER HAM LEC NOR; do
    python main.py --year 2024 --track Monaco --session Q --driver $driver --export --output ${driver}_monaco.csv
done
```

### 2. Custom Analysis
Extend the Python examples:

```python
# Load data for custom analysis
from src.data_acquisition import F1DataLoader
from src.performance_metrics import DriverPerformanceAnalyzer

data_manager = F1DataManager()
analyzer = PerformanceAnalyzer()

# Get session data
session = data_manager.load_session(2024, "Monaco", "Q")

# Analyze all drivers
drivers = ["VER", "HAM", "LEC", "NOR", "PER"]
results = {}

for driver in drivers:
    try:
        driver_data = data_manager.get_driver_data(session['session'], driver, "fastest")
        metrics = analyzer.calculate_basic_metrics(driver_data['telemetry'])
        results[driver] = metrics
    except Exception as e:
        print(f"Could not analyze {driver}: {e}")

# Find fastest driver
fastest_driver = max(results.keys(), key=lambda d: results[d]['max_speed'])
print(f"Fastest top speed: {fastest_driver} ({results[fastest_driver]['max_speed']:.1f} km/h)")
```

## 🌐 Web Interface Examples

Start the web application and use these scenarios:

```bash
# Start the web server
python app.py

# Then visit http://localhost:5000 and try:
```

**Scenario 1: Monaco GP Qualifying**
1. Select Year: 2024
2. Select Track: Monaco
3. Select Session: Qualifying
4. Select Driver: Max Verstappen
5. Choose Visualization: Telemetry Trace
6. Click "Generate Analysis"

**Scenario 2: Driver Comparison**
1. Select Year: 2024
2. Select Track: Monaco
3. Select Session: Qualifying
4. Select Driver: Max Verstappen
5. Select Compare Driver: Lewis Hamilton
6. Choose Visualization: Driver Comparison
7. Click "Generate Analysis"

## 📝 Output Files

Examples will generate files in various locations:

```
examples/
├── output_ver_trace.png          # Generated trace plots
├── output_ver_gg.png             # G-G diagrams
├── verstappen_monaco_q_telemetry.csv  # Exported telemetry data
outputs/
├── data/                         # CLI CSV exports
└── web/                          # Web interface exports
static/
└── plots/                        # Web-generated plots
```

## 🐛 Troubleshooting

### Common Issues

**"Driver not found" Error:**
```bash
# List available drivers first
python main.py --year 2024 --track Monaco --session Q --list-drivers
```

**"No internet connection" Error:**
- FastF1 requires internet to download data
- Data is cached after first download
- Check your internet connection

**"Session not found" Error:**
```bash
# List available tracks for the year
python main.py --year 2024 --list-tracks
```

**Import Errors in Python Examples:**
```bash
# Make sure you're in the project root directory
cd /path/to/F1-WHO-IS-BETTER-DRIVER-
python examples/basic_usage.py
```

## 💡 Tips for Best Results

1. **Start with recent seasons** (2021-2024) for best data availability
2. **Use Qualifying sessions** for clean lap comparisons
3. **Monaco and Monza** are great tracks for learning - very different characteristics
4. **Export data** to CSV for custom analysis in Excel/Python/R
5. **Try different visualization types** - each reveals different insights

## 📞 Need Help?

- Check the main [README.md](../README.md) for full documentation
- Look at [API.md](../API.md) for web API usage
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for development help
- Create an issue on GitHub for bugs or questions

Happy analyzing! 🏎️📊