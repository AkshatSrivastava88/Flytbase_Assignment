"""
Visualization components for drone trajectories and conflicts.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import List, Tuple, Optional

from conflict_checker import DroneTrajectory, Conflict


class DroneVisualizer:
    """Enhanced visualizer for drone trajectories and conflicts."""

    def __init__(self, trajectories: List[DroneTrajectory], conflicts: List[Conflict] = None):
        self.trajectories = trajectories
        self.conflicts = conflicts or []

    def plot_3d_trajectories_matplotlib(self, 
                                      show_conflicts: bool = True, 
                                      figsize: Tuple[int, int] = (12, 8),
                                      save_path: Optional[str] = None):
        """Create 3D trajectory plot using matplotlib."""
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')

        colors = plt.cm.Set1(np.linspace(0, 1, len(self.trajectories)))

        # Plot trajectories
        for traj, color in zip(self.trajectories, colors):
            waypoints = traj.sample_trajectory(100)

            xs = [w.x for w in waypoints]
            ys = [w.y for w in waypoints]
            zs = [w.z for w in waypoints]

            ax.plot(xs, ys, zs, label=f'Drone {traj.drone_id}', color=color, linewidth=2)

            # Mark start and end points
            ax.scatter([xs[0]], [ys[0]], [zs[0]], color=color, s=100, marker='o', alpha=0.8)
            ax.scatter([xs[-1]], [ys[-1]], [zs[-1]], color=color, s=100, marker='s', alpha=0.8)

        # Plot conflicts
        if show_conflicts and self.conflicts:
            marker_map = {'spatial': 'X', 'temporal': '^', 'altitude': 'v'}
            color_map = {'high': 'red', 'medium': 'orange', 'low': 'yellow'}
            for conflict in self.conflicts:
                marker = marker_map.get(conflict.conflict_type, 'X')
                color = color_map.get(conflict.severity, 'gray')
                ax.scatter([conflict.position1.x, conflict.position2.x],
                          [conflict.position1.y, conflict.position2.y],
                          [conflict.position1.z, conflict.position2.z],
                          color=color, s=150, marker=marker, alpha=0.8)
                ax.plot(
                    [conflict.position1.x, conflict.position2.x],
                    [conflict.position1.y, conflict.position2.y],
                    [conflict.position1.z, conflict.position2.z],
                    color=color, linestyle='dashed', linewidth=1
                )

        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Drone Trajectories and Conflicts')
        ax.legend()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig, ax

    def plot_interactive_3d_plotly(self, 
                                  show_conflicts: bool = True,
                                  conflict_types: Optional[List[str]] = None,
                                  severities: Optional[List[str]] = None,
                                  save_path: Optional[str] = None):
        """Create interactive 3D plot using plotly with conflict filters."""
        fig = go.Figure()

        colors = px.colors.qualitative.Set1

        # Plot trajectories
        for i, traj in enumerate(self.trajectories):
            waypoints = traj.sample_trajectory(100)

            xs = [w.x for w in waypoints]
            ys = [w.y for w in waypoints]
            zs = [w.z for w in waypoints]
            times = [w.timestamp for w in waypoints]

            color = colors[i % len(colors)]

            fig.add_trace(go.Scatter3d(
                x=xs, y=ys, z=zs,
                mode='lines+markers',
                name=f'Drone {traj.drone_id}',
                line=dict(color=color, width=4),
                marker=dict(size=3),
                hovertemplate=f'Drone {traj.drone_id}<br>X: %{{x}}<br>Y: %{{y}}<br>Z: %{{z}}<br>Time: %{{customdata}}<extra></extra>',
                customdata=times
            ))

        # Plot conflicts with filters
        if show_conflicts and self.conflicts:
            conflict_colors = {'high': 'red', 'medium': 'orange', 'low': 'yellow'}
            conflict_symbols = {'spatial': 'x', 'temporal': 'cross', 'altitude': 'diamond'}

            for conflict in self.conflicts:
                ctype = conflict.conflict_type
                severity = conflict.severity

                if (conflict_types and ctype not in conflict_types) or (severities and severity not in severities):
                    continue

                fig.add_trace(go.Scatter3d(
                    x=[conflict.position1.x, conflict.position2.x],
                    y=[conflict.position1.y, conflict.position2.y],
                    z=[conflict.position1.z, conflict.position2.z],
                    mode='lines+markers',
                    name=f'{ctype.title()} Conflict ({severity})',
                    marker=dict(
                        color=conflict_colors.get(severity, 'gray'),
                        size=10,
                        symbol=conflict_symbols.get(ctype, 'x')
                    ),
                    line=dict(
                        color=conflict_colors.get(severity, 'gray'),
                        width=2,
                        dash='dash'
                    ),
                    hovertemplate=f'Conflict: {conflict.drone1_id} vs {conflict.drone2_id}<br>Type: {ctype}<br>Severity: {severity}<br>Distance: {conflict.distance:.1f}m<br>Time: {conflict.timestamp}<extra></extra>'
                ))

        fig.update_layout(
            title='Interactive Drone Trajectory Visualization',
            scene=dict(
                xaxis_title='X (m)',
                yaxis_title='Y (m)',
                zaxis_title='Z (m)'
            ),
            height=700,
            legend=dict(
                title='Legend',
                itemsizing='constant'
            )
        )

        if save_path:
            fig.write_html(save_path)

        return fig

    def generate_conflict_report(self) -> str:
        """Generate a detailed text report of detected conflicts."""
        if not self.conflicts:
            return "✅ No conflicts detected."

        report = f"🚨 Conflict Detection Report\n{'='*50}\n\n"
        report += f"Total conflicts detected: {len(self.conflicts)}\n\n"

        by_severity = {'high': [], 'medium': [], 'low': []}
        for conflict in self.conflicts:
            by_severity[conflict.severity].append(conflict)

        for severity in ['high', 'medium', 'low']:
            conflicts = by_severity[severity]
            if conflicts:
                emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[severity]
                report += f"{emoji} {severity.upper()} SEVERITY CONFLICTS ({len(conflicts)}):\n"
                report += "-" * 40 + "\n"

                for conflict in conflicts:
                    report += f"Drones: {conflict.drone1_id} vs {conflict.drone2_id}\n"
                    report += f"Type: {conflict.conflict_type}\n"
                    report += f"Time: {conflict.timestamp:.1f}s\n"
                    report += f"Distance: {conflict.distance:.2f}m\n"
                    report += f"Positions: ({conflict.position1.x:.1f}, {conflict.position1.y:.1f}, {conflict.position1.z:.1f}) "
                    report += f"and ({conflict.position2.x:.1f}, {conflict.position2.y:.1f}, {conflict.position2.z:.1f})\n\n"

        return report