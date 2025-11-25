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

    sum = 0
    for i in ranked_population:
        sum += 1 / (1 + i[0]) ** 4

    roulette_wheel = []
    prev = 0
    for i in ranked_population:
        value = 1 / (1 + (i[0]) ** 4)
        roulette_wheel.append([prev + (value) / sum, i[1]])
        prev += (value) / sum

    selected = []
    for _ in range(len(ranked_population)):
        rand = random.random()
        for a in range(len(roulette_wheel)):
            if roulette_wheel[a][0] > rand:
                selected.append(roulette_wheel[a][1])
                break

    return selected


def crossover(selected):
    # =============================================================================================== #
    # This function crosses two parent frames at a random crossover point to make two child frames.   #
    # The two children have nothing in common:                                                        #
    # E.g.: [p1, p2, p3, p4, p5] + [q1, q2, q3, q4, q5] => [p1,p2, q3, q4, q5] + [q1, q2, p3, p4, p5] #
    # =============================================================================================== #

    out_population = []

    for i in range(0, len(selected), 2):

        parent1 = selected[i]

        if i + 1 < len(
                selected):  # this is so that if the selected list in odd, the last parent would get paired with a random other parent.
            parent2 = selected[i + 1]
        else:
            parent2 = random.choice(selected)

        crossover_point = random.randint(1, len(parent1) - 1)

        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

        out_population.append(child1)
        out_population.append(child2)

    return out_population


def mutate(population):
    # ====================================================================================== #
    # This goes through the entire population and their angles and mutates their values to a #
    # random value inside the boundaries with a chance of 0.2%                               #
    # ====================================================================================== #

    mutation_rate = 0.002

    for inv in range(len(population)):
        for i in range(len(population[inv])):
            if random.random() < mutation_rate:
                boundary = joint_boundaries[i % 3]

                min_val = boundary[0]
                max_val = boundary[1]

                population[inv][i] = round(random.uniform(min_val, max_val), 3)

    return population


def change_vector(latest_frame, last_change):
    change = []

    change_direction_prob = 0.025  # probability of a direction change
    change_scale = 0.2

    boundary_flat = [
        coxa_boundary[0], coxa_boundary[1],
        femur_boundary[0], femur_boundary[1],
        tibia_boundary[0], tibia_boundary[1]
    ]

    # Determines if the direction of change should stay the same.
    for i in range(len(last_change)):
        b_index = i % 3

        if random.random() > change_direction_prob and boundary_flat[b_index * 2] < latest_frame[i] < boundary_flat[b_index * 2 + 1]:
            change.append(last_change[i])
            
        else:
            if last_change[i] > 0:
                a = -1
            else:
                a = 1

            change.append(random.random() * change_scale * a)

    return change


def geneticA(latest_frame, last_change, size=500, generations = 500):
    # ================================================== #
    # This is the main function of the genetic Algorithm #
    # ================================================== #
    change = change_vector(latest_frame, last_change)

    population = []
    for _ in range(size):
        population.append(generate_frame())

    avg_fitness_per_gen = []

    while generations > 1:
        generations -= 1

        rated_population = []
        total_fitness = 0
        
        for frame in population:
            fitness = fitness_function(latest_frame, frame, change)
            rated_population.append([fitness, frame])
            total_fitness += fitness

        avg_fitness_per_gen.append(total_fitness/ len(population)) #stores average fitness for graph
        
        selected = roulette_selection(rated_population)
        population = crossover(selected)
        population = mutate(population)

    best = [10000, []]
    for frame in population:
        fitness_score = fitness_function(latest_frame, frame, change)
        if best[0] > fitness_score:
            best[0] = fitness_score
            best[1] = frame

    print("best", ["full", best[0]])
    best_fitness.append(["full", best[0]])
    
    return best[1], change, avg_fitness_per_gen

def animate_frames(frames):
    # ============================================================================== #
    # This is code to visualize the frames and has nothing to do with the actual GA. #
    # ============================================================================== #
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    def update(i):
        plot_spider_pose(ax, frames[i])
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval=200)
    plt.show()

def plot_graph(avg_fitness_across_frames):
    # Plot average fitness progression across all frames (log scale)
    plt.figure(figsize=(10,5))
    plt.plot(avg_fitness_across_frames, label="Average Fitness Across All Frames")
    plt.yscale("log")
    plt.xlabel("Generation")
    plt.ylabel("Average Fitness (log scale)")
    plt.title("Average Fitness Progression Across All Generations & Frames")
    plt.legend()
    plt.show()
    
def main(nn=False):
    speed = 200
    amount_frames = 100

    latest_frame = generate_frame()
    total_frames = [latest_frame]

    change = [random.choice([-0.1,0.1]) for _ in range(24)]

    all_avg_fitness_gen = []  # stores avg fitness per generation for each frame

    # Run GA for each frame
    while len(total_frames) < amount_frames:
        print("progress", len(total_frames))
        new_frame, change, avg_fitness_per_gen = geneticA(latest_frame, change, 200, 200)
        total_frames.append(new_frame)
        latest_frame = new_frame

        all_avg_fitness_gen.append(avg_fitness_per_gen)

    num_gen = len(all_avg_fitness_gen[0])
    avg_fitness_frames = []

    for gen in range(num_gen):
        generation_sum = 0  
        
        for frame_avg in all_avg_fitness_gen:
            generation_sum += frame_avg[gen]  
            
        generation_average = generation_sum / len(all_avg_fitness_gen)
    
        avg_fitness_frames.append(generation_average)

    # Save frames to CSV
    filename = 'output_data.csv'
    try:
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(total_frames)
        print(f"✅ Successfully wrote data to {filename}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

    print(best_fitness)

    if nn:
        return total_frames

    animate_frames(total_frames)
    plot_graph(avg_fitness_frames)


main()
