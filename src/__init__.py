"""
F1 WHO IS BETTER DRIVER? - Source Package

This package contains the core modules for F1 driver performance analysis:
- data_acquisition: F1 data loading and session management
- performance_metrics: Driver analytics and comparison tools  
- visualization: Plotting and visualization engine
- app: Flask web application
- main: Command-line interface

Author: F1 Analysis Team
Version: 1.0.1
License: MIT
Repository: https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-
"""

__version__ = "1.0.1"
__author__ = "F1 Analysis Team"
__license__ = "MIT"
__repository__ = "https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-"

# Import main classes for easier access
from .data_acquisition import F1DataLoader
from .performance_metrics import DriverPerformanceAnalyzer

__all__ = [
    'F1DataLoader',
    'DriverPerformanceAnalyzer'
]