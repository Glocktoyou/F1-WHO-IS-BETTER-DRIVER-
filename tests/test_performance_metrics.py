import pytest
import pandas as pd
from src.performance_metrics import DriverPerformanceAnalyzer

def test_braking_zones():
    df = pd.DataFrame({'Brake': [0, 20, 50, 0, 0, 30, 0], 'Distance': [0, 10, 20, 30, 40, 50, 60]})
    analyzer = DriverPerformanceAnalyzer(df)
    zones = analyzer.braking_zones()
    assert isinstance(zones, list)

def test_full_throttle_percentage():
    df = pd.DataFrame({'Throttle': [0, 100, 100, 0, 100]})
    analyzer = DriverPerformanceAnalyzer(df)
    pct = analyzer.full_throttle_percentage()
    assert 0 <= pct <= 100
