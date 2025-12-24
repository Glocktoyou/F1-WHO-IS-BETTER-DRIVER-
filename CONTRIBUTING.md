# Contributing to F1 WHO IS BETTER DRIVER?

Thank you for your interest in contributing to this F1 data analysis project! This document outlines how you can help improve the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or newer
- Git
- Basic knowledge of Formula 1 and data analysis concepts

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/F1-WHO-IS-BETTER-DRIVER-.git
   cd F1-WHO-IS-BETTER-DRIVER-
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests to ensure everything works**
   ```bash
   python -m pytest tests/
   python test_manual.py
   ```

## 🎯 Ways to Contribute

### 1. Bug Reports
If you find a bug, please create an issue with:
- Clear bug description
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Error logs/screenshots if applicable

### 2. Feature Requests
We welcome new feature ideas! Please include:
- Clear description of the feature
- Use case and benefits
- Implementation suggestions (if any)

### 3. Code Contributions

#### Areas for Improvement
- **New Visualizations**: Additional plot types for F1 analysis
- **Performance Metrics**: New driver comparison algorithms
- **Web Interface**: UI/UX improvements
- **Data Processing**: Optimization and new data sources
- **Testing**: More comprehensive test coverage
- **Documentation**: Examples and tutorials

#### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   python -m pytest tests/
   python test_api.py
   python app_test.py  # Test web interface
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add new visualization type"
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes

## 📝 Coding Standards

### Python Style Guide
- Follow [PEP 8](https://pep8.org/) guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Include type hints where appropriate

### Code Examples

**Function Documentation:**
```python
def analyze_lap_performance(telemetry_data: pd.DataFrame, 
                          driver: str, 
                          lap_type: str = 'fastest') -> dict:
    """
    Analyze driver lap performance from telemetry data.
    
    Args:
        telemetry_data: DataFrame containing F1 telemetry
        driver: Three-letter driver code (e.g., 'VER', 'HAM')
        lap_type: Type of lap to analyze ('fastest', 'first', 'last')
    
    Returns:
        Dictionary containing performance metrics
        
    Raises:
        ValueError: If driver not found in data
    """
    pass
```

**Variable Naming:**
```python
# Good
max_speed_kmh = telemetry['Speed'].max()
throttle_percentage = telemetry['Throttle']
lap_time_seconds = session.laps.pick_driver(driver)['LapTime']

# Avoid
ms = telemetry['Speed'].max()
tp = telemetry['Throttle']
lt = session.laps.pick_driver(driver)['LapTime']
```

### File Structure Guidelines

When adding new features:

**For new visualizations:**
- Add function to `visualization.py`
- Include example usage in docstring
- Add corresponding test in `tests/test_visualization.py`

**For new metrics:**
- Add function to `performance_metrics.py`
- Ensure it works with existing data structures
- Add test cases with sample data

**For web interface changes:**
- Update templates in `templates/`
- Add CSS to `static/css/style.css`
- Test responsiveness on different screen sizes

## 🧪 Testing Guidelines

### Writing Tests
- Use pytest framework
- Aim for >80% code coverage
- Include edge cases and error conditions
- Use sample data from `tests/` directory

### Test Categories

**Unit Tests** (`tests/test_*.py`):
```python
def test_calculate_speed_delta():
    """Test speed delta calculation between drivers."""
    # Use sample telemetry data
    driver1_data = load_sample_data('hamilton_monaco_q.csv')
    driver2_data = load_sample_data('verstappen_monaco_q.csv')
    
    delta = calculate_speed_delta(driver1_data, driver2_data)
    
    assert isinstance(delta, pd.DataFrame)
    assert 'SpeedDelta' in delta.columns
    assert len(delta) > 0
```

**Integration Tests** (`test_api.py`, `test_manual.py`):
- Test complete workflows
- Verify web interface functionality
- Check data pipeline end-to-end

## 📚 Documentation

### When to Update Documentation

- Adding new features or visualizations
- Changing CLI parameters or web interface
- Modifying installation or setup process
- Adding new dependencies

### Documentation Files to Update

- `README.md` - Main project documentation
- Docstrings in code - Function/class documentation
- `CONTRIBUTING.md` - This file
- Example files in `examples/` directory

## 🐛 Issue Guidelines

### Bug Report Template
```
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. Select driver '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Environment**
- OS: [e.g. Windows 10, macOS 12, Ubuntu 20.04]
- Python version: [e.g. 3.10.5]
- FastF1 version: [e.g. 3.0.1]

**Additional Context**
Error logs, screenshots, or other helpful information.
```

### Feature Request Template
```
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
How would this feature be used? What problem does it solve?

**Additional Context**
Mock-ups, examples from other tools, or implementation ideas.
```

## 🎉 Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- GitHub contributors list
- Release notes for significant contributions

## 📞 Questions?

- **General Questions**: [GitHub Discussions](https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-/issues)
- **Feature Requests**: [GitHub Issues](https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-/issues)

Thank you for contributing to the F1 data analysis community! 🏎️