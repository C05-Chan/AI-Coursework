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
    best_fit = [ 0.00718468 ,-1.34869969, -0.28237643 , 0.01891066 ,-1.4417715,  -0.27498149,
  0.00183869, -1.44370105, -0.27432623 ,-0.00498335 ,-1.38651414 ,-0.28629452,
 -0.02459882 ,-1.38303711, -0.2823869  , 0.01435695 ,-1.35437381, -0.26213412,
  0.0244755 , -1.40698533, -0.27629202, -0.02437824, -1.33091741, -0.29276928]





    angles_frame.append(list(best_fit))

    animate_frames(angles_frame)


main() # Starts the program
