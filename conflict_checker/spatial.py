
import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass
from scipy.spatial.distance import cdist

from conflict_checker.temporal import Conflict


@dataclass
class Waypoint:
    """Represents a single waypoint with position and time."""
    x: float
    y: float
    z: float
    timestamp: float  # Unix timestamp or seconds from start
    
    def distance_to(self, other: 'Waypoint') -> float:
        """Calculate 3D Euclidean distance to another waypoint."""
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)
    
    def to_dict(self) -> dict:
        """Convert waypoint to dictionary."""
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Waypoint':
        """Create waypoint from dictionary."""
        return cls(
            x=data['x'],
            y=data['y'], 
            z=data['z'],
            timestamp=data['timestamp']
        )


class DroneTrajectory:
    """
    Class to interpolate drone waypoints over time and manage flight paths.
    """
    
    def __init__(self, drone_id: str, waypoints: List[Waypoint]):
        """
        Initialize drone trajectory.
        
        Args:
            drone_id: Unique identifier for the drone
            waypoints: List of waypoints defining the flight path
        """
        self.drone_id = drone_id
        self.waypoints = sorted(waypoints, key=lambda w: w.timestamp)
        self._validate_waypoints()
    
    def _validate_waypoints(self):
        """Validate waypoint data."""
        if len(self.waypoints) < 2:
            raise ValueError(f"Drone {self.drone_id} must have at least 2 waypoints")
        
        timestamps = [w.timestamp for w in self.waypoints]
        if len(set(timestamps)) != len(timestamps):
            raise ValueError(f"Drone {self.drone_id} has duplicate timestamps")
    
    def interpolate_position(self, timestamp: float) -> Optional[Waypoint]:
        """
        Interpolate drone position at a given timestamp.
        
        Args:
            timestamp: Time to interpolate position for
            
        Returns:
            Interpolated waypoint or None if timestamp is outside trajectory bounds
        """
        if timestamp < self.waypoints[0].timestamp or timestamp > self.waypoints[-1].timestamp:
            return None
        
        # Find surrounding waypoints
        for i in range(len(self.waypoints) - 1):
            if self.waypoints[i].timestamp <= timestamp <= self.waypoints[i + 1].timestamp:
                w1, w2 = self.waypoints[i], self.waypoints[i + 1]
                
                # Linear interpolation
                if w2.timestamp == w1.timestamp:
                    return w1
                
                t = (timestamp - w1.timestamp) / (w2.timestamp - w1.timestamp)
                
                return Waypoint(
                    x=w1.x + t * (w2.x - w1.x),
                    y=w1.y + t * (w2.y - w1.y),
                    z=w1.z + t * (w2.z - w1.z),
                    timestamp=timestamp
                )
        
        return None
    
    def get_trajectory_bounds(self) -> Tuple[float, float]:
        """Get the time bounds of the trajectory."""
        return self.waypoints[0].timestamp, self.waypoints[-1].timestamp
    
    def sample_trajectory(self, num_points: int = 100) -> List[Waypoint]:
        """Sample trajectory at regular intervals for visualization."""
        start_time, end_time = self.get_trajectory_bounds()
        timestamps = np.linspace(start_time, end_time, num_points)
        
        return [self.interpolate_position(t) for t in timestamps if self.interpolate_position(t)]

    @classmethod
    def from_mission_data(cls, drone_id: str, mission_waypoints: List[dict]) -> 'DroneTrajectory':
        """Create trajectory from mission JSON data."""
        waypoints = [Waypoint.from_dict(wp) for wp in mission_waypoints]
        return cls(drone_id, waypoints)


def detect_spatial_conflicts(trajectories: List[DroneTrajectory], 
                           min_separation: float = 50.0,
                           time_resolution: float = 1.0) -> List['Conflict']:
    """
    Detect spatial conflicts between drone trajectories.
    
    Args:
        trajectories: List of drone trajectories to analyze
        min_separation: Minimum safe separation distance (meters)
        time_resolution: Time step for conflict detection (seconds)
        
    Returns:
        List of spatial conflicts
    """
    from .temporal import Conflict  # Import here to avoid circular imports
    
    conflicts = []
    
    if len(trajectories) < 2:
        return conflicts
    
    # Find overlapping time ranges
    all_start_times = [traj.get_trajectory_bounds()[0] for traj in trajectories]
    all_end_times = [traj.get_trajectory_bounds()[1] for traj in trajectories]
    
    global_start = max(all_start_times)
    global_end = min(all_end_times)
    
    if global_start >= global_end:
        return conflicts  # No temporal overlap
    
    # Generate time samples
    num_samples = int((global_end - global_start) / time_resolution) + 1
    time_samples = np.linspace(global_start, global_end, num_samples)
    
    # Check each time sample for conflicts
    for timestamp in time_samples:
        positions = {}
        
        # Get positions for all drones at this timestamp
        for traj in trajectories:
            pos = traj.interpolate_position(timestamp)
            if pos:
                positions[traj.drone_id] = pos
        
        # Check all pairs for conflicts
        drone_ids = list(positions.keys())
        for i in range(len(drone_ids)):
            for j in range(i + 1, len(drone_ids)):
                drone1_id, drone2_id = drone_ids[i], drone_ids[j]
                pos1, pos2 = positions[drone1_id], positions[drone2_id]
                
                distance = pos1.distance_to(pos2)
                
                if distance < min_separation:
                    # Determine severity
                    if distance < min_separation * 0.3:
                        severity = 'high'
                    elif distance < min_separation * 0.6:
                        severity = 'medium'
                    else:
                        severity = 'low'
                    
                    conflicts.append(Conflict(
                        drone1_id=drone1_id,
                        drone2_id=drone2_id,
                        timestamp=timestamp,
                        distance=distance,
                        position1=pos1,
                        position2=pos2,
                        severity=severity,
                        conflict_type='spatial'
                    ))
    
    return conflicts
