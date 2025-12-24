
# --- F1 Driver Performance Analysis Tool ---
import pandas as pd
from performance_metrics import DriverPerformanceAnalyzer
from data_acquisition import F1DataLoader
from visualization import (
    plot_throttle_brake_trace,
    plot_driver_comparison,
    plot_speed_delta,
    plot_gg_diagram,
    plot_corner_analysis,
    plot_gear_usage_map,
    plot_brake_usage_map
)
import sys
import argparse

def main():
	parser = argparse.ArgumentParser(
		description="F1 Telemetry Data Analysis CLI"
	)
	parser.add_argument('--year', type=int, required=True, help='Season year (e.g., 2024)')
	parser.add_argument('--track', type=str, required=True, help='Track/circuit name or round number (e.g., Monaco or 7)')
	parser.add_argument('--session', type=str, required=True, choices=['FP1', 'FP2', 'FP3', 'Q', 'S', 'R'], help='Session type (FP1, FP2, FP3, Q, S, R)')
	parser.add_argument('--driver', type=str, required=True, help='Three-letter driver code (e.g., VER, HAM)')
	parser.add_argument('--lap', type=str, default='fastest', choices=['fastest', 'first', 'last'], help='Lap type to analyze')
	parser.add_argument('--compare', type=str, help='Compare with another driver (three-letter code)')
	parser.add_argument('--plot', type=str, default='trace', choices=['trace', 'compare', 'delta', 'gg', 'corners', 'gearmap', 'brakemap', 'trackmap'], help='Type of plot to generate')
	parser.add_argument('--color-by', type=str, default='nGear', help='Telemetry column to color track map by (e.g., nGear, Speed, Throttle)')
	parser.add_argument('--export', action='store_true', help='Export telemetry to CSV')
	parser.add_argument('--output', type=str, help='Output file name for CSV or plot')
	parser.add_argument('--list-tracks', action='store_true', help='List available tracks for the given year and exit')
	parser.add_argument('--all-laps', action='store_true', help='Analyze all laps for the driver (multi-lap/stint analysis)')

	args = parser.parse_args()

	if args.list_tracks:
		import fastf1
		if not args.year:
			print('Please provide --year to list tracks.')
			sys.exit(1)
		schedule = fastf1.get_event_schedule(args.year)
		print(f"Tracks for {args.year}:")
		for rnd, row in schedule.iterrows():
			print(f"  Round {row['RoundNumber']}: {row['EventName']} ({row['Location']})")
		sys.exit(0)

	loader = F1DataLoader(cache_dir='cache')
	try:
		session = loader.load_session(args.year, args.track, args.session)
	except Exception as e:
		print(f"Error loading session: {e}")
		sys.exit(1)

	if not loader.validate_driver_code(args.driver):
		print(f"Driver {args.driver} not found in session.")
		sys.exit(1)

	try:
		if args.all_laps:
			# Multi-lap/stint analysis
			laps = loader.session.laps.pick_drivers([args.driver])
			if laps.empty:
				print(f"No laps found for driver {args.driver}.")
				sys.exit(1)
			lap_times = laps['LapTime'].dt.total_seconds()
			avg_lap_time = lap_times.mean()
			std_lap_time = lap_times.std()
			print(f"Analyzing all laps for {args.driver}:")
			print(f"  Number of laps: {len(laps)}")
			print(f"  Average lap time: {avg_lap_time:.3f} s")
			print(f"  Lap time std dev: {std_lap_time:.3f} s")
			# Optionally, export all lap times
			if args.export:
				laps[['LapNumber', 'LapTime']].to_csv(args.output or f"{args.driver.lower()}_{args.track.lower()}_{args.session.lower()}_all_laps.csv", index=False)
				print(f"Exported all lap times to CSV.")
			# Optionally, analyze stints (by compound)
			if 'Compound' in laps.columns:
				print("Stint summary by compound:")
				for compound, stint_laps in laps.groupby('Compound'):
					stint_times = stint_laps['LapTime'].dt.total_seconds()
					print(f"  {compound}: {len(stint_laps)} laps, avg {stint_times.mean():.3f} s, std {stint_times.std():.3f} s")
			# Optionally, plot lap times
			import matplotlib.pyplot as plt
			plt.figure(figsize=(10,5))
			plt.plot(laps['LapNumber'], lap_times, marker='o')
			plt.xlabel('Lap Number')
			plt.ylabel('Lap Time (s)')
			plt.title(f"Lap Times for {args.driver} ({args.track} {args.session})")
			plt.grid(True, linestyle='--', alpha=0.5)
			plt.tight_layout()
			plt.show()
			# End of all-laps analysis
		else:
			lap = loader.get_driver_lap(args.driver, lap_type=args.lap)
			telemetry = loader.get_telemetry(lap)
	except Exception as e:
		print(f"Error getting telemetry: {e}")
		sys.exit(1)

	if not args.all_laps:
		if args.export:
			out_name = args.output or f"{args.driver.lower()}_{args.track.lower()}_{args.session.lower()}.csv"
			out_path = loader.export_to_csv(telemetry, out_name)
			print(f"Exported telemetry to {out_path}")

		# Plotting options
		if args.plot == 'trace':
			# Use official sector boundaries from lap data
			sector_cols = [col for col in telemetry.columns if col.lower().startswith('sector')]
			# Get sector end distances from lap data if available
			try:
				s1_end = float(lap['Sector1SessionTime'].total_seconds()) if 'Sector1SessionTime' in lap else telemetry['Distance'].max() / 3
				s2_end = float(lap['Sector2SessionTime'].total_seconds()) if 'Sector2SessionTime' in lap else 2 * telemetry['Distance'].max() / 3
				# Map session times to distances
				s1_dist = telemetry.iloc[(telemetry['Time']-telemetry['Time'].iloc[0]).abs().argsort()[:1]]['Distance'].values[0]
				s2_dist = telemetry.iloc[(telemetry['Time']-telemetry['Time'].iloc[0]-s2_end+s1_end).abs().argsort()[:1]]['Distance'].values[0]
			except Exception:
				s1_dist = telemetry['Distance'].max() / 3
				s2_dist = 2 * telemetry['Distance'].max() / 3
			lap_info = {
				'lap_number': lap.get('LapNumber', '?'),
				'lap_time': lap.get('LapTime', '?'),
				'sector1_end': s1_dist,
				'sector2_end': s2_dist,
				'sector3_end': telemetry['Distance'].max()
			}
			# Assign sector numbers based on official boundaries
			if 'Sector' not in telemetry:
				telemetry = telemetry.copy()
				telemetry['Sector'] = 1
				telemetry.loc[telemetry['Distance'] > lap_info['sector1_end'], 'Sector'] = 2
				telemetry.loc[telemetry['Distance'] > lap_info['sector2_end'], 'Sector'] = 3
			plot_throttle_brake_trace(telemetry, lap_info, args.driver, save_path=args.output)
		elif args.plot == 'compare':
			if not args.compare:
				print("Please provide --compare DRIVER for comparison plot.")
				sys.exit(1)
			if not loader.validate_driver_code(args.compare):
				print(f"Driver {args.compare} not found in session.")
				sys.exit(1)
			lap2 = loader.get_driver_lap(args.compare, lap_type=args.lap)
			telemetry2 = loader.get_telemetry(lap2)
			plot_driver_comparison(telemetry, telemetry2, args.driver, args.compare, save_path=args.output)
		elif args.plot == 'delta':
			if not args.compare:
				print("Please provide --compare DRIVER for delta plot.")
				sys.exit(1)
			if not loader.validate_driver_code(args.compare):
				print(f"Driver {args.compare} not found in session.")
				sys.exit(1)
			lap2 = loader.get_driver_lap(args.compare, lap_type=args.lap)
			telemetry2 = loader.get_telemetry(lap2)
			plot_speed_delta(telemetry, telemetry2, args.driver, args.compare, save_path=args.output)
		elif args.plot == 'gg':
			if 'GforceLat' not in telemetry or 'GforceLong' not in telemetry:
				print("Telemetry does not contain GforceLat and GforceLong columns.")
				sys.exit(1)
			plot_gg_diagram(telemetry, args.driver, save_path=args.output)
		elif args.plot == 'corners':
			# Use official corner apex distances if available
			try:
				circuit_info = session.get_circuit_info()
				if 'Corners' in circuit_info:
					corner_locations = [corner['Apex'][0] for corner in circuit_info['Corners'] if 'Apex' in corner]
				else:
					raise Exception('No official corners')
			except Exception:
				# fallback: evenly spaced corners
				n_corners = 10
				dists = telemetry['Distance']
				corner_locations = [dists.min() + i * (dists.max() - dists.min()) / n_corners for i in range(1, n_corners+1)]
			plot_corner_analysis(telemetry, corner_locations, args.driver, save_path=args.output)
		elif args.plot == 'gearmap':
			plot_gear_usage_map(telemetry, args.driver, save_path=args.output)
		elif args.plot == 'brakemap':
			plot_brake_usage_map(telemetry, args.driver, save_path=args.output)
		elif args.plot == 'trackmap':
			from visualization import plot_colored_track_map
			plot_colored_track_map(session, telemetry, color_by=args.color_by, driver_label=args.driver, save_path=args.output)


if __name__ == "__main__":
	main()
