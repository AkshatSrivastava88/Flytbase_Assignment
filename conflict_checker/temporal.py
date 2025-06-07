# ==================== conflict_checker/temporal.py ====================
"""
Temporal conflict detection and data structures.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from .spatial import Waypoint, DroneTrajectory


@dataclass
class Conflict:
    """Represents a detected conflict between two drones."""
    drone1_id: str
    drone2_id: str
    timestamp: float
    distance: float
    position1: Waypoint
    position2: Waypoint
    severity: str  # 'high', 'medium', 'low'
    conflict_type: str  # 'spatial', 'temporal', 'altitude'
    
    def to_dict(self) -> dict:
        """Convert conflict to dictionary for JSON serialization."""
        return {
            'drone1_id': self.drone1_id,
            'drone2_id': self.drone2_id,
            'timestamp': self.timestamp,
            'distance': self.distance,
            'position1': self.position1.to_dict(),
            'position2': self.position2.to_dict(),
            'severity': self.severity,
            'conflict_type': self.conflict_type
        }


def detect_temporal_conflicts(trajectories: List[DroneTrajectory],
                            time_window: float = 10.0,
                            min_separation: float = 50.0) -> List[Conflict]:
    """
    Detect temporal conflicts (same area at different times but within window).
    
    Args:
        trajectories: List of drone trajectories
        time_window: Time window to check for temporal conflicts (seconds)
        min_separation: Minimum spatial separation (meters)
        
    Returns:
        List of temporal conflicts
    """
    conflicts = []
    
    # For each pair of trajectories
    for i in range(len(trajectories)):
        for j in range(i + 1, len(trajectories)):
            traj1, traj2 = trajectories[i], trajectories[j]
            
            # Sample both trajectories
            samples1 = traj1.sample_trajectory(50)
            samples2 = traj2.sample_trajectory(50)
            
            # Check for temporal conflicts
            for wp1 in samples1:
                for wp2 in samples2:
                    # Check if they're close in space
                    distance = wp1.distance_to(wp2)
                    if distance < min_separation:
                        # Check if they're close in time
                        time_diff = abs(wp1.timestamp - wp2.timestamp)
                        if 0 < time_diff <= time_window:
                            severity = 'high' if time_diff < time_window * 0.3 else 'medium'
                            
                            conflicts.append(Conflict(
                                drone1_id=traj1.drone_id,
                                drone2_id=traj2.drone_id,
                                timestamp=min(wp1.timestamp, wp2.timestamp),
                                distance=distance,
                                position1=wp1,
                                position2=wp2,
                                severity=severity,
                                conflict_type='temporal'
                            ))
    
    return conflicts


def detect_altitude_conflicts(trajectories: List[DroneTrajectory],
                            min_altitude_separation: float = 20.0) -> List[Conflict]:
    """Detect altitude-specific conflicts."""
    # Implementation for altitude conflicts
    return []