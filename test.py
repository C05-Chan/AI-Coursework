import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose

chromosome = 24  # 8 legs * 3 joints

# -----------------------------
#  Generate initial population
# -----------------------------
def generate_gait(population_size, frames):
    ### This generates a population of random gaits (animations), in each gait there are 300 frames, each frame has 24 joint angles (8 legs * 3 joints)
    population = []
    for _ in range(population_size):
        gait = []
        for _ in range(frames):
            frame = []
            for leg in range(8):
                frame.append(round(random.uniform(-0.38, 0.38), 3)) #Coxa
                frame.append(round(random.uniform(-2, -0.5), 3)) #Femur
                frame.append(round(random.uniform(-0.5, 0), 3)) # Tibia
            gait.append(frame)
        population.append(gait)
    return population

# -----------------------------
# Fitness function
# -----------------------------
def fitness_function(population):
    # This function evaluates each gait in the population and assigns a fitness score based on several criteria
    # Higher fitness is better
    
    # Criteria:
    # 1. If the joint angles are within limits
    # 2. The smoothness of transitions between frames
    # 3. Symmetry between left and right legs
    # 4. If the leg contacts the ground (tibia near zero)
    
    all_fitness = []
    max_symmetry_reward = 0.5


    # Define maximum and minimum joint angles for  the Coxa, Femur, Tibia
    max_angles = [0.38, -0.5, -0.5] 
    min_angles = [-0.38, -2, 0]

    for gait in population:  # gait is a list of frames
        fitness = 0
        prev_frame = None

        for frame in gait:  # Split the 24 angles into 8 legs with 3 angles each
            all_legs = []
            for leg_index in range(8):
                start_idx = leg_index * 3 #this gets the Coxa angles, so every 3 in the array
                end_idx = start_idx + 3 #this gets the Tibia angles
                leg_angles = frame[start_idx:end_idx]
                all_legs.append(leg_angles)

            # Check joint limits
            for leg in all_legs:
                coxa = leg[0]
                femur = leg[1]
                tibia = leg[2]

                if coxa < min_angles[0] or coxa > max_angles[0]:
                    fitness -= 10
                if femur < min_angles[1] or femur > max_angles[1]:
                    fitness -= 10
                if tibia < min_angles[2] or tibia > max_angles[2]:
                    fitness -= 10

            # Smooth transitions between frames
            if prev_frame is not None:
                for leg_index in range(8):
                    for joint_index in range(3):
                        difference = abs(all_legs[leg_index][joint_index] - prev_frame[leg_index][joint_index])
                        if difference < 0.2:
                            fitness += 0.1
            prev_frame = all_legs

            # Symmetry between left and right legs
            left_indices = [0, 1, 2, 3]
            right_indices = [4, 5, 6, 7]
            for symmetry_index in range(4): #4 it is the amount of legs/2
                left_leg = all_legs[left_indices[symmetry_index]]
                right_leg = all_legs[right_indices[symmetry_index]]

                diff_sum = 0
                for joint_idx in range(3):
                    diff_sum += abs(left_leg[joint_idx] - right_leg[joint_idx])

                symmetry_score = max_symmetry_reward - diff_sum

                if symmetry_score < 0: #make sure its not negative
                    symmetry_score = 0

                fitness += symmetry_score

            # Ground contact (tibia near zero)
            for leg in all_legs:
                tibia = leg[2]
                if tibia > 0:  #  the leg is floating
                    fitness -= 20

        all_fitness.append(fitness)

    return all_fitness

def tournament_selection(fitness_scores, population):
    
    tournament_size = 3
    win_prob=0.75
    selected_parents = []
    total_parents = len(population) // 2

    # Ensure total_parents is even
    if total_parents % 2 != 0:
        total_parents += 1

    while len(selected_parents) < total_parents:
        # Randomly pick competitors
        competitors = random.sample(range(len(population)), tournament_size)
        # Sort competitors by fitness (highest first)
        competitors.sort(key=lambda x: fitness_scores[x], reverse=True)

        # Probabilistic winner
        r = random.random()
        if r < win_prob:
            winner = competitors[0]  # strongest wins
        else:
            # pick a weaker competitor 
            winner = random.choice(competitors[1:])
        if winner not in selected_parents:
            selected_parents.append(winner)     
    return selected_parents

def breeding(parent1, parent2, frames):
    crossover_frame = random.randint(1, frames - 1)
    child1 = parent1[:crossover_frame] + parent2[crossover_frame:]
    child2 = parent2[:crossover_frame] + parent1[crossover_frame:]
    return child1, child2

def offspring_generation(selected_parents, population, frames):
    offspring = []
    for i in range(0, len(selected_parents), 2):
        p1 = population[selected_parents[i]]
        p2 = population[selected_parents[i+1]]
        child1, child2 = breeding(p1, p2, frames)
        offspring.extend([child1, child2])
    return offspring


def mutation(offspring, mutation_rate=0.1):
    for gait in offspring:
        for frame in gait:
            if random.random() < mutation_rate:
                idx = random.randint(0, chromosome - 1)
                # Determine joint type
                if idx % 3 == 0:
                    frame[idx] = round(random.uniform(-0.38, 0.38), 3)
                elif idx % 3 == 1:
                    frame[idx] = round(random.uniform(-2, -0.5), 3)
                else:
                    frame[idx] = round(random.uniform(-0.5, 0), 3)
    return offspring


def new_population(selected_parents, offspring, population):
    new_pop = [population[i] for i in selected_parents]
    new_pop.extend(offspring)
    return new_pop[:len(population)]

def animate_gait(frames):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)
    ax.set_zlim(0,10)

    def update(i):
        ax.cla()
        ax.set_xlim(-10,10)
        ax.set_ylim(-10,10)
        ax.set_zlim(0,10)
        plot_spider_pose(ax, frames[i])
        ax.set_title(f"Frame {i}")
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval= 300)
    plt.show()


def main():
    population_size = 10
    generations = 50
    frames = 300

    population = generate_gait(population_size, frames)

    for gen in range(generations):
        fitness_scores = fitness_function(population)
        selected_parents = tournament_selection(fitness_scores, population)
        offspring = offspring_generation(selected_parents, population, frames)
        mutated_offspring = mutation(offspring)
        population = new_population(selected_parents, mutated_offspring, population)
        
        #### This is for monitoring progress ####
        best_score = max(fitness_scores)
        print(f"Generation {gen+1}: Best fitness = {best_score:.2f}")

    # Animate the best gait
    fitness_scores = fitness_function(population)
    best_gait = population[fitness_scores.index(max(fitness_scores))]
    animate_gait(best_gait)

main()
