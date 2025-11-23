import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2
def generate_frame():
    frame = []  # generates 7200
    for i in range(8):
        frame.append(round(random.uniform(-0.38, 0.38), 3))
        frame.append(round(random.uniform(-2, -0.5), 3))
        frame.append(round(random.uniform(-0.5, 0), 3))
    return frame

def generate_population(n=300):
    population = []
    for x in range(n):
        population.append(generate_frame())
    return population

def fitness_function(reference, candidate, change):
    #max_angles = [0.38, -0.5, -0.5]
    #min_angles = [-0.38, -2, 0]
    fitness = 0
    #print("CANDIDATE", candidate)
    for i in range(len(reference)-1):
        #print("reference",reference[i])
        #print("candidate",candidate[i])
        #print("change",change[i])

        fitness += abs(reference[i] - candidate[i]-change[i])

    return fitness


def breeding(parent1, parent2):
    crossover_point = random.randint(1, 23)  # Crossover point between 1 and 23 as the vectors have 24 elements

    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2


def roulette_selection(ranked_population): # tournament style selection output 3 chromosones ' add 2 training dummys 1000 and 1 value
    sum=0
    avg = 2
    outpopulation = []
    for i in ranked_population:
        sum+=1/(1+i[0])

    roulette_wheel=[]
    prev=0
    for i in ranked_population:
        roulette_wheel.append([prev+(1/(1+i[0]))/sum,i[1]])
        prev+=(1/(1+i[0]))/sum

    eh=0
    rando=[]
    for i in range(len(ranked_population)//2):
        randA,randB = random.random(), random.random()
        for a in range(len(roulette_wheel)):
            if roulette_wheel[a][0] < randA:
                for b in roulette_wheel:
                    if b[0] < randB:
                        print("here",ranked_population[a][0])
                        child1, child2 = breeding(roulette_wheel[a][1], b[1])
                        outpopulation.append(child1)
                        outpopulation.append(child2)
                        eh += 2
                        break
                break
    print("here")

    sum = 0
    for i in ranked_population:
        sum += i[0]
    avg = sum / len(ranked_population)
    haha=0
    for i in range(len(ranked_population)):
        #print(ranked_population[i][0])
        if ranked_population[i][0] < avg*0.85:
            haha +=1

            outpopulation.append(ranked_population[i][1])
    print("das kommt", haha, avg)
    return outpopulation


def animate_frames(frames):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111, projection='3d')

    def update(i):
        plot_spider_pose(ax, frames[i])
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), interval=500)
    plt.show()


def geneticA(latest_frame, last_change, size=100):
    change = []
    generations = 1000
    for i in last_change:
        if random.random() < 0.8:
            change.append(i)
        else:
            if i > 0: #changes direction
                a=-1
            else:
                a=1
            change.append((random.random()*(0.1) + 0.05)*a)

    population = generate_population(size)
    while generations>1:
        generations -= 1
        rated_population = []

        for frame in population:

            fitness = fitness_function(latest_frame, frame, change)

            if fitness < 1: return frame, change
            if fitness < 15: rated_population.append([fitness, frame])
        population = roulette_selection(rated_population)
        while len(population) < size:
            population.append(generate_frame())




def main(nn=False):
    latest_frame = generate_frame()
    total_frames = [latest_frame]
    change = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]*3
    while len(total_frames) < 5:
        new_frame, change = geneticA(latest_frame, change)
        total_frames.append(new_frame)
        latest_frame = new_frame
    print(total_frames)
    #for i in range(len(total_frames)):
       # angles_frame.append(total_frames[i])
    #
    animate_frames(total_frames)
    # animate_frames(population[0])


    
    


main() # Starts the program frame[[1,2,3]]
