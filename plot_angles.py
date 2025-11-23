import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2

def animate_frames(frames):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111, projection='3d')

    def update(i):
        plot_spider_pose(ax, frames[i])
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval=100)
    plt.show()

def main():
    angles_frame = []
    best_fit = [0.14475136, 0.28525023, 0.21096817, 0.15370002, 0.1714549,  0.18900333,
 0.16273926, 0.13872806, 0.20271205, 0.22673427, 0.17559292, 0.14944604,
 0.19898235, 0.19894825, 0.18391876, 0.15059188, 0.16687085, 0.18306272,
 0.20022314, 0.17763588, 0.19096775, 0.22437265, 0.19513602, 0.16566045] 




    angles_frame.append(list(best_fit))

    animate_frames(angles_frame)


main() # Starts the program
