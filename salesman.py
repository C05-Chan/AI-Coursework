import random
import math

import pygame
import sys  

pygame.init()
#pygame.font.init()

city_coordinates = [
    (60, 200),  # City 0  - (X,Y)
    (180, 200), # City 1
    (80, 180),  # City 2
    (140, 180), # City 3
    (20, 160),  # City 4
    (100, 160), # City 5
    (200, 160), # City 6
    (140, 140), # City 7
    (40, 120),  # City 8
    (100, 120)  # City 9
]

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Basic Pygame Model")

font = pygame.font.Font(None,34)


clock = pygame.time.Clock()
FPS = 60  

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#
# -------------------------------------------------------------------GA -- 
#

start_value = 0
group_size = 10
population = []
popFitness = []
mutationRate = 0.01
generations = 1000

#randomise the city coordinates

city_coordinates = [
    (60, 200),  # City 0  - (X,Y)
    (180, 200), # City 1
    (80, 180),  # City 2
    (140, 180), # City 3
    (20, 160),  # City 4
    (100, 160), # City 5
    (200, 160), # City 6
    (140, 140), # City 7
    (40, 120),  # City 8
    (100, 120)  # City 9
]


def intToString(num: int ):
    match num:
        case 0:
            return 'A'
        case 1:
            return 'B'
        case 2:
            return 'C'
        case 3:
            return 'D'
        case 4:
            return 'E'
        case 5:
            return 'F'
        case 6:
            return 'G'
        case 7:
            return 'H'
        case 8:
            return 'I'
        case 9:
            return 'J'
        case _:
            return '-'
        
def convertListToStr(valueList: list):
    hold = []
    for item in valueList:
        convertTupleToStr = intToString(city_coordinates.index(item)) 
        hold.append(convertTupleToStr)
    return hold

def addHeadAndTail(valueList: list):
    valueList = [city_coordinates[start_value]] + valueList + [city_coordinates[start_value]]
    return valueList

def takeawayHeadAndTail(valueList: list):
    valueList = valueList[1:-1] 
    return valueList

def calculateDistance(pointA: tuple, pointB:tuple):
    x1,y1 = pointA
    x2,y2 = pointB

    delta_x = x2 - x1
    delta_y = y2 - y1

    distanceSquared = delta_x**2 + delta_y**2

    return math.sqrt(distanceSquared)

def listShiftFromIndex(startPoint: int,shiftList: list):
    orderedParent = []
    for i in range(len(shiftList)):
        #print(shiftList[count])
        if startPoint == len(shiftList):
            startPoint = 0
        #print(intToString(startPoint))
        orderedParent.append(shiftList[startPoint])
        startPoint = startPoint + 1
    
    return orderedParent

def mergeListFromIndex(startPoint: int,offspring: list,mergeList: list):
    for i in range(len(mergeList)):
        if startPoint == len(offspring):
            startPoint = 0
        offspring[startPoint] = mergeList[i]
        startPoint = startPoint + 1
    return offspring

def chromosomes():

    startPoint = city_coordinates[0]

    itemstoshuffle = [item for item in city_coordinates if item != startPoint]

    
    for _ in range(group_size):
        random.shuffle(itemstoshuffle)
        population.append([startPoint] + itemstoshuffle + [startPoint])


def fitness():
    weight = []
    for value in population:
        holder = []
        previousIndex = 0
        for currentIndex in range(1,len(value)):
            distance = round(calculateDistance(value[previousIndex],value[currentIndex]),2)
            holder.append([intToString(city_coordinates.index(value[previousIndex])) , distance, intToString(city_coordinates.index(value[currentIndex]))])
            previousIndex = currentIndex
        weight.append(holder)
    fitness = [sum([value[1] for value in item ]) for item in weight]
    return fitness


def rouletteTournement(popFitness):
    parents = []
    max_fitness = max(popFitness)
    inverted_score = [(max_fitness - f) + 1 for f in popFitness]
    fitTotal = sum(inverted_score)
    normalisedValue = [item/fitTotal for item in inverted_score] # makes all of the values fit between 1 and 0
    cumulative = []
    index = 0

    for item in normalisedValue:
        index += item
        cumulative.append(index)
    for _ in range(len(population)):
        pointer = random.random()
        for j, val in enumerate(cumulative): 
            if pointer <= val:
                parents.append(population[j])
                break
    return parents

def crossover(parents):
    children = []
    # doing it with a set range for now
    for i in range(0,len(parents)-1,2):
        #startPoint, endPoint = (3,7) # randomise this value

        #startPoint,endPoint = random.randint(0,len())

        firstParent,secondParent = takeawayHeadAndTail(parents[i]),takeawayHeadAndTail(parents[i+1])
        startPoint = random.randint(0,len(firstParent)-1)
        endPoint = random.randint(startPoint+1,len(firstParent))
        offspring1,offspring2 = [None] *len(firstParent), [None] *len(firstParent)

        segment1, segment2 = firstParent[startPoint:endPoint],secondParent[startPoint:endPoint]
        # offspring1 = to first parent section
        # offsprint2 = to second parent section

        offspring1[startPoint:endPoint], offspring2[startPoint:endPoint] = segment2, segment1

        # what im doing is making an offspring from parent 1 and cutting it with segment from parent 2
        # This is for the first offspring
        # getting the Ordered List of remaining values

        orderedList1 = listShiftFromIndex(endPoint,firstParent)
        orderedListSub1 = [value for value in orderedList1 if value not in segment2] # ori could cut of the last 4 integers
        #merges them
        mergeListFromIndex(endPoint,offspring1,orderedListSub1)

        # for Offspring 2
        orderedList2 = listShiftFromIndex(endPoint,secondParent)
        orderedListSub2 = [value for value in orderedList2 if value not in segment1] # ori could cut of the last 4 integers
        mergeListFromIndex(endPoint,offspring2,orderedListSub2)
        offspring1 = addHeadAndTail(offspring1)
        offspring2 = addHeadAndTail(offspring2)

        children.append(offspring1); children.append(offspring2)

        #children.append()
        #print(f"{startPoint},{endPoint}")
        #print(f"Parent 1:{convertListToStr(firstParent)}")
        #print(f"Parent 2 :{convertListToStr(secondParent)}")
        
        #print(f"Offspring 1:{convertListToStr(offspring1)} (Parent1 merging with parent2's segment)")
        #print(f"Offspring 2:{convertListToStr(offspring2)} (Parent2 merging with parent1's segment)")
        #print( )

    return children

def mutation(parentOffspring: list):
    mutated_offspring = []
    
    for x in parentOffspring:
        mutated_offspring.append(takeawayHeadAndTail(x))

    for i, offspring in enumerate(mutated_offspring):
        for j in range(len(offspring)):
            if random.random() < mutationRate:
                swapValue = random.choice([x for x in range(0,len(offspring)) if x != j])
                #mutated_offspring[i][j],mutated_offspring[i][swapValue] = mutated_offspring[i][swapValue],mutated_offspring[i][j]

                offspring[j],offspring[swapValue] = offspring[swapValue],offspring[j]
                print("i mutated")
    
    for value in range(len(mutated_offspring)):
        mutated_offspring[value] = addHeadAndTail(mutated_offspring[value])

    return mutated_offspring

def runGA():
    global population
    global popFitness

    population = []
    popFitness = []

    chromosomes()

    for generation in range(generations):

        popFitness = fitness()
        roulette = rouletteTournement(popFitness)
        crossoverChildren = crossover(roulette)
        population = mutation(crossoverChildren)

    best_fitness = max(popFitness)
    print(f"generation :{generation} - Best Fitness {best_fitness} - population size {len(population)}")

    best_fitness = min(popFitness)
    best_index = popFitness.index(best_fitness)
    print(convertListToStr(population[best_index]))

def drawCoordinates():
    for i, value in enumerate(city_coordinates):
        if i == 0:
            pygame.draw.circle(screen,GREEN,value,5)
        else:
            pygame.draw.circle(screen,BLACK,value,5)

def drawBestPath():
    #for i in best_fitness:
    holder = population[popFitness.index(min(popFitness))][:-1]
    #print(convertListToStr(holder))
    pygame.draw.lines(screen,RED,True,holder,1)

#print(population[best_index])

runGA()

buttonRect = pygame.Rect(700,100,75,50)

# 5. Main Game Loop
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if buttonRect.collidepoint(event.pos):
                print("button was clicked")
                runGA()

    screen.fill(WHITE)

    mouse_pos = pygame.mouse.get_pos()

    if buttonRect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, GREEN,buttonRect)
    else:
        pygame.draw.rect(screen,BLACK,buttonRect,2)

    drawCoordinates()
    drawBestPath()
    #pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, 100, 100))

    text_surface = font.render("Reset",True,BLACK)

    text_rect = text_surface.get_rect(center=buttonRect.center)

    screen.blit(text_surface,text_rect)
    # --- 5.4. Update the Display ---
    # Flips the display buffer to show the new frame

    pygame.display.flip()

    # --- 5.5. Cap the Framerate ---
    # Tell the clock to wait to maintain the target FPS
    clock.tick(FPS)

# 6. Quit
# Once the loop is broken, uninitialize Pygame and exit
pygame.quit()
sys.exit()