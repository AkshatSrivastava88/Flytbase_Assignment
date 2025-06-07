# Flytbase_Assignment
UAV Strategic Deconfliction: A modular Python + Webots system to detect and visualize 3D drone conflicts via spatial, temporal, and altitude analysis.

🚁 UAV Strategic Deconfliction System

This project is a complete end-to-end simulation, analysis, and visualization system that detects conflicts between UAV (drone) trajectories in a shared airspace. It was developed as part of the FlytBase Robotics Assignment 2025.

✅ What it Does

Loads drone mission paths from structured JSON files (primary and simulated drones)

Simulates 3D flight paths based on waypoints

Detects spatial, temporal, and altitude conflicts

Categorizes conflict severity (high / medium / low)

Provides interactive 3D visualizations using Plotly

Allows filtering by conflict type and severity

📁 Project Directory Structure

Flytbase_Assignment/
├── conflict_checker/        # Core conflict detection logic
│   ├── spatial.py           # 3D distance-based detection
│   ├── temporal.py          # Time-offset detection
│   └── __init__.py
├── data/                    # Input and output files
│   ├── primary_mission.json
│   ├── simulated_drones.json
│   └── detected_conflicts.json
├── visualizer.py            # 3D plotting logic (Matplotlib + Plotly)
├── utils.py                 # Data loaders, filters, and JSON helpers
├── main.py                  # Project entry point
├── README.md                # This file
├── reflection.md            # Design decisions and learnings
└── visualizations/          # Auto-generated interactive plots

▶️ How to Run the Project (Simplified)
Setup Python Environment

bash
python -m venv venv
source venv/bin/activate     # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt

Ensure JSON Mission Files Exist

data/primary_mission.json and data/simulated_drones.json must be correctly formatted.

If missing or malformed, the program will fallback to sample drone paths.

Run Conflict Detection & Visualization

bash
python main.py


Loads drone missions

Detects conflicts (spatial, temporal, altitude)

Outputs summary report and saves detected_conflicts.json

Launches interactive 3D Plotly visualization with conflict filters

(Optional) Run 3D Drone Simulation in Webots

Open the .wbt world file in Webots

Run controller.py for each drone to simulate flight following waypoints

Observe drone trajectories and conflict scenarios in 3D

Note: PID tuning is ongoing; simulation is functional but may need refinement for smooth flight

🔍 Sample Output
3D drone flight paths (lines + waypoints)

Color-coded conflict markers (red/orange/yellow) showing conflict points

Hover labels with conflict type, severity, distance, and involved drones

Console and JSON conflict summaries

🧪 Test Scenarios Included
One primary drone vs two simulated drones

Conflicts include:

Spatial conflict

Temporal conflict

Combined spatial-temporal conflict

Non-conflicting drone paths for comparison

🧠 Technologies Used
Python 3.11

NumPy & SciPy: interpolation and distance calculations

Matplotlib: static 3D visualization

Plotly: interactive HTML dashboards

Dataclasses: object-oriented drone and conflict modeling

Webots simulator: 3D UAV flight simulation with Mavic 2 Pro drones
