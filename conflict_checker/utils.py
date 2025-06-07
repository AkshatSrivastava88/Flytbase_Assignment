# ==================== utils.py ====================
"""
Utility functions for the drone deconfliction system.
"""

import json
from typing import List, Dict, Any
from conflict_checker import Waypoint, DroneTrajectory, Conflict


def load_mission_from_json(filepath: str) -> List[DroneTrajectory]:
    """
    Load drone trajectories from JSON mission file.
    
    Expected JSON format:
    {
        "drones": {
            "drone_id": [
                {"x": 0, "y": 0, "z": 100, "timestamp": 0},
                {"x": 100, "y": 50, "z": 120, "timestamp": 10}
            ]
        }
    }
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    trajectories = []
    
    if 'drones' in data:
        for drone_id, waypoints in data['drones'].items():
            trajectory = DroneTrajectory.from_mission_data(drone_id, waypoints)
            trajectories.append(trajectory)
    
    return trajectories


def save_conflicts_to_json(conflicts: List[Conflict], filepath: str):
    """Save conflicts to JSON file."""
    conflict_data = {
        'conflicts': [conflict.to_dict() for conflict in conflicts],
        'summary': {
            'total_conflicts': len(conflicts),
            'high_severity': len([c for c in conflicts if c.severity == 'high']),
            'medium_severity': len([c for c in conflicts if c.severity == 'medium']),
            'low_severity': len([c for c in conflicts if c.severity == 'low'])
        }
    }
    
    with open(filepath, 'w') as f:
        json.dump(conflict_data, f, indent=2)


def merge_conflicts(*conflict_lists: List[List[Conflict]]) -> List[Conflict]:
    """Merge multiple conflict lists and remove duplicates."""
    all_conflicts = []
    for conflict_list in conflict_lists:
        all_conflicts.extend(conflict_list)
    
    # Remove duplicates based on drone pairs and timestamp
    unique_conflicts = []
    seen = set()
    
    for conflict in all_conflicts:
        key = (
            tuple(sorted([conflict.drone1_id, conflict.drone2_id])),
            round(conflict.timestamp, 1)
        )
        if key not in seen:
            seen.add(key)
            unique_conflicts.append(conflict)
    
    return unique_conflicts


def filter_conflicts_by_severity(conflicts: List[Conflict], 
                                min_severity: str = 'low') -> List[Conflict]:
    """Filter conflicts by minimum severity level."""
    severity_order = {'low': 0, 'medium': 1, 'high': 2}
    min_level = severity_order[min_severity]
    
    return [c for c in conflicts if severity_order[c.severity] >= min_level]

