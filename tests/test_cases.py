"""
Comprehensive test suite for drone deconfliction system.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from conflict_checker import Waypoint, DroneTrajectory, detect_spatial_conflicts, detect_temporal_conflicts
from utils import merge_conflicts, filter_conflicts_by_severity


class TestDroneDeconfliction(unittest.TestCase):
    """Test suite for drone deconfliction system."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Simple straight-line trajectory
        self.simple_waypoints = [
            Waypoint(0, 0, 100, 0),
            Waypoint(100, 0, 100, 10)
        ]
        
        # Curved trajectory
        self.curved_waypoints = [
            Waypoint(0, 0, 50, 0),
            Waypoint(50, 25, 75, 5),
            Waypoint(100, 50, 100, 10)
        ]
        
        # Conflicting trajectory
        self.conflict_waypoints = [
            Waypoint(0, 50, 100, 2),
            Waypoint(100, -50, 100, 12)
        ]
    
    def test_waypoint_creation(self):
        """Test waypoint creation and methods."""
        w1 = Waypoint(0, 0, 0, 0)
        w2 = Waypoint(3, 4, 0, 1)
        
        self.assertEqual(w1.distance_to(w2), 5.0)
        
        # Test dict conversion
        w_dict = w1.to_dict()
        w_from_dict = Waypoint.from_dict(w_dict)
        self.assertEqual(w1.x, w_from_dict.x)
        self.assertEqual(w1.y, w_from_dict.y)
    
    def test_trajectory_validation(self):
        """Test trajectory validation."""
        # Valid trajectory
        traj = DroneTrajectory("test1", self.simple_waypoints)
        self.assertEqual(len(traj.waypoints), 2)
        
        # Invalid: too few waypoints
        with self.assertRaises(ValueError):
            DroneTrajectory("test2", [Waypoint(0, 0, 0, 0)])
    
    def test_spatial_conflict_detection(self):
        """Test spatial conflict detection."""
        traj1 = DroneTrajectory("drone1", self.simple_waypoints)
        traj2 = DroneTrajectory("drone2", self.conflict_waypoints)
        
        conflicts = detect_spatial_conflicts([traj1, traj2], min_separation=100)
        self.assertGreater(len(conflicts), 0)
        
        # Test conflict properties
        if conflicts:
            conflict = conflicts[0]
            self.assertIn(conflict.drone1_id, ["drone1", "drone2"])
            self.assertIn(conflict.drone2_id, ["drone1", "drone2"])
            self.assertEqual(conflict.conflict_type, 'spatial')
    
    def test_temporal_conflict_detection(self):
        """Test temporal conflict detection."""
        traj1 = DroneTrajectory("drone1", self.simple_waypoints)
        
        # Create trajectory with slight time offset
        offset_waypoints = [
            Waypoint(0, 0, 100, 5),  # Same position, different time
            Waypoint(100, 0, 100, 15)
        ]
        traj2 = DroneTrajectory("drone2", offset_waypoints)
        
        conflicts = detect_temporal_conflicts([traj1, traj2], time_window=10.0)
        # Should detect temporal conflicts
        
    def test_utility_functions(self):
        """Test utility functions."""
        from conflict_checker.temporal import Conflict
        
        # Create dummy conflicts
        w1 = Waypoint(0, 0, 100, 5)
        w2 = Waypoint(10, 10, 100, 5)
        
        conflicts1 = [
            Conflict("d1", "d2", 5, 10, w1, w2, "high", "spatial")
        ]
        conflicts2 = [
            Conflict("d1", "d3", 6, 15, w1, w2, "low", "temporal")
        ]
        
        # Test merge
        merged = merge_conflicts(conflicts1, conflicts2)
        self.assertEqual(len(merged), 2)
        
        # Test filter by severity
        high_only = filter_conflicts_by_severity(merged, "high")
        self.assertEqual(len(high_only), 1)
        self.assertEqual(high_only[0].severity, "high")


def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()

