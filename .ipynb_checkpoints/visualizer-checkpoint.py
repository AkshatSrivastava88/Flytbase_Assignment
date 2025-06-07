import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import json

def load_data():
    with open("data/primary_mission.json") as f:
        primary = json.load(f)
    with open("data/simulated_drones.json") as f:
        simulated = json.load(f)
    return primary, simulated

def plot_3d_animated(primary, simulated):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    drones = [("Primary", primary, 'red')] + [(d['mission_id'], d, 'blue') for d in simulated]

    lines = []
    points = []

    for name, drone, color in drones:
        wp = drone['waypoints']
        xs = [p['x'] for p in wp]
        ys = [p['y'] for p in wp]
        zs = [p['z'] for p in wp]

        (line,) = ax.plot([], [], [], label=name, color=color)
        (point,) = ax.plot([], [], [], marker='o', color=color)
        lines.append((line, xs, ys, zs))
        points.append((point, xs, ys, zs))

    ax.set_xlim(0, 250)
    ax.set_ylim(0, 250)
    ax.set_zlim(0, 80)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Altitude (Z)')
    ax.legend()

    max_len = max(len(l[1]) for l in lines)

    def update(frame):
        for i in range(len(lines)):
            line, xs, ys, zs = lines[i]
            point, _, _, _ = points[i]

            end = min(frame + 1, len(xs))
            line.set_data(xs[:end], ys[:end])
            line.set_3d_properties(zs[:end])
            if end > 0:
                point.set_data(xs[end-1:end], ys[end-1:end])
                point.set_3d_properties(zs[end-1:end])
        return [l[0] for l in lines] + [p[0] for p in points]

    ani = FuncAnimation(fig, update, frames=max_len, interval=1000, repeat=False)
    plt.show()

if __name__ == "__main__":
    primary, simulated = load_data()
    plot_3d_animated(primary, simulated)

