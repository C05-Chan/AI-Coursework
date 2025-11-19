import random
import math

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
     
     
def fitness_selection(ranked_population): # tournamen style selection output 3 cromosones ' add 2 training dummys 1000 and 1 value
    total_sum = 0
    seelected = 0
    pre_nums = 0
    Normilized_nums = []
    cumulative_sum = []
    selected_cromosones = []
    for i in range(len(ranked_population)):
        total_sum += ranked_population[i][0]

    for i in range(len(ranked_population)):
        Normilized_nums.append([ranked_population[i][0] / total_sum,ranked_population[i][1]])

    for i in range(len(Normilized_nums)):
        cumulative_sum.append(Normilized_nums[i][0] + pre_nums)
        pre_nums += Normilized_nums[i][0]
    
    for i in range(len(cumulative_sum)):
        selected = random.random()
        for i in range(len(cumulative_sum)):
            if selected < cumulative_sum[i][0]:
                selected_cromosones.append(cumulative_sum[i][0])
                break
    return(selected_cromosones)

def offspring(fit_population):
     fit_offspring = []

     return (fit_offspring)

def mutation(fit_offspring):
     mutated_offspring = []

     return (mutated_offspring)

def new_population(mutated_offspring):
     new_pop = []

     return(new_pop)

def main():
    mutation_rate = 0.01
    population_size = 100
    population = []
    fit_population = []
    i = 0
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

main() # Starts the program 
