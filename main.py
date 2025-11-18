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
     
     
def fitness_selection(ranked_population): # tournamen style selection output 3 cromosones
    current_round = []
    next_round = []
    finish = False

    for i in range(len(ranked_population)):
        current_round.append(ranked_population[i])

    while finish == False:
        print("Participents: ",next_round)
        next_round = []
        for i in range((round(len(current_round)/2))):
            contendor_one = random.randint(0,len(current_round)-1)
            contendor_two = random.randint(0,len(current_round)-1)
            if contendor_one == contendor_two:
                contendor_one = random.randint(0,len(current_round)-1)
                contendor_two = random.randint(0,len(current_round)-1)
            elif current_round[contendor_one] <= current_round[contendor_two]:
                print("Contestent 1 win:", current_round[contendor_one][0],"<", current_round[contendor_two][0])
                next_round.append(current_round[contendor_one])
                del current_round[contendor_one]
            else:
                print("Contestent 2 win:", current_round[contendor_two][0],"<", current_round[contendor_one][0])
                next_round.append(current_round[contendor_two])
                del current_round[contendor_two]
            if len(current_round) == 3:
                finish = True
                break
            
        if finish == False:
            current_round = next_round
        print("---round---")
        
    return(current_round)

# def offspring(fit_population):
#      fit_offspring = []

#      return (fit_offspring)

# def mutation(fit_offspring):
#      mutated_offspring = []

#      return (mutated_offspring)

# def new_population(mutated_offspring):
#      new_pop = []

#      return(new_pop)

def main():
    mutation_rate = 0.01
    population_size = 5
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
    output_fit = []
    for i in range(len(output)):
        output_fit.append(output[i][0])
    print("output fitness:", output_fit)
    print("output raw: ", output)

    # fit_population = fitness_selection(population)
    # fit_offspring = offspring(fit_population)
    # mutated_offspring = mutation(fit_offspring, mutation_rate)
    # population = new_population(mutated_offspring)

main() # Starts the program 
