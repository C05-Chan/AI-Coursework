import random
import math
import time
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
    #GA parameters
    frames = 100
    
    switch = []
    angles_frame = []
    best_fit = []
    animation = []
    frame_end = 0
    program_run_start = time.time()


    frame_start = time.time()
    for f in range(frames):
        frame_time = frame_end - frame_start
        print("frame: ",f," ", round(frame_time,2) , "sec ", "Program End Eta: ", f"{math.floor(frame_time*(frames-f)/60)}.{round(frame_time*(frames-f)%60)}" , "mins")
        frame_start = time.time()

        if len(best_fit) == 0:
            for i in range(8):
                if i < 4:
                    best_fit.append(0.38)
                else:
                    best_fit.append(-0.38)
                best_fit.append(-0.785)
                best_fit.append(-1.570)
                switch.append(0.0174533)
                switch.append(0.0174533)
                switch.append(0.0174533)


        frame_end = time.time()
        
        # for i in range(len(best_fit)):
        #     if i+1 > len(best_fit)/2:
        #         if best_fit[i] >= 0.38:
        #             switch[i] = -0.0174533
        #         elif best_fit[i] <= -0.38:
        #             switch[i] =  0.0174533
                
        #         best_fit[i] += switch[i]
        #     else:
        #         if best_fit[i] >= 0.38:
        #             switch[i] = 0.0174533
        #         elif best_fit[i] <= -0.38:
        #             switch[i] =  -0.0174533
        #         best_fit[i] -= switch[i]

        for x in range(8):
            if i*3 > 4:
                #COXA
                if best_fit[x*3] >= 0.38:
                    switch[x*3] = -0.0174533
                elif best_fit[x*3] <= -0.38:
                    switch[x*3] = 0.0174533
                #FEMER
                if best_fit[x*3+1] >= -0.5:
                    switch[x*3+1] = -0.0174533
                elif best_fit[x*3+1] <= -0.9:
                    switch[x*3+1] = 0.0174533
                #TIBIA
                if best_fit[x*3+2] >= -0.5:
                    switch[x*3+2] = -0.0174533
                elif best_fit[x*3+2] <= -1.57:
                    switch[x*3+2] = 0.0174533
                best_fit[x*3] += switch[x*3]
                best_fit[x*3+1] += switch[x*3+1]
                best_fit[x*3+2] += switch[x*3+2]


            else:
                #COXA
                if best_fit[x*3] >= 0.38:
                    switch[x*3] = 0.0174533
                elif best_fit[x*3] <= -0.38:
                    switch[x*3] = -0.0174533
                #FEMER
                if best_fit[x*3+1] >= -0.5:
                    switch[x*3+1] = 0.0174533
                elif best_fit[x*3+1] <= -0.9:
                    switch[x*3+1] = -0.0174533
                #TIBIA
                if best_fit[x*3+2] >= -0.5:
                    switch[x*3+2] = -0.0174533
                elif best_fit[x*3+2] <= -1.57:
                    switch[x*3+2] = 0.0174533
                best_fit[x*3] += switch[x*3]
                best_fit[x*3+1] += switch[x*3+1]
                best_fit[x*3+2] += switch[x*3+2]

        animation.append(list(best_fit))

    program_run_end = time.time()
    print("fin! Runtime: ", round(program_run_end - program_run_start,3),"sec")



    #animate function
    for i in range(len(animation)): 
        # print(animation[i])
        angles_frame.append(animation[i])

    animate_frames(angles_frame)


main() # Starts the program
