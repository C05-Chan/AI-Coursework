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
    
    # print("total_angles", total_angles)
    
    max_angles = [0.38,-0.5,-0.5] 
    min_angles = [-0.38,-2,0]
    
    prev_angles = None
    
    for frames in total_angles:  
        legs = []
        for i in range(0, len(frames), 3):
            legs.append(frames[i:i+3])
            
        # print("legs", legs)

        fitness_score = 5.04  # max fitness is 8 legs * 3 joints * 0.2 = 4.8
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

def tournament_selection(fitness_scores, tournament_size):
    index_results = []
    ranked_population = []
    selected_population = []
    exclude_indices = []
    
    while len(selected_population) < tournament_size:
        selection_size = tournament_size // 4
        
        while len(index_results) != selection_size:
            selected_index = random.randint(0, tournament_size-1)
            if (selected_index not in index_results) and (selected_index not in exclude_indices):
                index_results.append(selected_index)

        index_results.sort()
        for i in index_results:
            ranked_population.append((fitness_scores[i], i))
        
        ranked_population.sort()
        selected_population.append(ranked_population[:2])
        exclude_indices.append(ranked_population[0][1])
        exclude_indices.append(ranked_population[1][1])
        
        
            
    print("ranked population", ranked_population)
    print("selected population", selected_population)
    return selected_population


def animate_frames(frames):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111, projection='3d')

    def update(i):
        plot_spider_pose(ax, frames[i])
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval=500)
    plt.show()

def main():
    population_size = 10
    frame = []
    population = []
    
    animation = []

    total_angles = generate_angles(population_size)
    fitness_scores = fitness_function(total_angles)
    tournament_selection(fitness_scores, population_size)
    

    population.append(total_angles)

    angles_frame = []

    # animate_frames(angles_frame)
    

    # animate_frames(population[0])
    
    


main()
