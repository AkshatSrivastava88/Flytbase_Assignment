import json

def load_primary_mission(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def load_simulated_drones(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)
