import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.collections
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List

def plot_colored_track_map(
    session: Any,
    telemetry: pd.DataFrame,
    color_by: str = 'nGear',
    driver_label: str = 'Driver',
    save_path: Optional[str] = None
) -> None:
    """
    Plot the actual track map with telemetry colored by a chosen channel (e.g., gear, speed, throttle).
    Args:
        session: FastF1 session object (needed for track outline)
        telemetry: DataFrame with columns ['X', 'Y', ...]
        color_by: str, telemetry column to color by (e.g., 'nGear', 'Speed', 'Throttle')
        driver_label: str, label for the driver
        save_path: optional, if provided, save figure to this path
    """
    # Get track outline
    try:
        circuit_info = session.get_circuit_info()
        track_outline = circuit_info['Layout']
    except Exception:
        # fallback: just plot telemetry X/Y if outline not available
        track_outline = None

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    # Plot the track outline if available
    if track_outline is not None:
        ax.plot(track_outline[:, 0], track_outline[:, 1], color='black', linewidth=2, alpha=0.3, label='Track Outline')

    # Plot telemetry as a colored line
    points = np.array([telemetry['X'], telemetry['Y']]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = mpl.colors.Normalize(vmin=telemetry[color_by].min(), vmax=telemetry[color_by].max())
    lc = mpl.collections.LineCollection(segments, cmap='plasma', norm=norm)
    lc.set_array(telemetry[color_by])
    lc.set_linewidth(2)
    line = ax.add_collection(lc)
    cbar = plt.colorbar(line, ax=ax)
    cbar.set_label(color_by, fontsize=13)

    ax.set_xlabel('X (m)', fontsize=13)
    ax.set_ylabel('Y (m)', fontsize=13)
    ax.set_title(f'Track Map - {driver_label} ({color_by})', fontsize=15, fontweight='bold')
    ax.axis('equal')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()  # Close figure to free memory
    else:
        plt.show()
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

def plot_throttle_brake_trace(
    telemetry: pd.DataFrame,
    lap_info: Dict[str, Any],
    driver_code: str,
    save_path: Optional[str] = None
) -> None:
    """
    Plot speed, throttle, and brake traces with sector color coding.
    Args:
        telemetry: DataFrame with columns ['Distance', 'Speed', 'Throttle', 'Brake', 'Sector']
        lap_info: dict with keys 'lap_number', 'lap_time', 'sector1_end', 'sector2_end', 'sector3_end'
        driver_code: str, e.g. 'VER'
        save_path: optional, if provided, save figure to this path
    """
    # Sector color mapping
    sector_colors = {1: '#FF0000', 2: '#00FF00', 3: '#0000FF'}
    sector_bounds = [0, lap_info['sector1_end'], lap_info['sector2_end'], lap_info['sector3_end']]
    sector_labels = ['Sector 1', 'Sector 2', 'Sector 3']
    
    # Prepare figure
    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(12, 8), dpi=300)
    plt.subplots_adjust(hspace=0.1)
    font_kwargs = dict(fontsize=13)
    
    # Helper to plot colored line segments
    def plot_colored_line(ax, x, y, sectors, ylabel):
        for s in [1, 2, 3]:
            mask = (sectors == s)
            if np.any(mask):
                ax.plot(x[mask], y[mask], color=sector_colors[s], label=sector_labels[s] if ylabel=='Speed' else None, linewidth=2)
        ax.set_ylabel(ylabel, **font_kwargs)
        ax.grid(True, linestyle='--', alpha=0.5)
        if ylabel=='Speed':
            ax.legend(loc='upper right', fontsize=12)
        ax.tick_params(labelsize=12)

    # Plot each trace
    plot_colored_line(axes[0], telemetry['Distance'], telemetry['Speed'], telemetry['Sector'], 'Speed (km/h)')
    plot_colored_line(axes[1], telemetry['Distance'], telemetry['Throttle'], telemetry['Sector'], 'Throttle (%)')
    plot_colored_line(axes[2], telemetry['Distance'], telemetry['Brake'], telemetry['Sector'], 'Brake (%)')


    # Add sector boundaries
    for ax in axes:
        for bound in sector_bounds[1:-1]:
            ax.axvline(bound, color='k', linestyle='--', linewidth=1, label='Sector Boundary' if ax==axes[0] else None)

    # Annotate DRS activation if available
    if 'DRS_Active' in telemetry.columns:
        drs_on = telemetry[telemetry['DRS_Active'] > 0]
        for ax in axes:
            ax.scatter(drs_on['Distance'], [ax.get_ylim()[1]*0.98]*len(drs_on), color='magenta', marker='v', s=30, label='DRS Active' if ax==axes[0] else None, zorder=5)

    # Annotate pit stop if available
    if 'Pit' in telemetry.columns:
        pit_on = telemetry[telemetry['Pit'] > 0]
        for ax in axes:
            ax.scatter(pit_on['Distance'], [ax.get_ylim()[0]+2]*len(pit_on), color='black', marker='s', s=30, label='Pit Stop' if ax==axes[0] else None, zorder=5)

    axes[2].set_xlabel('Distance (m)', **font_kwargs)
    lap_time_str = str(lap_info['lap_time']) if 'lap_time' in lap_info else ''
    lap_num = lap_info.get('lap_number', '?')
    fig.suptitle(f"{driver_code} Lap {lap_num}  |  Lap Time: {lap_time_str}", fontsize=15, fontweight='bold')
    
    # Professional formatting
    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.margins(x=0)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_driver_comparison(
    driver1_telemetry: pd.DataFrame,
    driver2_telemetry: pd.DataFrame,
    driver1_label: str = 'Driver 1',
    driver2_label: str = 'Driver 2',
    save_path: Optional[str] = None
) -> None:
    """
    Plot side-by-side comparison of two drivers' speed, throttle, and brake traces.
    Args:
        driver1_telemetry: DataFrame with columns ['Distance', 'Speed', 'Throttle', 'Brake'] for driver 1
        driver2_telemetry: DataFrame with same columns for driver 2
        driver1_label: str, label for driver 1
        driver2_label: str, label for driver 2
        save_path: optional, if provided, save figure to this path
    """
    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(12, 8), dpi=300)
    plt.subplots_adjust(hspace=0.1)
    font_kwargs = dict(fontsize=13)

    # Speed
    axes[0].plot(driver1_telemetry['Distance'], driver1_telemetry['Speed'], label=driver1_label, color='red', linewidth=2)
    axes[0].plot(driver2_telemetry['Distance'], driver2_telemetry['Speed'], label=driver2_label, color='blue', linewidth=2, alpha=0.8)
    axes[0].set_ylabel('Speed (km/h)', **font_kwargs)
    axes[0].legend(loc='upper right', fontsize=12)
    axes[0].grid(True, linestyle='--', alpha=0.5)
    axes[0].tick_params(labelsize=12)

    # Throttle
    axes[1].plot(driver1_telemetry['Distance'], driver1_telemetry['Throttle'], label=driver1_label, color='red', linewidth=2)
    axes[1].plot(driver2_telemetry['Distance'], driver2_telemetry['Throttle'], label=driver2_label, color='blue', linewidth=2, alpha=0.8)
    axes[1].set_ylabel('Throttle (%)', **font_kwargs)
    axes[1].grid(True, linestyle='--', alpha=0.5)
    axes[1].tick_params(labelsize=12)

    # Brake
    axes[2].plot(driver1_telemetry['Distance'], driver1_telemetry['Brake'], label=driver1_label, color='red', linewidth=2)
    axes[2].plot(driver2_telemetry['Distance'], driver2_telemetry['Brake'], label=driver2_label, color='blue', linewidth=2, alpha=0.8)
    axes[2].set_ylabel('Brake (%)', **font_kwargs)
    axes[2].set_xlabel('Distance (m)', **font_kwargs)
    axes[2].grid(True, linestyle='--', alpha=0.5)
    axes[2].tick_params(labelsize=12)


    # Annotate DRS activation if available
    for idx, telemetry in enumerate([driver1_telemetry, driver2_telemetry]):
        color = 'magenta' if idx == 0 else 'cyan'
        if 'DRS_Active' in telemetry.columns:
            drs_on = telemetry[telemetry['DRS_Active'] > 0]
            for ax in axes:
                ax.scatter(drs_on['Distance'], [ax.get_ylim()[1]*0.98]*len(drs_on), color=color, marker='v', s=25, label=f'DRS {driver1_label if idx==0 else driver2_label}' if ax==axes[0] else None, zorder=5)
        if 'Pit' in telemetry.columns:
            pit_on = telemetry[telemetry['Pit'] > 0]
            for ax in axes:
                ax.scatter(pit_on['Distance'], [ax.get_ylim()[0]+2]*len(pit_on), color='black', marker='s', s=25, label=f'Pit {driver1_label if idx==0 else driver2_label}' if ax==axes[0] else None, zorder=5)

    # Professional formatting
    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.margins(x=0)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    fig.suptitle(f"{driver1_label} vs {driver2_label} - Telemetry Comparison", fontsize=15, fontweight='bold')
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_speed_delta(
    driver1_telemetry: pd.DataFrame,
    driver2_telemetry: pd.DataFrame,
    driver1_label: str = 'Driver 1',
    driver2_label: str = 'Driver 2',
    save_path: Optional[str] = None
) -> None:
    """
    Plot the speed delta and cumulative time delta between two drivers along the lap distance.
    Args:
        driver1_telemetry: DataFrame with columns ['Distance', 'Speed', 'Time'] for driver 1
        driver2_telemetry: DataFrame with same columns for driver 2
        driver1_label: str, label for driver 1
        driver2_label: str, label for driver 2
        save_path: optional, if provided, save figure to this path
    """
    # Interpolate both drivers to a common distance axis
    common_dist = np.linspace(
        max(driver1_telemetry['Distance'].min(), driver2_telemetry['Distance'].min()),
        min(driver1_telemetry['Distance'].max(), driver2_telemetry['Distance'].max()),
        1000
    )
    speed1 = np.interp(common_dist, driver1_telemetry['Distance'], driver1_telemetry['Speed'])
    speed2 = np.interp(common_dist, driver2_telemetry['Distance'], driver2_telemetry['Speed'])
    time1 = np.interp(common_dist, driver1_telemetry['Distance'], driver1_telemetry['Time'])
    time2 = np.interp(common_dist, driver2_telemetry['Distance'], driver2_telemetry['Time'])
    speed_delta = speed1 - speed2
    time_delta = (time1 - time2)
    time_delta -= time_delta[0]  # Normalize to zero at start

    fig, axes = plt.subplots(2, 1, sharex=True, figsize=(12, 6), dpi=300)
    plt.subplots_adjust(hspace=0.15)
    font_kwargs = dict(fontsize=13)

    # Speed delta
    axes[0].plot(common_dist, speed_delta, color='purple', linewidth=2)
    axes[0].axhline(0, color='k', linestyle='--', linewidth=1)
    axes[0].set_ylabel(f'Speed Δ ({driver1_label} - {driver2_label}) (km/h)', **font_kwargs)
    axes[0].grid(True, linestyle='--', alpha=0.5)
    axes[0].tick_params(labelsize=12)

    # Cumulative time delta
    axes[1].plot(common_dist, time_delta, color='orange', linewidth=2)
    axes[1].axhline(0, color='k', linestyle='--', linewidth=1)
    axes[1].set_ylabel(f'Time Δ ({driver1_label} - {driver2_label}) (s)', **font_kwargs)
    axes[1].set_xlabel('Distance (m)', **font_kwargs)
    axes[1].grid(True, linestyle='--', alpha=0.5)
    axes[1].tick_params(labelsize=12)


    # Annotate DRS activation if available (for both drivers)
    for idx, telemetry in enumerate([driver1_telemetry, driver2_telemetry]):
        color = 'magenta' if idx == 0 else 'cyan'
        if 'DRS_Active' in telemetry.columns:
            drs_on = telemetry[telemetry['DRS_Active'] > 0]
            for ax in axes:
                ax.scatter(drs_on['Distance'], [ax.get_ylim()[1]*0.98]*len(drs_on), color=color, marker='v', s=20, label=f'DRS {driver1_label if idx==0 else driver2_label}' if ax==axes[0] else None, zorder=5)
        if 'Pit' in telemetry.columns:
            pit_on = telemetry[telemetry['Pit'] > 0]
            for ax in axes:
                ax.scatter(pit_on['Distance'], [ax.get_ylim()[0]+0.02*(ax.get_ylim()[1]-ax.get_ylim()[0])]*len(pit_on), color='black', marker='s', s=20, label=f'Pit {driver1_label if idx==0 else driver2_label}' if ax==axes[0] else None, zorder=5)

    # Professional formatting
    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.margins(x=0)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.suptitle(f"{driver1_label} vs {driver2_label} - Speed & Time Delta", fontsize=15, fontweight='bold')
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_gg_diagram(
    telemetry: pd.DataFrame,
    driver_label: str = 'Driver',
    save_path: Optional[str] = None
) -> None:
    """
    Plot a GG diagram (lateral vs longitudinal g-forces) from telemetry data.
    Args:
        telemetry: DataFrame with columns ['GforceLat', 'GforceLong']
        driver_label: str, label for the driver
        save_path: optional, if provided, save figure to this path
    """
    if 'GforceLat' not in telemetry or 'GforceLong' not in telemetry:
        raise ValueError('Telemetry must contain GforceLat and GforceLong columns.')
    plt.figure(figsize=(7, 7), dpi=300)
    plt.scatter(telemetry['GforceLat'], telemetry['GforceLong'], s=8, c=telemetry.get('Speed', None), cmap='viridis', alpha=0.7)
    plt.axhline(0, color='k', linestyle='--', linewidth=1)
    plt.axvline(0, color='k', linestyle='--', linewidth=1)
    plt.xlabel('Lateral G (g)', fontsize=13)
    plt.ylabel('Longitudinal G (g)', fontsize=13)
    plt.title(f'GG Diagram - {driver_label}', fontsize=15, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.gca().set_aspect('equal', 'box')
    plt.tick_params(labelsize=12)
    if 'Speed' in telemetry:
        cbar = plt.colorbar(label='Speed (km/h)')
        cbar.ax.tick_params(labelsize=12)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_corner_analysis(
    telemetry: pd.DataFrame,
    corner_locations: List[float],
    driver_label: str = 'Driver',
    save_path: Optional[str] = None
) -> None:
    """
    Plot corner-by-corner performance: entry, apex, and exit speeds for each corner.
    Args:
        telemetry: DataFrame with columns ['Distance', 'Speed']
        corner_locations: list or array of apex distances (meters)
        driver_label: str, label for the driver
        save_path: optional, if provided, save figure to this path
    """
    entry_offset = 50  # meters before apex
    exit_offset = 50   # meters after apex
    entry_speeds = []
    apex_speeds = []
    exit_speeds = []
    for apex in corner_locations:
        # Entry speed
        entry_idx = (np.abs(telemetry['Distance'] - (apex - entry_offset))).argmin()
        entry_speeds.append(telemetry['Speed'].iloc[entry_idx])
        # Apex speed
        apex_idx = (np.abs(telemetry['Distance'] - apex)).argmin()
        apex_speeds.append(telemetry['Speed'].iloc[apex_idx])
        # Exit speed
        exit_idx = (np.abs(telemetry['Distance'] - (apex + exit_offset))).argmin()
        exit_speeds.append(telemetry['Speed'].iloc[exit_idx])
    corners = np.arange(1, len(corner_locations) + 1)
    plt.figure(figsize=(12, 5), dpi=300)
    plt.plot(corners, entry_speeds, marker='o', label='Entry Speed', color='#1f77b4')
    plt.plot(corners, apex_speeds, marker='s', label='Apex Speed', color='#ff7f0e')
    plt.plot(corners, exit_speeds, marker='^', label='Exit Speed', color='#2ca02c')
    plt.xlabel('Corner Number', fontsize=13)
    plt.ylabel('Speed (km/h)', fontsize=13)
    plt.title(f'Corner-by-Corner Analysis - {driver_label}', fontsize=15, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(fontsize=12)
    plt.xticks(corners)
    plt.tick_params(labelsize=12)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_gear_usage_map(
    telemetry: pd.DataFrame,
    driver_label: str = 'Driver',
    save_path: Optional[str] = None
) -> None:
    """
    Plot a map of the track colored by gear selection.
    Args:
        telemetry: DataFrame with columns ['X', 'Y', 'nGear']
        driver_label: str, label for the driver
        save_path: optional, if provided, save figure to this path
    """
    if not all(col in telemetry for col in ['X', 'Y', 'nGear']):
        raise ValueError('Telemetry must contain X, Y, and nGear columns.')
    x = telemetry['X'].values
    y = telemetry['Y'].values
    gears = telemetry['nGear'].astype(int).values
    cmap = plt.get_cmap('plasma', np.max(gears) - np.min(gears) + 1)
    plt.figure(figsize=(10, 7), dpi=300)
    sc = plt.scatter(x, y, c=gears, cmap=cmap, s=8, marker='o', alpha=0.85)
    cbar = plt.colorbar(sc, ticks=np.arange(np.min(gears), np.max(gears)+1))
    cbar.set_label('Gear', fontsize=13)
    cbar.ax.tick_params(labelsize=12)
    plt.xlabel('X (m)', fontsize=13)
    plt.ylabel('Y (m)', fontsize=13)
    plt.title(f'Gear Usage Map - {driver_label}', fontsize=15, fontweight='bold')
    plt.axis('equal')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_brake_usage_map(
    telemetry: pd.DataFrame,
    driver_label: str = 'Driver',
    save_path: Optional[str] = None
) -> None:
    """
    Plot a map of the track colored by brake intensity/pressure.
    Args:
        telemetry: DataFrame with columns ['X', 'Y', 'Brake']
        driver_label: str, label for the driver
        save_path: optional, if provided, save figure to this path
    """
    if not all(col in telemetry for col in ['X', 'Y', 'Brake']):
        raise ValueError('Telemetry must contain X, Y, and Brake columns.')
    
    x = telemetry['X'].values
    y = telemetry['Y'].values
    brake = telemetry['Brake'].values
    
    # Handle cases where brake data might be boolean or need conversion
    try:
        brake = pd.to_numeric(brake, errors='coerce').fillna(0).values
    except:
        brake = np.array([float(b) if pd.notna(b) else 0.0 for b in brake])
    
    plt.figure(figsize=(10, 7), dpi=300)
    sc = plt.scatter(x, y, c=brake, cmap='hot', s=8, marker='o', alpha=0.85, vmin=0, vmax=100)
    cbar = plt.colorbar(sc)
    cbar.set_label('Brake Pressure (%)', fontsize=13)
    cbar.ax.tick_params(labelsize=12)
    plt.xlabel('X (m)', fontsize=13)
    plt.ylabel('Y (m)', fontsize=13)
    plt.title(f'Brake Usage Map - {driver_label}', fontsize=15, fontweight='bold')
    plt.axis('equal')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
