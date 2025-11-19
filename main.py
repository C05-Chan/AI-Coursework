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
    angles = []
    for i in range(24):
        angles.append(round(random.uniform(0,6.28),3)) #only in range that is (360 degrees)
    return(angles)

def fitness_body_cross(frame): # this checks if the angles are legal (illegal angles means the legs are intersecting the body, etc.)
    fitness = 0
    for i in range(8):
        x = 0
        leg = frame[x: x+3]
        if 0.38 < leg[0] < -0.38:
            fitness += abs(leg[0]*10)
        else:
            fitness += abs(leg[0])
            
        if -0.5 > leg[1] > -2:
            fitness += abs(leg[1]*10)
        else:
            fitness += abs(leg[1])
        
        if 0 > leg[2] > -0.5:
            fitness += abs(leg[2]*10)
        else:
            fitness += abs(leg[2])
        x += 3

    fit_angles = round(fitness,2)
    return (fit_angles,frame)
     
     
def fitness_selection(ranked_population): # tournament style selection output 3 cromosones ' add 2 training dummys 1000 and 1 value
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

def crossover(parent1, parent2):
    i = (random.randint(1,8)) * 3
    child = parent1[0:i] + parent2[i:-1]
    child += parent2[0:i] + parent1[i:-1]

    return (children)

def mutation(fit_offspring):
     mutated_offspring = []
     mutated_offspring = fit_offspring
     for i in range(24):
        if random.randint(0,1) == 1:
            mutated_offspring[i] = (round(random.random(),3))
     return (mutated_offspring)

def new_population(mutated_offspring):
    new_pop = []

    return(new_pop)

def animate_frames(frames):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111, projection='3d')

    def update(i):
        plot_spider_pose(ax, frames[i])
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval=500)
    plt.show()


def main():
    mutation_rate = 0.01
    population_size = 100
    population = []
    fit_population = []
    test_angles = generate_angles()

    for i in range(population_size):
        population.append(generate_angles())
    
    # fitness_rank = 
    for x in range(population_size):
        fit_population.append(fitness_body_cross(population[x]))
    print("input raw: ", fit_population)
    input_fit = []
    for i in range(len(fit_population)):
        input_fit.append(fit_population[i][0])
    print("input fitness:", input_fit)
    output = fitness_selection(fit_population)
        
    print("output:", output)
    print("output length: ", len(output))

    # fit_population = fitness_selection(population)
    # fit_offspring = offspring(fit_population)
    # mutated_offspring = mutation(fit_offspring, mutation_rate)
    # population = new_population(mutated_offspring)
    angles_frame = []

    for _ in range(300):
        angles_frame.append(generate_angles())

    animate_frames(angles_frame)


main() # Starts the program 
