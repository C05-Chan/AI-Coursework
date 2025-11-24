import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2
bestfitness = []
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
    fitness = 0
    for i in range(len(reference)-1):
        fitness += abs(reference[i] - candidate[i]-change[i])

    return fitness


def breeding(parent1, parent2):
    crossover_point = random.randint(1, 23)  # Crossover point between 1 and 23 as the vectors have 24 elements

    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2


def roulette_selection(ranked_population,refe,change): # tournament style selection output 3 chromosones ' add 2 training dummys 1000 and 1 value
    sum=0
    avg = 2
    outpopulation = []
    for i in ranked_population:
        sum+=1/(1+i[0])**4

    roulette_wheel=[]
    prev=0
    for i in ranked_population:
        value=1/(1+(i[0])**4)
        roulette_wheel.append([prev+(value)/sum,i[1]])
        prev+=(value)/sum

    eh=0
    insgesamtneu=0
    insgesamt=0
    for i in range(len(ranked_population)//2):
        randA,randB = random.random(), random.random()
        for a in range(len(roulette_wheel)):
            if roulette_wheel[a][0] > randA:
                for b in roulette_wheel:
                    if b[0] > randB:
                        #print("here",ranked_population[a][0])
                        child1, child2 = breeding(roulette_wheel[a][1], b[1])
                        outpopulation.append(child1)
                        outpopulation.append(child2)
                        insgesamt+=fitness_function(refe,roulette_wheel[a][1],change) + fitness_function(refe,b[1],change)
                        #print(roulette_wheel[a][1][0],b[1][0])
                        eh += 2
                        #insgesamt+=roulette_wheel[a][0]+b[0]
                        insgesamtneu+=fitness_function(refe, child1, change)+ fitness_function(refe, child2, change)

                        break
                break
    #print("here", len(outpopulation), insgesamt/eh, insgesamtneu/eh)
    return outpopulation

def mutate(population):
    for inv in range(len(population)):
        for i in range(len(population[inv])):
            if random.random() < 0.002:
                if i%3 == 0:
                    population[inv][i] = round(random.uniform(-0.38, 0.38), 3)
                elif i%3 == 1:
                    population[inv][i] = round(random.uniform(-2, -0.5), 3)
                else:
                    population[inv][i] = round(random.uniform(-0.5, 0), 3)
    return population


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
    generations = 10000
    boundary = [-0.38, 0.38, -2, -0.5, -0.5, 0]
    for i in range(len(last_change)):
        if i%3 == 0:





        if random.random() < 0.9:
            change.append(i)
        else:
            if i > 0: #changes direction
                a=-1
            else:
                a=1
            change.append((random.random()*(0.1) + 0.1)*a)
    print(change)
    population = generate_population(size)
    while generations>1:
        generations -= 1
        rated_population = []

        for frame in population:

            fitness = fitness_function(latest_frame, frame, change)

            if fitness < 0.7:
                print("generation",["stop",generations])
                bestfitness.append(["stop",fitness,generations])
                return frame, change
            if fitness < 7: rated_population.append([fitness, frame])
        population = roulette_selection(rated_population,latest_frame,change)
        population = mutate(population)
        #print("OMG",len(population))
        while len(population) < size:

            population.append(generate_frame())
    best=[10000,[]]
    for i in population:
        if best[0] > fitness_function(latest_frame,i,change):
            best[0]=fitness_function(latest_frame,i,change)
            best[1]=i
    print("best",["full",best[0]])
    bestfitness.append(["full",best[0]])
    return best[1], change





def main(nn=False):
    latest_frame = generate_frame()
    total_frames = [latest_frame]
    change = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]*3
    while len(total_frames) < 20:
        print("progress",len(total_frames))
        new_frame, change = geneticA(latest_frame, change)
        total_frames.append(new_frame)
        latest_frame = new_frame
    print("total",total_frames)
    #for i in range(len(total_frames)):
       # angles_frame.append(total_frames[i])
    #
    print(bestfitness, )
    if nn:
        return total_frames
    animate_frames(total_frames)
    # animate_frames(population[0])


    
    


main() # Starts the program frame[[1,2,3]]
