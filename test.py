import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2


def generate_angles(population_size):
    gaits = []
    
    for x in range(population_size):
        angles = [] #generates 7200
        for i in range(8):
            angles.append(round(random.uniform(-0.38,0.38),3))
            angles.append(round(random.uniform(-2,-0.5),3))
            angles.append(round(random.uniform(-0.5,0),3))
        gaits.append(angles)

    return(gaits)


def fitness_function(total_angles):
    all_fitness = []
    
    print("total_angles", total_angles)
    
    max_angles = [0.38,-0.5,-0.5] 
    min_angles = [-0.38,-2,0]
    
    prev_angles = None
    
    for frames in total_angles:  
        ### This sections splits the flat list of 24 angles into 8 legs with 3 angles each ###
        legs = []
        for i in range(0, len(frames), 3):
            legs.append(frames[i:i+3])
            
        print("legs", legs)

        fitness_score = 7.2  # max fitness
        fitness_pos = 0
        fitness_transition = 0
        
        for individual_leg in legs:
            coxa, femur, tibia = individual_leg

            ## Checks the angles of each leg to see if they are in a legal position or not ##
            if min_angles[0] < coxa < max_angles[0]:
                fitness_pos += 0.2
            if min_angles[1] < femur < max_angles[1]:
                fitness_pos += 0.2
            if  min_angles[2] < tibia < max_angles[2]:
                fitness_pos += 0.2
                

        if prev_angles == None:
            prev_angles = legs
        else:
            for i in range(8):
                current_coxa, current_femur, current_tibia = legs[i]
                prev_coxa, prev_femur, prev_tibia = prev_angles[i]
                
            # Checks how much the leg has moved from the previous frame to the current frame
                if abs(current_coxa - prev_coxa) < 0.2:
                    fitness_transition += 0.1
                if abs(current_femur - prev_femur) < 0.2:
                    fitness_transition += 0.1
                if abs(current_tibia - prev_tibia) < 0.2:
                    fitness_transition += 0.1
            
            
        # print("fitness pos", fitness_pos)
        # print("fitness transition", fitness_transition)
                
        fitness_score -= (fitness_pos + fitness_transition)
        all_fitness.append(fitness_score)
        
    print(all_fitness)
    
    return all_fitness


def tournament_selection(fitness_scores, total_angles):
    selected_parents = []

    total_parents = len(total_angles) // 2

    if total_parents % 2 != 0: #ensure total parents is always even
        total_parents += 1

    while len(selected_parents) < total_parents:
        tournament_size = random.randint(2, len(total_angles)) ######################## THIS SHOULDNT BE RANDOM EVERY TIME ##########################
        competitors = random.sample(range(len(total_angles)), tournament_size)

        print("Competitors:", competitors)

        competitors.sort(key=lambda x: fitness_scores[x])
        best = competitors[0]

        if best not in selected_parents:
            selected_parents.append(best)
        
        print("best competitor:", best)
    
    print("Selected indices:", selected_parents)


    return selected_parents

def offspring_generation(selected_indices, total_angles):
    offspring = []
    
    for i in range(0, len(selected_indices), 2):
        parent1 = total_angles[selected_indices[i]]
        parent2 = total_angles[selected_indices[i+1]]
        
        child1, child2 = breeding(parent1, parent2)
        
        offspring.append(child1)
        offspring.append(child2)
    

    print("Offspring:", offspring)
    return offspring

def breeding(parent1, parent2):
    crossover_point = random.randint(1, 23)  # Crossover point between 1 and 23 as the vectors have 24 elements

    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    print("Parent 1:", parent1)
    print("Parent 2:", parent2)

    print("Crossover point:", crossover_point)
    print("Child 1:", child1)
    print("Child 2:", child2)
    return child1, child2


def mutation(offspring):
    mutation_rate = 0.1 # 10% mutation rate

    for individual in offspring:
        if random.random() < mutation_rate:
            
            mutated_index = random.randint(0, len(individual)-1)

            joint = mutated_index % 3

            if joint == 0:#coxa
                individual[mutated_index] = round(random.uniform(-0.38, 0.38), 3)
            elif joint == 1:# femur
                individual[mutated_index] = round(random.uniform(-2, -0.5), 3)
            else:# tibia
                individual[mutated_index] = round(random.uniform(-0.5, 0), 3)

    print("Mutated Offspring:", offspring)
    print(len(offspring))

    return offspring


def animate_frames(frames):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Set fixed axis limits so animation does not jitter
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(0, 10)

    def update(i):
        ax.cla()  # clear old frame

        # Keep limits every frame
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_zlim(0, 10)

        plot_spider_pose(ax, frames[i])
        ax.set_title(f"Frame {i}")

        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval=200)
    plt.show()


def main():
    population_size = 10
    best_frame = []
    population = []
    
    animation = []

    total_angles = generate_angles(population_size)
    fitness_scores = fitness_function(total_angles)
    selected_parents = tournament_selection(fitness_scores, total_angles)
    offspring = offspring_generation(selected_parents, total_angles)
    mutated_offspring = mutation(offspring)


    # total_angles = list of 300 frames
# fitness_scores = corresponding list of fitness values


    population.append(total_angles)

    angles_frame = []

    animate_frames(total_angles)

    

    # animate_frames(population[0])
    
    


main()
