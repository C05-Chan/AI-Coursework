import random
import math
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2

best_fitness = []

# =========================== #
# CONSTANTS BOUNDARIES        #
# =========================== #

coxa_boundary = (-0.38, 0.38)
femur_boundary = (-2, -0.5)
tibia_boundary = (-0.5, 0)

joint_boundaries = [
    coxa_boundary,
    femur_boundary,
    tibia_boundary
]


def generate_frame():
    # ============================================================ #
    # Generates a single RANDOM frame inside of our set boundaries #
    # ============================================================ #

    frame = []

    for _ in range(8):
        # Instead of random.uniform(*coxa_boundary)
        frame.append(round(random.uniform(coxa_boundary[0], coxa_boundary[1]), 3))
        frame.append(round(random.uniform(femur_boundary[0], femur_boundary[1]), 3))
        frame.append(round(random.uniform(tibia_boundary[0], tibia_boundary[1]), 3))

    return frame


def fitness_function(reference, candidate, change):
    # ========================================================================================================== #
    # Evaluates how close a proposed next frame (candidate) is to the last frame (reference) + a change (change) #
    # Change makes sure to favor frames that are different from the last frame                                   #
    # ========================================================================================================== #

    fitness = 0
    for i in range(len(reference)):
        fitness += (abs(reference[i] - candidate[i] - change[i])*100)**2

    return fitness


def roulette_selection(ranked_population):
    # =============================================================================================================================== #
    # This selects random individuals of the current populations.                                                                     #
    # While a higher fitness equals to a higher chance to be selected, the process is still random, as all individuals have a chance. #
    # =============================================================================================================================== #
    # We have to use 1 / (1 + i[0]) ** 2 to assign the chance,
    # as a value assigned by the fitness function is equal to a better fitness
    # but should reflect a higher chance
    # +1 so we don't divide by 0
    sum = 0
    for i in ranked_population:
        sum += 1 / (1 + i[0]) ** 2

    roulette_wheel = []
    prev = 0
    for i in ranked_population:
        value = 1 / (1 + (i[0]) ** 2)
        roulette_wheel.append([prev + value / sum, i[1]]) #Assigns "area on the roulette wheel" and "position"
        prev += value / sum # position for the next one

    selected = []
    for _ in range(len(ranked_population)): # selects as many as the population is big
        rand = random.random()
        for a in range(len(roulette_wheel)):
            if roulette_wheel[a][0] > rand: # finds the selected individual on the "roulette wheel"
                selected.append(roulette_wheel[a][1])
                break # break or everything after the selected gets added

    return selected


def crossover(selected):
    # =============================================================================================== #
    # This function crosses two of the selected frames at a random crossover point to make two child frames.   #
    # The two children have nothing in common:                                                        #
    # E.g.: [p1, p2, p3, p4, p5] + [q1, q2, q3, q4, q5] => [p1,p2, q3, q4, q5] + [q1, q2, p3, p4, p5] #
    # =============================================================================================== #

    out_population = []

    for i in range(0, len(selected), 2):

        parent1 = selected[i]

        if i + 1 < len(selected):  # this is so that if the selected list in odd, the last parent would get paired with a random other parent.
            parent2 = selected[i + 1]
        else:
            parent2 = random.choice(selected)

        crossover_point = random.randint(1, len(parent1) - 1) # random crossover point

        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

        out_population.append(child1)
        out_population.append(child2)

    return out_population


def mutate(population):
    # ====================================================================================== #
    # Loops through the entire population and their alleles. If selected (chance: 2%) their  #
    # their value is changed to a random value inside the boundaries                         #
    # ====================================================================================== #

    mutation_rate = 0.002

    for inv in range(len(population)): # loop through population
        for i in range(len(population[inv])): # loop through allele
            if random.random() < mutation_rate:
                boundary = joint_boundaries[i % 3] # to make sure to use the right boundaries for each angle

                min_val = boundary[0]
                max_val = boundary[1]

                population[inv][i] = round(random.uniform(min_val, max_val), 3) # assigns random value within boundaries

    return population


def change_vector(latest_frame, last_change):
    # ====================================================================================== #
    # This function defines by which values the new angles should be different in comparison #
    # to the last ones. It also makes sure that the direction of movement generally stays the#
    # the same and only changes if out of border or by a small chance (2.5%)                 #
    # ====================================================================================== #

    change = []

    change_direction_prob = 0.025  # probability of a direction change
    change_scale = 0.2 # metric to define by approximately how much the change should be

    boundary_flat = [
        coxa_boundary[0], coxa_boundary[1],
        femur_boundary[0], femur_boundary[1],
        tibia_boundary[0], tibia_boundary[1]
    ]

    # Determines if the direction of change should stay the same.
    for i in range(len(last_change)):
        b_index = i % 3

        if (random.random() > change_direction_prob and boundary_flat[b_index * 2] < latest_frame[i] < boundary_flat[b_index * 2 + 1]): # if it goes out of boundary, always change direction, otherwise random
            change.append(last_change[i])
        else:
            if latest_frame[i] > boundary_flat[b_index * 2 + 1]: # this ensures that if outside the border it will always seek to get inside again
                a = -1
            elif latest_frame[i] < boundary_flat[b_index * 2 ]: # same for the lower border
                a = 1
            elif last_change[i] > 0: # this is to change the direction
                a = -1
            else:
                a = 1

            change.append(round(random.random() * change_scale * a, 3)) # random new value in opposite direction

    return change


def geneticA(latest_frame, last_change, size, generations):
    # ================================================== #
    # This is the main function of the genetic Algorithm #
    # ================================================== #
    change = change_vector(latest_frame, last_change)
    #This initializes the first generation
    population = []
    for _ in range(size):
        population.append(generate_frame())

    avg_fitness_per_gen = [] # stores average fitness

    #This starts the loop for the GA
    while generations > 1:
        generations -= 1 # counter for the generations

        rated_population = []
        total_fitness = 0

        for frame in population:
            fitness = fitness_function(latest_frame, frame, change) # computes a fitness
            rated_population.append([fitness, frame]) # assigns the fitness to the frame
            total_fitness += fitness # for average fitness
        avg_fitness_per_gen.append(total_fitness / len(population))  # stores average fitness
        # selection
        selected = roulette_selection(rated_population)

        # reproduction
        population = crossover(selected)

        # mutation
        population = mutate(population)

    #This loop searches for the best frame after the GA ends
    best = [10000, []]
    for frame in population:
        if best[0] > fitness_function(latest_frame, frame, change):
            best[0] = fitness_function(latest_frame, frame, change)
            best[1] = frame

    print("best", [best[0]]) # Print to monitor the archived fitness of the final frame
    best_fitness.append([best[0]])
    return best[1], change, avg_fitness_per_gen


def animate_frames(frames, speed = 200):
    # ============================================================================== #
    # This is code to visualize the frames and has nothing to do with the actual GA. #
    # ============================================================================== #
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    def update(i):
        plot_spider_pose(ax, frames[i])
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval=speed)
    plt.show()

def plot_graph(avg_fitness_across_frames):
    # ============================================================================== #
    # This is code to visualize average progression of the archived fitness after    #
    # each generation.                                                               #
    # ============================================================================== #
    # Plot average fitness progression across all frames (log scale)
    plt.figure(figsize=(10,5))
    plt.plot(avg_fitness_across_frames, label="Average Fitness Across All Frames")
    plt.yscale("log")
    plt.grid(True, which="both", ls="-", color='0.7', alpha=0.5)
    plt.xlabel("Generation")
    plt.ylabel("Average Fitness (log scale)")
    plt.title("Average Fitness Progression Across All Generations & Frames")
    plt.legend()
    plt.show()


def main():
    # ============================================================================== #
    # This is the main function                                                      #
    # In the following the parameters of the GA and the animation can be changed     #
    # ============================================================================== #

    #These two define how good the GA will be and how long it will take.
    #Generations defines how many iterations the GA is running through
    generations = 250
    #Population_size
    population_size = 150

    #How fast should the Animation run for?
    speed = 200
    #How many frames should the Animation have?
    amount_frames = 300


    latest_frame = generate_frame()
    total_frames = [latest_frame]

    change = [random.choice([0.1,-0.1]) for _ in range(24)]

    all_avg_fitness_gen = []  # stores avg fitness per generation for each frame

    # Run GA for each frame
    while len(total_frames) < amount_frames:
        print("progress", len(total_frames)) # This indicates how far the program is while it is running
        new_frame, change, avg_fitness_per_gen = geneticA(latest_frame, change, population_size, generations)
        total_frames.append(new_frame)
        latest_frame = new_frame # remember the newest frame for the next GA

        all_avg_fitness_gen.append(avg_fitness_per_gen) # This is for the graph

    num_gen = len(all_avg_fitness_gen[0])
    avg_fitness_frames = []

    #This is for the graph
    for gen in range(num_gen):
        generation_sum = 0

        for frame_avg in all_avg_fitness_gen:
            generation_sum += frame_avg[gen]

        generation_average = generation_sum / len(all_avg_fitness_gen)

        avg_fitness_frames.append(generation_average)

    # This is to save the generated data in a csv to use in the Neural Network
    filename = 'output_data.csv'

    try:
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(total_frames)

        print(f"Successfully wrote data to {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")


    animate_frames(total_frames, speed) # This is to animate the frames

    plot_graph(avg_fitness_frames) # This is to plot the graph


main()