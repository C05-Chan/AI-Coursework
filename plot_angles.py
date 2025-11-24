import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2

def animate_frames(frames):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111, projection='3d')

    def update(i):
        plot_spider_pose(ax, frames[i])
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval=10000)
    plt.show()

def main():
    angles_frame = []
    best_fit = [
        -0.083, -1.978, -0.176,
        -0.332, -1.556, -0.129,
        0.306, -1.865, -0.453,
        0.316, -0.598, -0.113,
        0.34, -0.548, -0.187,
        -0.298, -1.778, -0.129,
        -0.322, -1.769, -0.466,
        -0.365, -1.395, -0.304
    ]




    angles_frame.append(list(best_fit))

    animate_frames(angles_frame)


main() # Starts the program
