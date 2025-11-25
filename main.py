import random
import math
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2
bestfitness = []

'''
Generates a single RANDOM frame inside of our set boundaries
'''
def generate_frame():
    frame = []
    for i in range(8):
        frame.append(round(random.uniform(-0.38, 0.38), 3))
        frame.append(round(random.uniform(-2, -0.5), 3))
        frame.append(round(random.uniform(-0.5, 0), 3))
    return frame


'''
Evaluates how close a proposed next frame (candidate) is to the last frame (reference) + a change (change)
Change makes sure to favor frames that are different from the last frame
'''
def fitness_function(reference, candidate, change):
    fitness = 0
    for i in range(len(reference)-1):
        fitness += abs(reference[i] - candidate[i]-change[i])

    return fitness**2

'''
This function
crosses two parent frames at a random crossover point to make two child frames.
The two children have nothing in common:
E.g.: [p1, p2, p3, p4, p5] + [q1, q2, q3, q4, q5] => [p1,p2, q3, q4, q5] + [q1, q2, p3, p4, p5]
'''
def crossover(selected):
    outpopulation = [] #output population, get it?
    for i in range(0, len(selected)//2, 2):
        parent1 = selected[i]
        parent2 = selected[i+1]

        crossover_point = random.randint(1, 23)  # Crossover point between 1 and 23 as the vectors have 24 elements

        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

        outpopulation.append(child1)
        outpopulation.append(child2)

    return outpopulation


'''
This selects random individuals of the current populations.
While a higher fitness equals to a higher chance to be selected, the process is still random, as all individuals have a chance.
'''
def roulette_selection(ranked_population):
    sum=0
    for i in ranked_population:
        sum+=1/(1+i[0])**4

    roulette_wheel=[]
    prev=0
    for i in ranked_population:
        value=1/(1+(i[0])**4)
        roulette_wheel.append([prev+(value)/sum,i[1]])
        prev+=(value)/sum

    selected = []
    for i in range(len(ranked_population)):
        rand = random.random()
        for a in range(len(roulette_wheel)):
            if roulette_wheel[a][0] > rand:
                selected.append(roulette_wheel[a][1])
                break

    return selected

'''
This goes through the entire population and their angles and 
mutates their values to a random value inside the boundaries with a chance of 0.2%
'''
def mutate(population):
    for inv in range(len(population)):
        for i in range(len(population[inv])):
            if random.random() < 0.002:
                if i%3 == 0: #This makes sure that the new values are inside the correct boundaries
                    population[inv][i] = round(random.uniform(-0.38, 0.38), 3)
                elif i%3 == 1:
                    population[inv][i] = round(random.uniform(-2, -0.5), 3)
                else:
                    population[inv][i] = round(random.uniform(-0.5, 0), 3)
    return population



'''
This is the main function of the genetic Algorithm
'''
def geneticA(latest_frame, last_change, size=1000):
    change = []
    generations = 1000
    boundary = [-0.38, 0.38, -2, -0.5, -0.5, 0]

    '''
    Determines if the direction of change should stay the same.
    '''
    for i in range(len(last_change)):
        bIndex = i%3
        p=0.025
        ranges = abs((boundary[bIndex * 2] - boundary[bIndex * 2 + 1])) / 2

        if random.random() > p and boundary[bIndex*2]<latest_frame[i]<boundary[bIndex*2 + 1]:
            change.append(last_change[i])
        else:
            if last_change[i] > 0:  # changes direction
                a = -1
            else:
                a = 1
            change.append(random.random() * 0.1 * a)
    '''
        ***Initialization***
    This produces a initial population using "generate_frame()" of 
    individuals with random angles (inside of the boundaries)
    '''
    population = []
    for x in range(size):
        population.append(generate_frame())


    while generations>1:
        generations -= 1

        '''
            ***Selection***

        '''
        rated_population = []
        for frame in population:

            fitness = fitness_function(latest_frame, frame, change)
            rated_population.append([fitness, frame])

        selected = roulette_selection(rated_population)

        '''
            ***Reproduction***
        
        '''
        population = crossover(selected)
        population = mutate(population)
    '''
        ***best one***
        
    '''
    best=[10000,[]]
    for i in population:
        if best[0] > fitness_function(latest_frame,i,change):
            best[0]=fitness_function(latest_frame,i,change)
            best[1]=i
    print("best",["full",best[0]])
    bestfitness.append(["full",best[0]])
    return best[1], change


'''
This is code to visualize the frames and has nothing to do with the actual GA.
'''
def animate_frames(frames):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111, projection='3d')

    def update(i):
        plot_spider_pose(ax, frames[i])
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval=200)
    plt.show()

def main(nn=False):
    latest_frame = generate_frame()
    total_frames = [latest_frame]
    change = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]*3
    while len(total_frames) < 300:
        print("progress",len(total_frames))
        new_frame, change = geneticA(latest_frame, change)
        total_frames.append(new_frame)
        latest_frame = new_frame
    print("total",total_frames)

    filename = 'output_data.csv'

    # 3. Write the data to the CSV file
    try:
        # Use 'w' for write mode. 'newline=""' is important
        # for correctly handling line endings, especially on Windows.
        with open(filename, 'w', newline='') as csvfile:
            # Create a csv.writer object
            csv_writer = csv.writer(csvfile)

            # Write all rows at once
            csv_writer.writerows(total_frames)

        print(f"✅ Successfully wrote data to {filename}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")


    print(bestfitness, )
    if nn:
        return total_frames
    animate_frames(total_frames)


    


main() # Starts the program frame[[1,2,3]]
