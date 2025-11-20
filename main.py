import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2



# def check_if_legs_cross(angles):
#     is_bad = False
#     base_angle = [45, ]

#     return (is_bad)

def generate_angles(): # generates 1 frame
    gaits = [[]]
    
    for x in range(300):
        angles = []
        for i in range(8):
            angles.append(round(random.uniform(-0.38,0.38),3))
            angles.append(round(random.uniform(-0.5,-2),3))
            angles.append(round(random.uniform(-0.5,0),3))
            # angles.append(round(random.uniform(0,6.28),3)) #only in range that is (360 degrees)
        gaits.insert(x,angles)

    return(gaits)

def fitness_function(prev,frame):   #this calculates a how good the frame fits to the previous frame with a slight difference
    fitness = 0
    for i in range(len(prev)):
        if prev[i] < frame[i]:
            fitness += (prev[i] - frame[i] - 0.2)^(4-i) # punishes less if the further the
        else:
            fitness += (prev[i] - frame[i] + 0.2)^(4-i)
    return fitness

def breeding(prev,frame): #cuts two frames at random spots and combines them
    i = random.randint(0,len(prev)-1)

    prevA=prev[:i]
    prevB=prev[i+1:]
    frameA=frame[:i]
    frameB=frame[i+1:]

    new1 = []
    new2 = []
    new1.append(prevA)
    new1.append(frameB)

    new2.append(frameA)
    new2.append(prevB)

    return new1, new2  
     
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
    
    for i in range(len(cumulative_sum)):
        selected = random.random()
        for i in range(len(cumulative_sum)):
            if selected < cumulative_sum[i][0]:
                selected_cromosones.append(cumulative_sum[i][0])
                break
    return(selected_cromosones)

def mutation(population, mutation_rate):
    mutated_offspring = []
    for i in range(len(population)): #goes through animations
        for x in range(len(population[0])): # goes through frames in an individual
            if random.random() < mutation_rate: # if under mutation rate
                mutated_offspring.append(population[i][x]) #
                for y in range(len(mutated_offspring)):
                    if random.randint(0,1) == 1:
                        mutated_offspring[y] = (round(random.random(),2))
                print(i,x)
                population[i][x] = mutated_offspring
                
    return (population)

def animate_frames(frames):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111, projection='3d')

    def update(i):
        plot_spider_pose(ax, frames[i])
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval=500)
    plt.show()


def main():
    mutation_rate = 1
    population_size = 1
    population = [[]]
    generations = 10
    

    for i in range(population_size):
        population.insert(i,generate_angles())
    print(population)
    print(mutation(population, mutation_rate))

    # for i in generations:
    #     fitness = fitness_function(population)
    #     selected = roulette_selection(fitness)
    #     offspring = breeding(selected)
    #     population = mutation(offspring, mutation_rate)

    # angles_frame = []
    
    # print(population[0][0])
    # for i in range(300):
    #     angles_frame.append(population[0][i])

    # animate_frames(angles_frame)
    # animate_frames(population[0])


main() # Starts the program frame[[1,2,3]]
