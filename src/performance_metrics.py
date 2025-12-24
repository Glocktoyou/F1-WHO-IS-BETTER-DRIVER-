import numpy as np
import pandas as pd

class DriverPerformanceAnalyzer:
    """
    Analyze driver telemetry for advanced performance metrics.
    """
    def __init__(self, telemetry: pd.DataFrame, laps: pd.DataFrame = None):
        """
        Args:
            telemetry: DataFrame with columns ['Time', 'Distance', 'Speed', 'Throttle', 'Brake', 'RPM', 'nGear', 'DRS', 'X', 'Y', 'Z']
            laps: Optional DataFrame of lap data for multi-lap analysis
        """
        self.telemetry = telemetry
        self.laps = laps

    # --- Braking Metrics ---
    def braking_zones(self, threshold=10):
        """Return list of (start_idx, end_idx) for each braking zone (brake > threshold)."""
        brake = self.telemetry['Brake'] > threshold
        zones = []
        in_zone = False
        for i, b in enumerate(brake):
            if b and not in_zone:
                start = i
                in_zone = True
            elif not b and in_zone:
                end = i-1
                zones.append((start, end))
                in_zone = False
        if in_zone:
            zones.append((start, len(brake)-1))
        return zones

    def brake_application_points(self, apex_distances):
        """Return distance before apex where brake is first applied for each corner (requires apex_distances)."""
        points = []
        for apex in apex_distances:
            before_apex = self.telemetry[self.telemetry['Distance'] < apex]
            brake_on = before_apex[before_apex['Brake'] > 10]
            if not brake_on.empty:
                points.append(apex - brake_on['Distance'].iloc[-1])
            else:
                points.append(np.nan)
        return points

    def max_brake_pressure_per_zone(self):
        """Return max brake value for each braking zone."""
        zones = self.braking_zones()
        return [self.telemetry['Brake'].iloc[start:end+1].max() for start, end in zones]

    def brake_consistency(self):
        """Return std deviation of max brake per zone across laps (if laps provided)."""
        if self.laps is None:
            return np.nan
        max_pressures = [self.max_brake_pressure_per_zone() for _ in self.laps]
        return np.std([np.mean(m) for m in max_pressures])

    def trail_braking_profile(self):
        """Return correlation between brake and steering (if steering data present)."""
        if 'SteeringAngle' in self.telemetry:
            return self.telemetry['Brake'].corr(self.telemetry['SteeringAngle'])
        return np.nan

    # --- Throttle Metrics ---
    def throttle_pickup_after_apex(self, apex_distances):
        """Return distance after apex where throttle > 10% resumes for each corner."""
        points = []
        for apex in apex_distances:
            after_apex = self.telemetry[self.telemetry['Distance'] > apex]
            throttle_on = after_apex[after_apex['Throttle'] > 10]
            if not throttle_on.empty:
                points.append(throttle_on['Distance'].iloc[0] - apex)
            else:
                points.append(np.nan)
        return points

    def full_throttle_percentage(self):
        """Return percent of lap spent at >95% throttle."""
        return (self.telemetry['Throttle'] > 95).mean() * 100

    def throttle_smoothness(self):
        """Return mean rate of change of throttle (smooth = low value)."""
        return np.abs(np.diff(self.telemetry['Throttle'])).mean()

    def coasting_time_percentage(self):
        """Return percent of lap spent with throttle < 5% and brake < 5%."""
        coast = (self.telemetry['Throttle'] < 5) & (self.telemetry['Brake'] < 5)
        return coast.mean() * 100

    # --- Corner Performance ---
    def min_speed_per_corner(self, apex_distances, window=10):
        """Return minimum speed in a window around each apex."""
        min_speeds = []
        for apex in apex_distances:
            mask = (self.telemetry['Distance'] > apex - window) & (self.telemetry['Distance'] < apex + window)
            min_speeds.append(self.telemetry.loc[mask, 'Speed'].min())
        return min_speeds

    def corner_entry_speed(self, apex_distances, entry_offset=50):
        """Return speed 50m before each apex."""
        return [self.telemetry.iloc[(self.telemetry['Distance']-apex+entry_offset).abs().argsort()[:1]]['Speed'].values[0] for apex in apex_distances]

    def corner_exit_speed(self, apex_distances, exit_offset=50):
        """Return speed 50m after each apex."""
        return [self.telemetry.iloc[(self.telemetry['Distance']-apex-exit_offset).abs().argsort()[:1]]['Speed'].values[0] for apex in apex_distances]

    def time_lost_in_corners(self, straight_mask):
        """Return time spent in corners vs straights (requires boolean mask for straights)."""
        total_time = self.telemetry['Time'].iloc[-1] - self.telemetry['Time'].iloc[0]
        straight_time = self.telemetry.loc[straight_mask, 'Time'].diff().sum()
        return (total_time - straight_time, straight_time)

    # --- Driving Style ---
    def steering_smoothness_index(self):
        """Return mean rate of change of steering angle (if present)."""
        if 'SteeringAngle' in self.telemetry:
            return np.abs(np.diff(self.telemetry['SteeringAngle'])).mean()
        return np.nan

    def gforce_efficiency(self):
        """Return mean of sqrt(lateral^2 + longitudinal^2) if g-force columns present."""
        if 'GforceLat' in self.telemetry and 'GforceLong' in self.telemetry:
            return np.mean(np.sqrt(self.telemetry['GforceLat']**2 + self.telemetry['GforceLong']**2))
        return np.nan

    def gear_shift_timing(self):
        """Return list of (distance, rpm) at each upshift."""
        nGear = self.telemetry['nGear'].values
        rpm = self.telemetry['RPM'].values
        dist = self.telemetry['Distance'].values
        upshifts = np.where(np.diff(nGear) > 0)[0]
        return [(dist[i], rpm[i]) for i in upshifts]

    def drs_usage_timing(self):
        """Return list of (distance, time) where DRS is activated (DRS > 0)."""
        drs_on = self.telemetry[self.telemetry['DRS'] > 0]
        return list(zip(drs_on['Distance'], drs_on['Time']))
