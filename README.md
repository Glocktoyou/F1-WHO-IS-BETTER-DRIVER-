
# F1 Data Analysis Web Application

A modern web-based Formula 1 telemetry analysis tool built with Python, Flask, and FastF1. 

## 🏎️ Features

- **Interactive Web Dashboard**: User-friendly interface for F1 data analysis
- **Multiple Visualizations**: 8 different plot types including telemetry traces, driver comparisons, and brake maps
- **Real F1 Data**: Uses official FastF1 API for authentic race data
- **Performance Metrics**: Advanced analytics on driver performance
- **Data Export**: CSV export functionality for further analysis

## 📊 Visualization Types

1. **Telemetry Trace**: Speed, throttle, and brake traces with sector boundaries
2. **Driver Comparison**: Side-by-side telemetry comparison between drivers
3. **Speed Delta**: Speed and time differences between drivers
4. **G-G Diagram**: Lateral vs longitudinal g-forces analysis
5. **Corner Analysis**: Entry, apex, and exit speeds per corner
6. **Gear Usage Map**: Track visualization colored by gear selection
7. **Brake Usage Map**: Track visualization colored by brake intensity
8. **Track Map**: Customizable track visualization with various telemetry channels

## 🚀 Live Demo

This application is deployed and accessible at: [Your Render URL will go here]

## 💻 Technology Stack

- **Backend**: Python, Flask
- **Data Analysis**: pandas, numpy, FastF1
- **Visualization**: matplotlib
- **Frontend**: Bootstrap 5, JavaScript, HTML5/CSS3
- **Deployment**: Gunicorn, Render

## 🛠️ Local Development

```bash
git clone [your-repo-url]
cd data-analysis
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` to use the application locally.

## 📈 Usage

1. Select a Formula 1 season year (2021-2024)
2. Choose a track/circuit from the available races  
3. Pick session type (Practice, Qualifying, Sprint, Race)
4. Select driver(s) for analysis
5. Choose visualization type and generate insights
6. Export data or save high-quality plots

## 🎯 Project Highlights

- **Real-world Data**: Works with actual F1 telemetry from official sources
- **Professional UI/UX**: Modern, responsive web interface
- **Scalable Architecture**: Clean separation of data, analysis, and visualization layers
- **Production Ready**: Deployed with proper error handling and logging
- **Performance Optimized**: Efficient data processing and caching

Built as a demonstration of full-stack development skills combined with domain expertise in motorsport data analysis.

## Project Structure
```
app.py                     # Flask web application (main entry point)
app_test.py               # Simple test version of web app
data_acquisition.py       # Data loading and session management
performance_metrics.py    # Driver performance analysis and metrics
visualization.py          # Plotting and visualization functions
main.py                   # CLI entry point
start_web.bat            # Windows startup script
start_web.sh             # Linux/Mac startup script
cache/                   # FastF1 cache (auto-generated)
outputs/data/            # Exported telemetry CSVs
outputs/web/             # Web application CSV exports
static/css/              # Web interface styling
static/plots/            # Generated plot images for web
templates/               # HTML templates for web interface
tests/                   # Unit tests and sample/mock data
```

## Web Interface Features

The web interface provides an intuitive dashboard with:

### Session Management
- **Dynamic Track Loading**: Automatically loads available tracks for selected year
- **Session Information**: Displays loaded session details and driver list
- **Real-time Validation**: Ensures valid combinations before analysis

### Interactive Controls
- **Driver Selection**: Dropdown with all available drivers in the session  
- **Lap Type Options**: Fastest lap, first lap, or last lap analysis
- **Visualization Types**: 7 different plot types with automatic UI adaptation
- **Smart UI**: Controls adapt based on selected visualization (e.g., comparison driver selection)

### Performance Dashboard
- **Live Metrics**: Displays key performance indicators during analysis
- **Speed Statistics**: Max, min, and average speeds
- **Driving Style Metrics**: Throttle usage, coasting time, smoothness
- **Professional Formatting**: Clean, organized metric display

### Data Export
- **One-Click CSV Export**: Download telemetry data for external analysis
- **High-Quality Plots**: 300 DPI images suitable for reports
- **Automatic Naming**: Intelligent file naming with timestamps

## Dependencies & Environment Setup

**Python Version:**
- Python 3.10 or newer is recommended.

**Required Packages:**
- fastf1
- pandas
- numpy
- matplotlib

You can install all dependencies using either pip (requirements.txt) or conda (environment.yml).

---


## Setup & Installation
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd data-analysis
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # Or with conda:
   conda env create -f environment.yml
   conda activate f1-driver-performance-analysis
   ```
3. **(Optional) Enable FastF1 cache:**
   The cache directory is auto-created as `cache/`.


## Usage

### Command-Line Interface
Run the main script with desired options:
```bash
python main.py --year 2024 --track Monaco --session Q --driver VER --lap fastest --plot trace
```

#### Key CLI Options
- `--year` (int): F1 season year (e.g., 2024)
- `--track` (str): Track/circuit name or round number (e.g., Monaco or 7)
- `--session` (str): Session type (`FP1`, `FP2`, `FP3`, `Q`, `S`, `R`)
- `--driver` (str): Three-letter driver code (e.g., VER, HAM)
- `--lap` (str): Lap type (`fastest`, `first`, `last`)
- `--compare` (str): Compare with another driver (three-letter code)
- `--plot` (str): Plot type (`trace`, `compare`, `delta`, `gg`, `corners`, `gearmap`, `trackmap`)
- `--export`: Export telemetry to CSV
- `--output` (str): Output file name for CSV or plot
- `--list-tracks`: List available tracks for the given year
- `--all-laps`: Analyze all laps for the driver

#### Example: Compare Two Drivers
```bash
python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot compare
```

#### Example: Export Telemetry to CSV
```bash
python main.py --year 2024 --track Monaco --session Q --driver VER --export --output verstappen_monaco_q.csv
```

#### Example: Generate a GG Diagram
```bash
python main.py --year 2024 --track Monaco --session Q --driver HAM --plot gg --output hamilton_gg.png
```

#### Example Output/Plots
- See outputs/data/ for sample CSVs
- See outputs/web/ for sample images (if generated)


## Example Plots

![Throttle/Brake Trace](outputs/web/sample_trace.png)
![Driver Comparison](outputs/web/sample_compare.png)
![Speed Delta](outputs/web/sample_delta.png)
![GG Diagram](outputs/web/sample_gg.png)

*(See outputs/data/ for sample CSVs and outputs/web/ for more images if generated)*

## Advanced Usage
- **Multi-lap Analysis:** Use `--all-laps` to analyze all laps for a driver (average lap time, stint summary, etc.).
- **Custom Plots:** Extend `visualization.py` to add new plot types or customize existing ones.
- **Web Dashboard:** (Optional) Integrate with Streamlit or Dash for interactive analysis.

## Dependencies
- [FastF1](https://theoehrly.github.io/Fast-F1/)
- pandas
- numpy
- matplotlib

## Contributing
Contributions are welcome! Please open issues or pull requests for improvements, bug fixes, or new features.

## License
MIT License. See LICENSE file for details.

## Acknowledgments
- [FastF1](https://theoehrly.github.io/Fast-F1/) for F1 data access
- Formula 1 for the data

---
For questions or collaboration, contact: <your-email-or-linkedin>
