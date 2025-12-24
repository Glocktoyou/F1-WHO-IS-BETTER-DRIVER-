import pytest
import pandas as pd
import numpy as np
from src.visualization import plot_throttle_brake_trace

def test_plot_throttle_brake_trace(tmp_path):
    telemetry = pd.DataFrame({
        'Distance': np.linspace(0, 100, 10),
        'Speed': np.random.uniform(100, 300, 10),
        'Throttle': np.random.uniform(0, 100, 10),
        'Brake': np.random.uniform(0, 100, 10),
        'Sector': [1]*3 + [2]*3 + [3]*4
    })
    lap_info = {'lap_number': 1, 'lap_time': '1:12.345', 'sector1_end': 30, 'sector2_end': 60, 'sector3_end': 100}
    driver_code = 'VER'
    out_path = tmp_path / 'trace.png'
    plot_throttle_brake_trace(telemetry, lap_info, driver_code, save_path=str(out_path))
    assert out_path.exists()
