# ==================== main.py ====================
"""
Main execution script for drone deconfliction system.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from conflict_checker import detect_spatial_conflicts, detect_temporal_conflicts
from visualizer import DroneVisualizer
from utils import load_mission_from_json, save_conflicts_to_json, merge_conflicts


def main():
    """Main execution function."""
    print("🚁 Drone Deconfliction System")
    print("=" * 50)
    
    try:
        # Load trajectories from JSON files
        print("📁 Loading mission data...")
        
        primary_trajectories = []
        simulated_trajectories = []
        
        # Try to load primary mission
        if Path("data/primary_mission.json").exists():
            primary_trajectories = load_mission_from_json("data/primary_mission.json")
            print(f"✅ Loaded {len(primary_trajectories)} primary mission trajectories")
        
        # Try to load simulated drones
        if Path("data/simulated_drones.json").exists():
            simulated_trajectories = load_mission_from_json("data/simulated_drones.json")
            print(f"✅ Loaded {len(simulated_trajectories)} simulated trajectories")
        
        all_trajectories = primary_trajectories + simulated_trajectories
        
        if not all_trajectories:
            print("⚠️  No trajectory data found. Creating demo data...")
            all_trajectories = create_demo_trajectories()
        
        # Detect conflicts
        print(f"\n🔍 Analyzing {len(all_trajectories)} trajectories for conflicts...")
        
        spatial_conflicts = detect_spatial_conflicts(
            all_trajectories, 
            min_separation=30.0, 
            time_resolution=0.5
        )
        
        temporal_conflicts = detect_temporal_conflicts(
            all_trajectories,
            time_window=15.0,
            min_separation=50.0
        )
        
        all_conflicts = merge_conflicts(spatial_conflicts, temporal_conflicts)
        
        print(f"📊 Found {len(spatial_conflicts)} spatial conflicts")
        print(f"📊 Found {len(temporal_conflicts)} temporal conflicts")
        print(f"📊 Total unique conflicts: {len(all_conflicts)}")
        
        # Generate visualizations
        print("\n📈 Generating visualizations...")
        visualizer = DroneVisualizer(all_trajectories, all_conflicts)
        
        # Create conflict report
        report = visualizer.generate_conflict_report()
        print("\n" + report)
        
        # Save results
        print("💾 Saving results...")
        save_conflicts_to_json(all_conflicts, "data/detected_conflicts.json")
        
        # Create interactive plot
        fig = visualizer.plot_interactive_3d_plotly()
        fig.write_html("visualizations/drone_trajectories.html")
        print("✅ Interactive visualization saved to visualizations/drone_trajectories.html")
        
        # Show plot in browser
        fig.show()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def create_demo_trajectories():
    """Create demo trajectories for testing."""
    from conflict_checker import Waypoint, DroneTrajectory
    
    # Demo trajectory 1
    waypoints1 = [
        Waypoint(0, 0, 100, 0),
        Waypoint(50, 25, 120, 5),
        Waypoint(100, 50, 100, 10)
    ]
    
    # Demo trajectory 2 (potential conflict)
    waypoints2 = [
        Waypoint(0, 50, 80, 1),
        Waypoint(50, 25, 110, 6),  # Conflict zone
        Waypoint(100, 0, 90, 11)
    ]
    
    # Demo trajectory 3
    waypoints3 = [
        Waypoint(25, 0, 150, 0),
        Waypoint(75, 50, 130, 8),
        Waypoint(100, 100, 110, 12)
    ]
    
    return [
        DroneTrajectory("DEMO_Alpha", waypoints1),
        DroneTrajectory("DEMO_Beta", waypoints2),
        DroneTrajectory("DEMO_Gamma", waypoints3)
    ]


if __name__ == "__main__":
    main()

