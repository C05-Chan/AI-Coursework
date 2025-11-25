import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# ------------------------------
# Helper: Axis–angle rotation
# ------------------------------
def axis_angle_rotation_matrix(axis, angle):
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c = np.cos(angle)
    s = np.sin(angle)
    C = 1 - c

    R = np.array([
        [x*x*C + c,   x*y*C - z*s, x*z*C + y*s],
        [y*x*C + z*s, y*y*C + c,   y*z*C - x*s],
        [z*x*C - y*s, z*y*C + x*s, z*z*C + c]
    ])
    return R


def rotate_vector(v, axis, angle):
    R = axis_angle_rotation_matrix(axis, angle)
    return R @ v


# ------------------------------
# Forward Kinematics
# ------------------------------
def forward_leg_kinematics2(base_pos, base_angle, joint_angles, segment_lengths):

    theta1, theta2, theta3 = joint_angles  # coxa yaw, femur pitch, tibia pitch
    L1, L2, L3 = segment_lengths

    # j1 = base
    j1 = np.array(base_pos)

    # Coxa upward pitch
    coxa_elev = np.deg2rad(30)

    # Coxa horizontal direction
    horiz = np.array([
        np.cos(base_angle + theta1),
        np.sin(base_angle + theta1),
        0
    ])

    # Axis perpendicular to horizontal → rotate upward
    rot_axis = np.cross(horiz, [0, 0, 1])
    R = axis_angle_rotation_matrix(rot_axis, coxa_elev)
    coxa_dir = R @ horiz

    j2 = j1 + L1 * coxa_dir  # end of coxa

    # femur rotation
    femur_axis = np.cross(coxa_dir, [0, 0, 1])
    femur_axis = femur_axis / np.linalg.norm(femur_axis)
    femur_dir = rotate_vector(coxa_dir, femur_axis, theta2)

    j3 = j2 + L2 * femur_dir

    # tibia rotation
    tibia_axis = np.cross(femur_dir, [0, 0, 1])
    tibia_axis = tibia_axis / np.linalg.norm(tibia_axis)
    tibia_dir = rotate_vector(femur_dir, tibia_axis, theta3)

    j4 = j3 + L3 * tibia_dir

    return j1, j2, j3, j4


# ------------------------------
# Main Plot Function
# ------------------------------
def plot_spider_pose(ax, angles):


    n_legs = 8
    segment_lengths = np.array([1.2, 0.7, 1.0])
    a, b = 1.5, 1.0

    # leg order
    left_leg_angles  = np.deg2rad([45, 75, 105, 135])
    right_leg_angles = np.deg2rad([-135, -105, -75, -45])
    base_angles = np.concatenate([left_leg_angles, right_leg_angles])

    leg_labels = ['L1','L2','L3','L4','R4','R3','R2','R1']

    if len(angles) != 24:
        raise ValueError("angles must be length 24")

    # ---- PLOT SETUP ----
    # fig = plt.figure(figsize=(8,8))
    # ax = fig.add_subplot(111, projection='3d')
    ax.cla() 
    

    ax.set_xlim([-4,4])
    ax.set_ylim([-4,4])
    ax.set_zlim([-2,2])
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    ax.view_init(elev=30, azim=45)
    ax.grid(True)

    # draw body
    t = np.linspace(0, 2*np.pi, 200)
    bx = a * np.cos(t)
    by = b * np.sin(t)
    ax.plot(bx, by, 0, 'k', linewidth=3)
    ax.scatter([a + 0.2], [0], [0], c='r', s=60, marker='^')

    # draw legs
    for i in range(n_legs):
        idx = i*3
        th1, th2, th3 = angles[idx:idx+3]

        ang = base_angles[i]
        x_base = a * np.cos(ang)
        y_base = b * np.sin(ang)
        base_pos = np.array([x_base, y_base, 0.0])

        j1, j2, j3, j4 = forward_leg_kinematics2(base_pos, ang,
                                                 [th1, th2, th3],
                                                 segment_lengths)

        ax.plot([j1[0], j2[0]], [j1[1], j2[1]], [j1[2], j2[2]], 'k')
        ax.plot([j2[0], j3[0]], [j2[1], j3[1]], [j2[2], j3[2]], 'b')
        ax.plot([j3[0], j4[0]], [j3[1], j4[1]], [j3[2], j4[2]], 'r')
        ax.scatter([j4[0]], [j4[1]], [j4[2]], c='r', s=30)

