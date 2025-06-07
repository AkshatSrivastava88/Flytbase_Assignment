🧭 Project Reflection & Design Justification
UAV Strategic Deconfliction System

👋 About Me
I’m Akshat Srivastava, a robotics software engineer in training. I developed this project independently to simulate, detect, and visualize trajectory conflicts for UAV fleets operating in shared airspace.

💡 Architectural and Design Decisions
📦 Modular Design for Scalability and Testing
The codebase is organized into clear modules by responsibility:

Conflict detection logic

Utility functions

Visualization components

Execution and control

This modularity makes the system easier to maintain, extend, and test incrementally.

🧱 Object-Oriented Modeling
Core concepts like Waypoint and DroneTrajectory are modeled as Python @dataclass objects for clarity and immutability.

Conflict events are also structured objects carrying metadata such as severity, position, and type.

This design simplifies debugging, filtering, and future feature addition.

🎯 Resilience by Design
If mission JSON files are missing or incomplete, the system falls back to hardcoded demo missions.

Each module provides detailed logging to track execution progress and failure points, aiding troubleshooting.

🔍 How Conflict Detection Works
🛰 Spatial Conflict Detection
Compares 3D Euclidean distances between all drone positions sampled at overlapping timestamps.

If the distance between drones falls below a threshold (e.g., 30 meters), a spatial conflict is flagged.

Severity levels are assigned based on distance:

High: < 10 m

Medium: < 20 m

Low: otherwise

🕒 Temporal Conflict Detection
Checks if drones pass through the same spatial region within a short time window (e.g., 15 seconds), accounting for slight time offsets.

This simulates risk from timing delays or asynchronous flight schedules.

🧭 Altitude Conflict Detection
If drones share the same (x, y) position but have insufficient vertical separation (e.g., less than 20 m), an altitude conflict is recorded.

These conflicts can be toggled on/off in the visualizer.

🕹️ Webots 3D Simulation and Controller Development
Developed a 3D UAV flight simulation using Webots with Mavic 2 Pro drones as models.

Designed controller.py to handle drone flight control by reading mission waypoints from primary_mission.json and simulated_drones.json.

Drones successfully follow waypoint paths in the simulation, demonstrating realistic spatial trajectories that correspond to conflict scenarios defined in the .wbt world file.

The simulation visually confirms drone movement and waypoint navigation, illustrating conflict occurrences in real-time.

PID controller tuning is ongoing; the current implementation allows functional flight but lacks full stability and smoothness, indicating further refinement is needed for production-grade simulation.

This simulation serves as a proof of concept bridging mission planning and physical drone behavior in a controlled virtual environment.

🤖 Use of AI Tools
GPT-4 (OpenAI)

Assisted in brainstorming system architecture and modular design.

Suggested refactoring visualization code into reusable components.

Reviewed and explained time-based conflict detection logic.

Claude AI (Anthropic)

Helped restructure data classes and format documentation.

Provided comparative insights on coding patterns.

Accelerated editing of reflection and design documents.

Note: No AI-generated code was used directly; AI tools were employed to accelerate design and documentation workflows, not to substitute core development.

🧪 Testing Strategy
Tested with 3 distinct mission setups:

One containing only spatial conflicts

One with temporal-only conflicts

One combining spatial and temporal conflicts

Included a non-conflicting drone path for negative testing.

🔄 Edge Cases Considered
Duplicate or overlapping timestamps

Empty or missing mission files

Mission start/end boundary overlaps

Altitude-only separation conflicts

🚀 Scaling Towards Real-World Systems
To scale this system to manage 10,000+ drones in near real-time:

⚙️ Code Efficiency
Use vectorized interpolation with NumPy for fast trajectory sampling.

Parallelize conflict detection with multiprocessing or joblib.

📦 Data Handling
Migrate from file-based JSON to spatial databases like PostGIS for efficient querying.

Implement spatial indexing (KD-Trees, R-Trees) to speed up 3D proximity searches.

📊 Visualization
Use tile-based WebGL rendering (e.g., deck.gl) for scalable 3D visualizations.

Dynamically reduce trajectory resolution to improve rendering performance.

❤️ Final Thoughts
This project was more than a coding challenge — it was a real-world inspired simulation requiring architectural foresight, spatial reasoning, and clear communication. I enjoyed building a foundation for a larger airspace traffic management system and look forward to evolving it further.

Thank you for reviewing my work!
