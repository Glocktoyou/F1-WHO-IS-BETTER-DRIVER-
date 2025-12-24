#!/usr/bin/env python3
"""
F1 Driver Analysis - Basic Usage Examples

This script demonstrates how to use the F1 WHO IS BETTER DRIVER? analysis tool
with various examples ranging from basic to advanced usage.

Run with: python examples/basic_usage.py
"""

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_acquisition import F1DataManager
from performance_metrics import PerformanceAnalyzer
from visualization import F1Visualizer

def example_1_basic_driver_analysis():
    """
    Example 1: Basic driver telemetry analysis
    Load a session and analyze a single driver's fastest lap
    """
    print("🏎️  Example 1: Basic Driver Analysis")
    print("="*50)
    
    # Initialize the data manager
    data_manager = F1DataManager()
    
    # Load 2024 Monaco GP Qualifying session
    try:
        session = data_manager.load_session(2024, "Monaco", "Q")
        print(f"✅ Loaded: {session['name']}")
        
        # Get Max Verstappen's fastest lap
        driver_data = data_manager.get_driver_data(session['session'], "VER", "fastest")
        print(f"🏁 VER fastest lap: {driver_data['lap_time']}")
        
        # Analyze performance
        analyzer = PerformanceAnalyzer()
        metrics = analyzer.calculate_basic_metrics(driver_data['telemetry'])
        
        print("📊 Performance Metrics:")
        print(f"   Max Speed: {metrics['max_speed']:.1f} km/h")
        print(f"   Average Speed: {metrics['avg_speed']:.1f} km/h")
        print(f"   Throttle Usage: {metrics['throttle_usage']:.1f}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Tip: Make sure you have internet connection for FastF1 data")

def example_2_driver_comparison():
    """
    Example 2: Compare two drivers on the same track
    Compare Max Verstappen vs Lewis Hamilton in Monaco Qualifying
    """
    print("\n🆚 Example 2: Driver Comparison")
    print("="*50)
    
    data_manager = F1DataManager()
    analyzer = PerformanceAnalyzer()
    
    try:
        session = data_manager.load_session(2024, "Monaco", "Q")
        
        # Get data for both drivers
        ver_data = data_manager.get_driver_data(session['session'], "VER", "fastest")
        ham_data = data_manager.get_driver_data(session['session'], "HAM", "fastest")
        
        print(f"🏁 VER: {ver_data['lap_time']} | HAM: {ham_data['lap_time']}")
        
        # Compare performance
        comparison = analyzer.compare_drivers(
            ver_data['telemetry'], ham_data['telemetry'], 
            "VER", "HAM"
        )
        
        print("📈 Comparison Results:")
        print(f"   Faster driver: {comparison['faster_driver']}")
        print(f"   Time difference: {comparison['time_delta']:.3f}s")
        print(f"   Speed advantage: {comparison['speed_advantage']:.1f} km/h")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_3_multiple_visualizations():
    """
    Example 3: Generate multiple plot types for analysis
    Create different visualizations for the same driver
    """
    print("\n📊 Example 3: Multiple Visualizations")
    print("="*50)
    
    data_manager = F1DataManager()
    visualizer = F1Visualizer()
    
    try:
        session = data_manager.load_session(2024, "Monaco", "Q")
        driver_data = data_manager.get_driver_data(session['session'], "VER", "fastest")
        
        plot_types = ["trace", "gg", "gearmap"]
        
        for plot_type in plot_types:
            try:
                output_file = f"examples/output_ver_{plot_type}.png"
                
                if plot_type == "trace":
                    visualizer.plot_telemetry_trace(
                        driver_data['telemetry'], "VER", 
                        save_path=output_file
                    )
                elif plot_type == "gg":
                    visualizer.plot_gg_diagram(
                        driver_data['telemetry'], "VER",
                        save_path=output_file
                    )
                elif plot_type == "gearmap":
                    visualizer.plot_gear_usage_map(
                        driver_data['telemetry'], session['session'],
                        save_path=output_file
                    )
                
                print(f"✅ Generated {plot_type} plot: {output_file}")
                
            except Exception as e:
                print(f"❌ Failed to generate {plot_type}: {e}")
                
    except Exception as e:
        print(f"❌ Error loading session: {e}")

def example_4_data_export():
    """
    Example 4: Export telemetry data to CSV
    Save driver data for external analysis
    """
    print("\n💾 Example 4: Data Export")
    print("="*50)
    
    data_manager = F1DataManager()
    
    try:
        session = data_manager.load_session(2024, "Monaco", "Q")
        driver_data = data_manager.get_driver_data(session['session'], "VER", "fastest")
        
        # Export to CSV
        output_file = "examples/verstappen_monaco_q_telemetry.csv"
        
        # Save telemetry data
        telemetry_df = driver_data['telemetry']
        telemetry_df.to_csv(output_file, index=False)
        
        print(f"✅ Telemetry exported to: {output_file}")
        print(f"📊 Data shape: {telemetry_df.shape[0]} rows, {telemetry_df.shape[1]} columns")
        print(f"📋 Columns: {', '.join(telemetry_df.columns[:5])}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_5_advanced_analysis():
    """
    Example 5: Advanced performance analysis
    Calculate complex metrics and driver insights
    """
    print("\n🧠 Example 5: Advanced Analysis")
    print("="*50)
    
    data_manager = F1DataManager()
    analyzer = PerformanceAnalyzer()
    
    try:
        session = data_manager.load_session(2024, "Monaco", "Q")
        driver_data = data_manager.get_driver_data(session['session'], "VER", "fastest")
        
        # Advanced metrics
        advanced_metrics = analyzer.calculate_advanced_metrics(driver_data['telemetry'])
        
        print("🔬 Advanced Performance Analysis:")
        print(f"   Smoothness Index: {advanced_metrics['smoothness_index']:.3f}")
        print(f"   Braking Efficiency: {advanced_metrics['braking_efficiency']:.2f}%")
        print(f"   Cornering Speed Index: {advanced_metrics['cornering_speed_index']:.3f}")
        print(f"   Throttle Application Rate: {advanced_metrics['throttle_application_rate']:.2f}%/s")
        
        # Sector analysis
        sector_analysis = analyzer.analyze_sectors(driver_data['telemetry'])
        
        print("\n🏁 Sector Analysis:")
        for sector, data in sector_analysis.items():
            print(f"   {sector}: {data['time']:.3f}s (avg speed: {data['avg_speed']:.1f} km/h)")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """
    Run all examples
    """
    print("🏎️  F1 WHO IS BETTER DRIVER? - Usage Examples")
    print("=" * 60)
    print("This script demonstrates various ways to use the F1 analysis tool.")
    print("Note: Examples require internet connection for FastF1 data.\n")
    
    # Create output directory if it doesn't exist
    os.makedirs("examples", exist_ok=True)
    
    # Run examples
    examples = [
        example_1_basic_driver_analysis,
        example_2_driver_comparison,
        example_3_multiple_visualizations,
        example_4_data_export,
        example_5_advanced_analysis
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
            if i < len(examples):
                input("\nPress Enter to continue to next example...")
        except KeyboardInterrupt:
            print("\n\n👋 Examples interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Example {i} failed with error: {e}")
            continue
    
    print("\n✨ Examples completed!")
    print("💡 Try running the CLI tool: python main.py --help")
    print("🌐 Or start the web interface: python app.py")

if __name__ == "__main__":
    main()