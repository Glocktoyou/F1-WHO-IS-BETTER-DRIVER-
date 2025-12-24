# 🏎️ F1 WHO IS BETTER DRIVER?

> **A comprehensive Formula 1 driver performance analysis tool with interactive web dashboard**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![FastF1](https://img.shields.io/badge/FastF1-3.0+-red.svg)](https://theoehrly.github.io/Fast-F1/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

This project provides **data-driven insights** to answer the eternal F1 question: "Who is the better driver?" Using official Formula 1 telemetry data, advanced analytics, and interactive visualizations, you can compare driver performance across different metrics, sessions, and scenarios.

### Key Features

- 🌐 **Interactive Web Dashboard** - Modern UI for real-time F1 data analysis
- 📊 **8 Visualization Types** - From telemetry traces to G-G diagrams
- 🏁 **Official F1 Data** - Powered by FastF1 API with authentic race data
- ⚡ **Performance Metrics** - Advanced driver analytics and comparison tools
- 📥 **Data Export** - CSV export functionality for further analysis
- 🚀 **Production Ready** - Deployable with proper error handling and logging

## 🏗️ Project Structure

```
├── 📁 Project Root
│   ├── 🐍 Core Application (src/)
│   │   ├── app.py                    # Flask web application (main entry point)
│   │   ├── app_test.py              # Lightweight test version
│   │   ├── main.py                  # CLI entry point  
│   │   ├── data_acquisition.py      # Data loading & session management
│   │   ├── performance_metrics.py   # Driver analytics & metrics
│   │   ├── visualization.py         # Plotting & visualization engine
│   │   └── __init__.py              # Package initialization
│   │
│   ├── 📄 Entry Points (Wrappers)
│   │   ├── app.py                   # Web app wrapper script
│   │   └── main.py                  # CLI wrapper script
│   │
│   ├── 🌐 Web Interface
│   │   ├── templates/               # HTML templates
│   │   │   ├── base.html           # Base template
│   │   │   ├── index.html          # Main dashboard
│   │   │   └── error.html          # Error handling
│   │   └── static/                 # Static assets
│   │       ├── css/style.css       # Custom styling
│   │       └── plots/              # Generated plot images
│   │
│   ├── 🧪 Testing & Examples
│   │   ├── tests/                  # Unit tests & sample data
│   │   │   ├── test_api.py         # API testing
│   │   │   ├── test_manual.py      # Manual testing utilities
│   │   │   └── test_*.py           # Unit test modules
│   │   └── examples/               # Usage examples
│   │
│   ├── 📊 Data & Cache
│   │   ├── cache/                   # FastF1 cache (auto-generated)
│   │   └── outputs/                 # Generated files
│   │       ├── data/               # CSV exports
│   │       └── web/                # Web app outputs
│   │
│   └── ⚙️ Configuration
│       ├── requirements.txt         # Python dependencies
│       ├── environment.yml          # Conda environment
│       ├── .env.example            # Environment variables template
│       ├── Procfile                # Heroku/Render deployment
│       ├── runtime.txt             # Python version specification
│       └── start_web.*             # Startup scripts
```

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)

```bash
# Clone the repository
git clone https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-.git
cd F1-WHO-IS-BETTER-DRIVER-

# Install dependencies
pip install -r requirements.txt

# Run the web application
python app.py

# Visit http://localhost:5000
```

### Option 2: Command Line Interface

```bash
# Basic driver analysis
python main.py --year 2024 --track Monaco --session Q --driver VER --lap fastest --plot trace

# Compare two drivers
python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot compare

# Export data to CSV
python main.py --year 2024 --track Monaco --session Q --driver VER --export --output verstappen_data.csv
```

## 📊 Visualization Gallery

| Visualization Type | Description | Use Case |
|-------------------|-------------|----------|
| 🏁 **Telemetry Trace** | Speed, throttle, brake traces with sectors | Individual driver analysis |
| ⚖️ **Driver Comparison** | Side-by-side telemetry comparison | Direct driver vs driver |
| 📈 **Speed Delta** | Speed and time differences | Performance gaps analysis |
| 🎯 **G-G Diagram** | Lateral vs longitudinal g-forces | Driving style comparison |
| 🏃‍♂️ **Corner Analysis** | Entry, apex, exit speeds per corner | Track-specific performance |
| ⚙️ **Gear Usage Map** | Track colored by gear selection | Technical analysis |
| 🚦 **Brake Map** | Track colored by brake intensity | Braking point analysis |
| 🗺️ **Track Map** | Customizable track visualization | General track overview |

## 💻 Technology Stack

### Backend & Analysis
- **Python 3.10+** - Core language
- **Flask 2.0+** - Web framework
- **FastF1 3.0+** - Official F1 data API
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **matplotlib** - Visualization engine

### Frontend
- **Bootstrap 5** - UI framework
- **JavaScript (ES6+)** - Interactive functionality
- **HTML5/CSS3** - Modern web standards

### Deployment & DevOps
- **Gunicorn** - WSGI HTTP Server
- **Render/Heroku** - Cloud deployment platforms

## 📈 Usage Guide

### Web Interface Features

1. **Session Selection**
   - Choose F1 season year (2021-2024+)
   - Select track/circuit from dropdown
   - Pick session type (FP1/FP2/FP3/Q/S/R)

2. **Driver Analysis**
   - Select primary driver for analysis
   - Choose comparison driver (optional)
   - Pick lap type (fastest/first/last)

3. **Visualization & Export**
   - Generate real-time plots
   - Export telemetry data as CSV
   - Save high-quality images (300 DPI)

### CLI Parameters Reference

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `--year` | int | F1 season year | `2024` |
| `--track` | str | Track name or round number | `Monaco` or `7` |
| `--session` | str | Session type | `Q`, `R`, `FP1` |
| `--driver` | str | Primary driver (3-letter code) | `VER`, `HAM` |
| `--compare` | str | Comparison driver | `NOR`, `LEC` |
| `--lap` | str | Lap selection | `fastest`, `first`, `last` |
| `--plot` | str | Visualization type | `trace`, `compare`, `delta` |
| `--export` | flag | Export to CSV | |
| `--output` | str | Output filename | `analysis_result.csv` |

## 🔧 Development Setup

### Prerequisites
- Python 3.10 or newer
- Git
- (Optional) Conda for environment management

### Installation

1. **Clone and setup**:
   ```bash
   git clone https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-.git
   cd F1-WHO-IS-BETTER-DRIVER-
   ```

2. **Virtual environment (recommended)**:
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # OR using conda
   conda env create -f environment.yml
   conda activate f1-analysis
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your preferences
   ```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Specific test modules
python -m pytest tests/test_data_acquisition.py
python -m pytest tests/test_performance_metrics.py
python -m pytest tests/test_visualization.py

# Manual API testing
python test_api.py
python test_manual.py
```

## 🌐 Deployment

### Local Production Server

```bash
# Using Gunicorn
gunicorn --bind 0.0.0.0:5000 app:app

# Using provided scripts
./start_web.sh      # Linux/macOS
start_web.bat       # Windows
```

### Cloud Deployment (Render/Heroku)

The project includes deployment configuration:
- `Procfile` - Process configuration
- `runtime.txt` - Python version specification
- `requirements.txt` - Dependencies

Simply connect your GitHub repository to your preferred platform.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python -m pytest`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Include type hints where appropriate

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[FastF1](https://theoehrly.github.io/Fast-F1/)** - Excellent F1 data access library
- **Formula 1** - For providing the telemetry data
- **The F1 Community** - For inspiration and feedback

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-/discussions)

---

**Made with ❤️ for F1 fans and data enthusiasts**
