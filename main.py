import random
import math
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2

def generate_angles(): # generates 1 animation (300 frames)
    gaits = []
    
    for x in range(299):
        angles = []
        for i in range(8):
            angles.append(round(random.uniform(-0.38,0.38),3))
            angles.append(round(random.uniform(-0.5,-2),3))
            angles.append(round(random.uniform(-0.5,0),3))
        gaits.append(angles)

    return(gaits)

def fitness_function(prev,frame):#this calculates a how good the frame fits to the previous frame with a slight difference (NEEDS RE-WRITEING DESPERATLY)
    fitness = 0
    max_angles = [0.38,-0.5,-0.5]
    min_angles = [-0.38,-2,0]
    for i in range(len(prev)): #loops 24 times
        for x in range(8):
            #checks first part of leg
            if frame[x*3] < max_angles[0]:
                fitness += frame[x*3]
            elif frame[x*3] > min_angles[0]:
                fitness += frame[x*3]
            else:
                fitness -= frame[x*3]

            #checks second part of leg
            if frame[x*3+1] < max_angles[1]:
                fitness += frame[x*3+1]
            elif frame[x*3+1] > min_angles[1]:
                fitness += frame[x*3+1]
            else:
                fitness -= frame[x*3+1]
            
            #checks third part of leg
            fitness -= 3.14-round(frame[x*3+2] + frame[x*3+1],2)
            
    return fitness

def breeding(prev,frame): #cuts two animations at random spots and combines them
    i = random.randint(0,len(prev)-1)

    prevA=prev[:i]
    prevB=prev[i:]
    frameA=frame[:i]
    frameB=frame[i:]

    for i in range(len(prevB)):
        frameA.append(prevB[i])
    
    for i in range(len(prevA)): 
        frameB.append(prevA[i])

    return prev, frame 
     
def roulette_selection(ranked_population): # tournament style selection output 3 chromosones ' add 2 training dummys 1000 and 1 value
    total_sum = 0
    selected = 0
    pre_nums = 0
    normalised_nums = []
    cumulative_sum = []
    selected_cromosones = []
    for i in range(len(ranked_population)):
        total_sum += ranked_population[i][0]

    for i in range(len(ranked_population)):
        normalised_nums.append([ranked_population[i][0] / total_sum,ranked_population[i][1]])

    for i in range(len(normalised_nums)):
        cumulative_sum.append([normalised_nums[i][0] + pre_nums, ranked_population[i][1]])
        pre_nums += normalised_nums[i][0]
    
    for i in range(len(cumulative_sum)): # loops for 300 selected frames
        selected = random.random() # selects individual
        for x in range(len(cumulative_sum)): # loops to check what individual is selected
            if selected < cumulative_sum[x][0]:
                selected_cromosones.append(cumulative_sum[x]) 
                break

    return(selected_cromosones)

def mutation(population, mutation_rate): # mutates random angles in all frames in mutaion_rate(0.01) % of the population
    total_mut = 0
    mutated_offspring = []

    for i in range(len(population)): #goes through animations(population_size)
        if random.random() < mutation_rate: # if under mutation rate(0.01)
            total_mut += 1

            for x in range(len(population[0])): # goes through frames in an individual (300)
                mutated_offspring = population[i][x] #appends to be mutated frame

                for y in range(len(mutated_offspring)): #goes through angles (24)
                    if random.randint(0,1) == 1:
                        mutated_offspring[y] += (round(random.uniform(-0.0872665,0.0872665),2))

                population[i][x] = mutated_offspring
                mutated_offspring = []

    return population

def animate_frames(frames):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111, projection='3d')

    def update(i):
        plot_spider_pose(ax, frames[i])
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval=250)
    plt.show()


def main():
    #GA parameters
    mutation_rate = 0.01
    population_size = 100
    generations = 10

    animation_fitness = 0
    population = []
    fitness = []
    offspring = []
    angles_frame = []
    best_fit = [0,[]]
    gen_end = 0
    program_run_start = time.time()

    #initial generation function
    for i in range(population_size):
        population.append(generate_angles())

    #generation loop
    gen_start = time.time()
    for i in range(generations):
        gen_time = gen_end - gen_start
        print("Generation: ",i," ", round(gen_time,2) , "sec ", "Program End Eta: ", f"{math.floor(gen_time*(generations-i)/60)}.{round(gen_time*(generations-i)%60)}" , "mins")
        gen_start = time.time()

        #fitness function
        for x in range(len(population)): # loops animations
            for y in range(len(population[x])): # loops frames
                if y != len(population[0])-1:
                    animation_fitness += fitness_function(population[x][y], population[x][y+1])
            fitness.append([animation_fitness, population[x]])
            frame_fitness = []
        print("fitness: COMPLETE")

        #selection function
        selected = roulette_selection(fitness)
        for x in range(len(fitness)): # getting best fit animation over entire program run
            if fitness[x][0] <= best_fit[0]:
                best_fit = fitness[x]
        fitness = []
        print("select: COMPLETE")

        #offspring function
        for x in range(round(len(selected)/2)): # loops animations
                if x != len(selected)-1:
                    offspring.append(breeding(selected[x][1], selected[x+1][1])[0])
                    offspring.append(breeding(selected[x][1], selected[x+1][1])[1])
        print("offspring: COMPLETE")

        #mutation function
        population = []
        population = mutation(offspring, mutation_rate)
        offspring = []
        print("mutation: COMPLETE")
        gen_end = time.time()
    program_run_end = time.time()
    print("fin! Runtime: ", round(program_run_end - program_run_start,3),"sec")
    
    #animate function
    for i in range(len(best_fit[1])): 
        angles_frame.append(best_fit[1][i])

    animate_frames(angles_frame)
    animate_frames(best_fit)


main() # Starts the program
