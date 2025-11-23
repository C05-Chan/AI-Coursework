import random
import math
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2

def generate_frame(): # generates 1 frame (24 angles)
    
    frame = []
    for i in range(8):
        frame.append(round(random.uniform(-0.38,0.38),3)) # 43 degrees of freedom
        # frame.append(round(random.uniform(-2,-0.5),3)) # 143 degrees of freedom below 0 means it cannot angle above coxa
        # frame.append(round(random.uniform(-0.5,0),3)) # 28 degrees of freedom 0 means it cannot angle above femer
        frame.append(round(0,3)) # temp
        frame.append(round(0,3)) # temp

    return(frame)

def fitness_function(population, aimed_start_pos):#
    fitness = []
    legs = []
    simitery_fit = []
    smoothness_fit = []
    target_movment = 0
    fit = 0

    for i in range(len(population)):
        #simitery check that each side moves the same amount the same direction
        for x in range(8):
            legs.append([population[i][x*3],population[i][x*3+1],population[i][x*3+2]])


        # for x in range(4): # checks leg on the left to corrosponding leg on the right
        #     #for y in range(3): # checks all segments of leg
        #     fit += abs(legs[i][0] - legs[7-i][0]) # higher the number the more they are asimetrical so should be punished
        # simitery_fit.insert(i,fit)
        # fit = 0
        
        #smoothness check
        for x in range(24):
            #leg crossing prevention + L/R leg target agustment
            if population[i][x] > 0.36:
                fit += abs(legs[i][0] - aimed_start_pos[x]+target_movment)
                break
            elif population[i][x] < -0.36:
                fit += abs(legs[i][0] + aimed_start_pos[x]+target_movment)
                break

            if population[i][x] > 0.36:
                target_movment = -0.0174533 # about -1 degree
            elif population[i][x] < -0.36:
                target_movment = 0.0174533 # about +1 degree
            else:
                target_movment = 0.0174533

                

            fit += population[i][x] - aimed_start_pos[x] + target_movment
        smoothness_fit.insert(i,fit)
        fit = 0
    
    for i in range(len(population)):
        fitness.append([(smoothness_fit[i]),population[i]])

# simitery_fit[i]+
            
    return fitness

def breeding(prev,current): #cuts two frames at random spots and combines them
    i = random.randint(0,len(prev)-1)
    prevA=prev[:i]
    prevB=prev[i:]
    currentA=current[:i]
    currentB=current[i:]

    for i in range(len(prevB)):
        currentA.append(prevB[i])
    
    for i in range(len(currentB)): 
        prevA.append(currentB[i])

    return prevA,currentA
     
def roulette_selection(ranked_population):# 
    total_sum = 0
    selected = 0
    pre_nums = 0
    normalised_nums = []
    cumulative_sum = []
    selected_cromosones = []
    for i in range(len(ranked_population)):
        scores = [1/(1+fit) for fit, cromo in ranked_population]
        #total_sum += ranked_population[i][0]

    total_sum = sum(scores)

    for i in range(len(ranked_population)):
        normalised_nums = [s / total_sum for s in scores]
        #normalised_nums.append(ranked_population[i][0]/ total_sum)

    for i in range(len(normalised_nums)):
        cumulative_sum.append([normalised_nums[i] + pre_nums, ranked_population[i][1]])
        pre_nums += normalised_nums[i]

    
    for i in range(len(cumulative_sum)): # loops for frames
        selected = random.random() # selects individual
        for x in range(len(cumulative_sum)): # loops to check what individual is selected
            if selected < cumulative_sum[x][0]:
                if x == 0:
                    selected_cromosones.append(cumulative_sum[x]) 
                elif x == len(cumulative_sum):
                    selected_cromosones.append(cumulative_sum[x]) 
                else:
                    selected_cromosones.append(cumulative_sum[x-1]) 
                break
    
    #scaleing check
    # num = 0
    # output= []
    # for i in range(len(cumulative_sum)):
    #     for x in range(len(cumulative_sum)):
    #         if cumulative_sum[i][0] == selected_cromosones[x][0]:
    #             num += 1
    #     if i == len(cumulative_sum)-1:
    #         output.append([abs(cumulative_sum[i-1][0] - cumulative_sum[i][0]),num])
    #     else:

    #         output.append([cumulative_sum[i+1][0] - cumulative_sum[i][0] , num])
    #     num = 0
    # output.sort()
    # for i in range(len(output)):
    #     print(output[i])
    return(selected_cromosones)



    return selected

def mutation(population, mutation_rate): # mutates random angles in all frames in mutaion_rate(0.01) % of the population
    total_mut = 0
    mutated_offspring = []

    for i in range(len(population)): #goes through poulation(Frames)
        if random.random() < mutation_rate: # if under mutation rate(0.01)
            total_mut += 1
            mutated_offspring = population[i] #appends to be mutated frame

            for y in range(len(mutated_offspring)): #goes through angles (24)
                 if random.randint(0,1) == 1:
                    mutated_offspring[y] += (round(random.uniform(-0.02,0.02),2))

            population[i] = mutated_offspring
            mutated_offspring = []

    return population

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
        
        for i in range(len(best_fit)):
            if i+1 > len(best_fit)/2:
                if best_fit[i] >= 0.38:
                    switch[i] = -0.0174533
                elif best_fit[i] <= -0.38:
                    switch[i] =  0.0174533
                
                best_fit[i] += switch[i]
            else:
                if best_fit[i] >= 0.38:
                    switch[i] = 0.0174533
                elif best_fit[i] <= -0.38:
                    switch[i] =  -0.0174533
                best_fit[i] -= switch[i]

        animation.append(list(best_fit))

    program_run_end = time.time()
    print("fin! Runtime: ", round(program_run_end - program_run_start,3),"sec")



    #animate function
    for i in range(len(animation)): 
        # print(animation[i])
        angles_frame.append(animation[i])

    animate_frames(angles_frame)


main() # Starts the program
