"""
F1 Data Acquisition Module

This module provides the F1DataLoader class for fetching and processing 
Formula 1 telemetry data using the FastF1 API.

Requirements:
- fastf1 library for accessing official F1 timing data
- pandas for data manipulation
- Enable caching to minimize API calls and improve performance
- Handle missing data and API errors gracefully
- Support exporting telemetry data to CSV for MATLAB integration

Dependencies:
    pip install fastf1 pandas numpy
"""

import fastf1
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Union, Literal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a class F1DataLoader that handles all F1 data acquisition
class F1DataLoader:
    """
    A class to load and process Formula 1 session data and telemetry.
    
    This class provides methods to:
    - Load F1 sessions (practice, qualifying, race, sprint)
    - Retrieve driver lap data (fastest lap, specific lap number)
    - Extract telemetry channels (speed, throttle, brake, etc.)
    - Export data to CSV format for MATLAB analysis
    - Implement caching to avoid repeated API calls
    
    Attributes:
        cache_dir (Path): Directory path for FastF1 cache storage
        session: Currently loaded FastF1 session object
        
    Example Usage:
        loader = F1DataLoader(cache_dir='cache')
        session = loader.load_session(2024, 'Monaco', 'Q')
        lap = loader.get_driver_lap('VER', lap_type='fastest')
        telemetry = loader.get_telemetry(lap)
        loader.export_to_csv(telemetry, 'verstappen_monaco_q.csv')
    """
    
    def __init__(self, cache_dir: str = 'cache'):
        """
        Initialize F1DataLoader with caching enabled.
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        fastf1.Cache.enable_cache(str(self.cache_dir))
        self.session = None
    
    def load_session(self, 
                     year: int, 
                     race: Union[int, str], 
                     session_type: Literal['FP1', 'FP2', 'FP3', 'Q', 'S', 'R']) -> fastf1.core.Session:
        """
        Load a specific F1 session using FastF1 API.
        
        Args:
            year: Season year (e.g., 2024, 2023)
            race: Race name (e.g., 'Monaco', 'Silverstone') or round number (1-24)
            session_type: Session identifier:
                'FP1' - Free Practice 1
                'FP2' - Free Practice 2  
                'FP3' - Free Practice 3
                'Q'   - Qualifying
                'S'   - Sprint
                'R'   - Race
        
        Returns:
            fastf1.core.Session: Loaded session object with all data
        
        Raises:
            ValueError: If session cannot be loaded or doesn't exist
            
        Implementation:
            - Use fastf1.get_session() to fetch session
            - Call session.load() to load all session data
            - Store session in self.session for later use
            - Add logging for successful load
            - Implement error handling for invalid sessions
            - Return the loaded session object
        """
        try:
            session = fastf1.get_session(year, race, session_type)
            session.load()
            self.session = session
            logger.info(f"Loaded session: {year} {race} {session_type}")
            return session
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            raise ValueError(f"Could not load session: {year} {race} {session_type}") from e
    
    def get_driver_lap(self, 
                       driver_code: str, 
                       lap_type: Literal['fastest', 'first', 'last'] = 'fastest',
                       lap_number: Optional[int] = None) -> fastf1.core.Lap:
        """
        Retrieve a specific lap for a driver from the loaded session.
        
        Args:
            driver_code: Three-letter driver code (e.g., 'VER', 'HAM', 'LEC')
            lap_type: Type of lap to retrieve:
                'fastest' - Fastest lap of the session (default)
                'first'   - First completed lap
                'last'    - Last completed lap
            lap_number: Specific lap number to retrieve (overrides lap_type)
        
        Returns:
            fastf1.core.Lap: Lap object containing lap data and telemetry
        
        Raises:
            ValueError: If session not loaded or driver not found
            
        Implementation:
            - Check if session is loaded, raise error if not
            - Use session.laps.pick_driver() to filter driver laps
            - If lap_number specified, use .pick_lap(lap_number)
            - If lap_type is 'fastest', use .pick_fastest()
            - If lap_type is 'first' or 'last', use appropriate indexing
            - Verify lap is valid (not null, has telemetry)
            - Add logging with driver code and lap info
            - Return the lap object
        """
        if self.session is None:
            raise ValueError("No session loaded. Call load_session() first.")
        driver_code = driver_code.upper()
        # Use pick_drivers (returns DataFrame) instead of deprecated pick_driver
        laps = self.session.laps.pick_drivers([driver_code])
        if laps.empty:
            logger.error(f"No laps found for driver {driver_code}")
            raise ValueError(f"Driver {driver_code} not found in session.")
        lap = None
        if lap_number is not None:
            lap = laps.pick_lap(lap_number)
        elif lap_type == 'fastest':
            lap = laps.pick_fastest()
        elif lap_type == 'first':
            lap = laps.iloc[0] if len(laps) > 0 else None
        elif lap_type == 'last':
            lap = laps.iloc[-1] if len(laps) > 0 else None
        if lap is None or (hasattr(lap, 'empty') and lap.empty):
            logger.error(f"Lap not found for driver {driver_code} (lap_type={lap_type}, lap_number={lap_number})")
            raise ValueError(f"Lap not found for driver {driver_code}.")
        logger.info(f"Selected lap for {driver_code}: LapTime={lap['LapTime'] if 'LapTime' in lap else 'N/A'}")
        return lap
    
    def get_telemetry(self, lap: fastf1.core.Lap) -> pd.DataFrame:
        """
        Extract telemetry data from a lap object.
        
        Args:
            lap: FastF1 Lap object from get_driver_lap()
        
        Returns:
            pd.DataFrame: Telemetry dataframe with columns:
                - Time: Elapsed time (datetime)
                - Distance: Distance along track (meters)
                - Speed: Vehicle speed (km/h)
                - Throttle: Throttle position (0-100%)
                - Brake: Brake pressure (0-100%)
                - RPM: Engine RPM
                - nGear: Current gear (1-8)
                - DRS: DRS status (0-14)
                - X, Y, Z: Position coordinates (meters)
                - Status: Session status
                
        Implementation:
            - Call lap.get_telemetry() to retrieve telemetry
            - Verify telemetry data exists and is not empty
            - Convert telemetry to pandas DataFrame if needed
            - Ensure all expected channels are present
            - Handle missing channels gracefully (fill with NaN or 0)
            - Add logging with telemetry shape and available channels
            - Return clean DataFrame
        """
        telemetry = lap.get_telemetry()
        if telemetry is None or len(telemetry) == 0:
            logger.error("No telemetry data found for lap.")
            raise ValueError("No telemetry data found for lap.")
        df = pd.DataFrame(telemetry)
        
        # Ensure all expected columns are present
        expected_cols = ['Time', 'Distance', 'Speed', 'Throttle', 'Brake', 'RPM', 'nGear', 'DRS', 'X', 'Y', 'Z']
        for col in expected_cols:
            if col not in df.columns:
                df[col] = np.nan if col != 'nGear' else 0
        
        # Ensure proper data types for numeric columns
        numeric_cols = ['Distance', 'Speed', 'Throttle', 'Brake', 'RPM', 'nGear', 'DRS', 'X', 'Y', 'Z']
        for col in numeric_cols:
            if col in df.columns:
                # Convert boolean and other types to numeric, handle errors gracefully
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        logger.info(f"Telemetry shape: {df.shape}, columns: {df.columns.tolist()}")
        return df[expected_cols]
    
    def export_to_csv(self, 
                      telemetry: pd.DataFrame, 
                      filename: str,
                      output_dir: str = 'outputs/data') -> Path:
        """
        Export telemetry data to CSV format for MATLAB integration.
        
        Args:
            telemetry: Telemetry DataFrame from get_telemetry()
            filename: Output filename (e.g., 'verstappen_monaco.csv')
            output_dir: Directory for output files (default: 'outputs/data')
        
        Returns:
            Path: Full path to the exported CSV file
            
        Implementation:
            - Create output directory if it doesn't exist
            - Construct full output path using Path
            - Convert Time column to seconds if it's datetime
            - Select relevant columns for MATLAB:
              Time, Distance, Speed, Throttle, Brake, RPM, nGear, X, Y, Z
            - Export to CSV with headers, no index
            - Add logging with file path and size
            - Return Path object of exported file
            
        CSV Format Requirements:
            - Headers in first row
            - Numeric data only (no datetime objects)
            - No index column
            - Comma-separated values
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        full_path = output_path / filename
        df = telemetry.copy()
        # Convert Time to seconds if it's a datetime or timedelta
        if pd.api.types.is_timedelta64_dtype(df['Time']):
            df['Time'] = df['Time'].dt.total_seconds()
        elif pd.api.types.is_datetime64_any_dtype(df['Time']):
            df['Time'] = (df['Time'] - df['Time'].iloc[0]).dt.total_seconds()
        # Select only relevant columns
        cols = ['Time', 'Distance', 'Speed', 'Throttle', 'Brake', 'RPM', 'nGear', 'X', 'Y', 'Z']
        df = df[cols]
        df.to_csv(full_path, index=False)
        logger.info(f"Exported telemetry to {full_path} ({full_path.stat().st_size} bytes)")
        return full_path
    
    def get_session_info(self) -> dict:
        """
        Get metadata about the currently loaded session.
        
        Returns:
            dict: Session information including:
                - year: Season year
                - race: Race name
                - session_type: Session type (Q, R, etc.)
                - date: Session date
                - weather: Weather conditions
                - track_length: Track length in meters
                - drivers: List of driver codes in session
                
        Implementation:
            - Check if session is loaded
            - Extract session metadata from self.session
            - Get list of drivers using session.laps['Driver'].unique()
            - Compile information into dictionary
            - Return session info dict
        """
        if self.session is None:
            return None
        info = {
            'year': self.session.event['Year'] if 'Year' in self.session.event else None,
            'race': self.session.event['EventName'] if 'EventName' in self.session.event else None,
            'session_type': self.session.name if hasattr(self.session, 'name') else None,
            'date': self.session.date if hasattr(self.session, 'date') else None,
            'weather': getattr(self.session, 'weather', None),
            'track_length': getattr(self.session, 'trackLength', None),
            'drivers': sorted(self.session.laps['Driver'].unique()) if hasattr(self.session, 'laps') and not self.session.laps.empty else [],
        }
        return info
    
    def get_all_drivers(self) -> list:
        """
        Get list of all driver codes in the current session.
        
        Returns:
            list: List of three-letter driver codes
            
        Implementation:
            - Extract unique driver codes from session.laps
            - Sort alphabetically
            - Return as list
        """
        if self.session is None or not hasattr(self.session, 'laps') or self.session.laps.empty:
            return None
        drivers = sorted(self.session.laps['Driver'].unique())
        return drivers
    
    def validate_driver_code(self, driver_code: str) -> bool:
        """
        Validate if a driver code exists in the current session.
        
        Args:
            driver_code: Three-letter driver code to validate
            
        Returns:
            bool: True if driver exists, False otherwise
            
        Implementation:
            - Get list of drivers in session
            - Check if driver_code exists in list (case-insensitive)
            - Return boolean result
        """
        drivers = self.get_all_drivers()
        if not drivers:
            return False
        return driver_code.upper() in [d.upper() for d in drivers]


# Example usage demonstrating the complete workflow
if __name__ == "__main__":
    # Initialize data loader with cache
    loader = F1DataLoader(cache_dir='cache')
    
    # Load 2024 Monaco Grand Prix Qualifying session
    print("Loading session...")
    session = loader.load_session(2024, 'Monaco', 'Q')
    
    # Get session information
    session_info = loader.get_session_info()
    print(f"Loaded: {session_info}")
    
    # Get available drivers
    drivers = loader.get_all_drivers()
    print(f"Drivers in session: {drivers}")
    
    # Get Verstappen's fastest lap
    print("\nGetting Verstappen's fastest lap...")
    verstappen_lap = loader.get_driver_lap('VER', lap_type='fastest')
    print(f"Lap time: {verstappen_lap['LapTime']}")
    
    # Extract telemetry
    print("\nExtracting telemetry...")
    telemetry = loader.get_telemetry(verstappen_lap)
    print(f"Telemetry shape: {telemetry.shape}")
    print(f"Channels: {telemetry.columns.tolist()}")
    
    # Export to CSV for MATLAB
    print("\nExporting to CSV...")
    output_path = loader.export_to_csv(telemetry, 'verstappen_monaco_q.csv')
    print(f"Exported to: {output_path}")
    
    # Compare two drivers
    print("\nComparing Hamilton's lap...")
    hamilton_lap = loader.get_driver_lap('HAM', lap_type='fastest')
    hamilton_telemetry = loader.get_telemetry(hamilton_lap)
    loader.export_to_csv(hamilton_telemetry, 'hamilton_monaco_q.csv')
    
    print("\nData acquisition complete!")