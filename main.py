import random

def check_if_legs_cross(angles):
     is_bad = False


     return (is_bad)

def generate_angles(): # generates 1 animations
    frames=300
    animation=[]
    for x in range(frames):
            angles = []
            is_bad=True
            while is_bad:
                for _ in range(24):
                    angles.append(round(random.uniform(0,2),2)) #only in range that is legal
                is_bad = check_if_legs_cross(angles)  #    
                animation.append(angles)
    return(animation)

def fitness_body_cross(population): # this checks if the angles are legal (illegal angles means the legs are intersecting the body, etc.)
     body_cords = [0,0,0]

     return (fit_angles)
     
     
def fitness_selection(population):
    angles = fitness_angles(population)
    
    return (fit_population)

def offspring(fit_population):
     fit_offspring = []

     return (fit_offspring)

def new_population(mutated_offspring):
     new_pop = []

     return(new_pop)

def mutation(fit_offspring):
     mutated_offspring = []

     return (mutated_offspring)

def main():
    mutation_rate = 0.01
    population_size = 100
    population = []

    for i in range(population_size):
        population.append(generate_angles())
    
    fit_population = fitness_selection(population)
    fit_offspring = offspring(fit_population)
    mutated_offspring = mutation(fit_offspring, mutation_rate)
    population = new_population(mutated_offspring)

main() # Starts the program 
