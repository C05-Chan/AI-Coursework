import matplotlib.pyplot as plt
from spider_plot import plot_spider_pose

def test_spider_plot():
    """
    Generates a single 'full extension' frame for the spider
    so you can check that the plot_spider_pose function
    plots correctly.
    """
    # 8 legs * 3 joints = 24 angles
    # Coxa: 0 (centered), Femur: -1.0, Tibia: -0.5
    test_frame = []
    for leg in range(8):
        test_frame.append(0.0)    # Coxa
        test_frame.append(-1.0)   # Femur
        test_frame.append(-0.5)   # Tibia

    # Plot the frame
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])
    ax.set_zlim([-2, 2])

    plot_spider_pose(ax, test_frame)
    ax.set_title("Test Spider Plot: Full Extension Frame")
    plt.show()

# Call the test
test_spider_plot()
