#!/bin/bash
# F1 WHO IS BETTER DRIVER? - CLI Usage Examples
# This script demonstrates various CLI commands for F1 analysis

echo "🏎️  F1 WHO IS BETTER DRIVER? - CLI Examples"
echo "==========================================="
echo ""

# Example 1: Basic driver analysis
echo "📊 Example 1: Basic Driver Telemetry Analysis"
echo "----------------------------------------------"
echo "Command: python main.py --year 2024 --track Monaco --session Q --driver VER --lap fastest --plot trace"
echo ""
python main.py --year 2024 --track Monaco --session Q --driver VER --lap fastest --plot trace
echo ""

read -p "Press Enter to continue to next example..."

# Example 2: Driver comparison
echo "🆚 Example 2: Driver Comparison"
echo "--------------------------------"
echo "Command: python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot compare"
echo ""
python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot compare
echo ""

read -p "Press Enter to continue to next example..."

# Example 3: Speed delta analysis
echo "📈 Example 3: Speed Delta Analysis"
echo "----------------------------------"
echo "Command: python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot delta"
echo ""
python main.py --year 2024 --track Monaco --session Q --driver VER --compare HAM --plot delta
echo ""

read -p "Press Enter to continue to next example..."

# Example 4: G-G Diagram
echo "🎯 Example 4: G-G Diagram Analysis"
echo "----------------------------------"
echo "Command: python main.py --year 2024 --track Monaco --session Q --driver HAM --plot gg"
echo ""
python main.py --year 2024 --track Monaco --session Q --driver HAM --plot gg
echo ""

read -p "Press Enter to continue to next example..."

# Example 5: Track visualization
echo "🗺️  Example 5: Track Map Visualization"
echo "--------------------------------------"
echo "Command: python main.py --year 2024 --track Monaco --session Q --driver VER --plot trackmap"
echo ""
python main.py --year 2024 --track Monaco --session Q --driver VER --plot trackmap
echo ""

read -p "Press Enter to continue to next example..."

# Example 6: Data export
echo "💾 Example 6: Export Telemetry Data"
echo "-----------------------------------"
echo "Command: python main.py --year 2024 --track Monaco --session Q --driver VER --export --output verstappen_monaco.csv"
echo ""
python main.py --year 2024 --track Monaco --session Q --driver VER --export --output verstappen_monaco.csv
echo ""

read -p "Press Enter to continue to next example..."

# Example 7: List available tracks
echo "📋 Example 7: List Available Tracks"
echo "-----------------------------------"
echo "Command: python main.py --year 2024 --list-tracks"
echo ""
python main.py --year 2024 --list-tracks
echo ""

read -p "Press Enter to continue to next example..."

# Example 8: Different session types
echo "🏁 Example 8: Different Session Analysis"
echo "----------------------------------------"
echo "Race session analysis:"
echo "Command: python main.py --year 2024 --track Monaco --session R --driver VER --lap fastest --plot trace"
echo ""
python main.py --year 2024 --track Monaco --session R --driver VER --lap fastest --plot trace
echo ""

# Example 9: Multiple track comparison
echo "🌍 Example 9: Different Track Analysis"
echo "--------------------------------------"
echo "Bahrain GP analysis:"
echo "Command: python main.py --year 2024 --track Bahrain --session Q --driver VER --lap fastest --plot trace"
echo ""
python main.py --year 2024 --track Bahrain --session Q --driver VER --lap fastest --plot trace
echo ""

read -p "Press Enter to continue to final example..."

# Example 10: Advanced visualization
echo "🎨 Example 10: Advanced Visualizations"
echo "--------------------------------------"
echo "Gear usage map:"
echo "Command: python main.py --year 2024 --track Monaco --session Q --driver VER --plot gearmap"
echo ""
python main.py --year 2024 --track Monaco --session Q --driver VER --plot gearmap
echo ""

echo "Brake usage map:"
echo "Command: python main.py --year 2024 --track Monaco --session Q --driver VER --plot brakemap"
echo ""
python main.py --year 2024 --track Monaco --session Q --driver VER --plot brakemap
echo ""

echo ""
echo "✨ CLI Examples Complete!"
echo ""
echo "💡 Additional Tips:"
echo "   • Use --help for full parameter list"
echo "   • Use --verbose for detailed output"
echo "   • Check outputs/ directory for generated files"
echo "   • Use --list-drivers to see available drivers for a session"
echo ""
echo "🌐 Try the web interface: python app.py"