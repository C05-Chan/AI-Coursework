Puitato
cry.__.stal
😭 i am fucking stress drawing

gurrkee — 15:13
i will load this while during my complex meeting
gurrkee — 15:13
same
and i am doing 300 frames
at frame 49 rn
been runing for a couple minutes
Puitato — 15:14
okay
i cahnged it
to 100 generations
Puitato — 15:16
but how do yk
if u cant even see the outcome?
gurrkee — 15:17
i see the fitness of the final frames
Puitato — 15:17
?
gurrkee — 15:17
Image
progress ist how many frames
Puitato — 15:37
right
@gurrkee i see why u have the //2
cuz for ur rouleet selection, u were selecting 1000 individuals out of 1000 individuals 
so now i made it so u only select 150 frames out of 300 frames
then they do cross over
so the final population will still be 300 now
gurrkee — 15:41
Are you sure?
matt. — 15:41
that doesnt make sense to me
gurrkee — 15:41
the code is iterating 150 times (with //2), but skips every second one
matt. — 15:41
what does ur roullette output
gurrkee — 15:42
300 parents
matt. — 15:43
idk just read lecture notes and see what a selection function is meant to output
gurrkee — 15:45
maybe we should select 2 parents per child and not 2 parents per 2 childs
Image
would take double the time tho
Puitato — 15:45
the cross over
creates two child
gurrkee — 15:45
yes
matt. — 15:45
Image
gurrkee — 15:46
ok so if population is 300, we need to select 600 parents
and crossover does one children
will change that and see what happens
matt. — 15:47
crossover can produce 2 children
that is allowed
Image
gurrkee — 15:47
and this allowes to create offspring while doing roulette lol
as I had it yesterday before i was told to change
gurrkee — 15:48
okay good
nearly got my animation rdy
takes 8s per frame
Puitato — 15:49
wait
Puitato — 15:49
then thats too many no?
we want 300
not 750
gurrkee — 15:50
?? how did you come up with 750??
Puitato — 15:52
hold on
maybe ur code is right
and i am dumb
lemme check
okay
i was half right and half wrong
ur roulette is fine 
but crossover was wrong 👍
gurrkee — 15:55
the //2 part?
Puitato — 15:55
yeah we didnt need //2
at all baso
look
when u get here its easier to explain
😭
gurrkee — 15:56
nono i get it
just making sure thats all that was wrong
look at whatsapp
i generated a slow mow spider
lol
Puitato — 15:57
what does it look so wrong? 
gurrkee — 15:58
@matt. this is rather predictable
-0.274,-0.712,-0.087,-0.281,-1.875,-0.163,0.076,-1.117,-0.199,-0.306,-1.862,-0.331,-0.297,-1.258,-0.399,-0.267,-1.427,-0.448,-0.032,-1.856,-0.218,0.146,-1.769,-0.446
-0.339,-0.849,-0.196,-0.37,-1.972,-0.274,-0.021,-1.168,-0.308,-0.329,-1.965,-0.48,-0.37,-1.344,-0.46,-0.362,-1.54,-0.493,-0.157,-1.981,-0.301,0.033,-1.87,-0.083
-0.369,-0.957,-0.314,-0.364,-1.996,-0.377,-0.126,-1.252,-0.41,-0.351,-1.969,-0.492,-0.373,-1.465,-0.498,-0.375,-1.474,-0.496,-0.236,-1.905,-0.401,-0.065,-1.949,-0.431
-0.374,-1.037,-0.409,-0.37,-1.984,-0.497,-0.228,-1.349,-0.497,-0.371,-1.993,-0.493,-0.376,-1.58,-0.486,-0.379,-1.413,-0.495,-0.343,-1.83,-0.495,-0.174,-1.997,-0.471
-0.368,-1.144,-0.495,-0.367,-1.997,-0.498,-0.328,-1.463,-0.498,-0.365,-1.996,-0.493,-0.366,-1.679,-0.499,-0.377,-1.317,-0.493,-0.376,-1.746,-0.496,-0.278,-1.991,-0.134
-0.371,-1.255,-0.499,-0.371,-1.98,-0.489,-0.377,-1.557,-0.495,-0.377,-1.96,-0.5,-0.378,-1.781,-0.5,-0.373,-1.237,-0.496,-0.37,-1.666,-0.497,-0.369,-1.98,-0.298
Expand
output_data.csv
49 KB
gurrkee — 15:58
fitness too hight and change to tight
Puitato — 15:58
so what should we do
gurrkee — 15:59
i will get food and come in now
Puitato — 16:00
i will push to ur branch then
import random
import math
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2
Expand
message.txt
9 KB
matt. — 16:14
@gurrkee can u run ur code like 4- 5 times and send a massive csv
like 1200 lines
gurrkee — 16:14
Uhh ig yes
But this recent one took like 30-40mins
matt. — 16:15
30m for one animation?????
Puitato — 16:15
change
the population 1000 - > 500 
gurrkee — 16:16
Yea
matt. — 16:16
how many generations
gurrkee — 16:16
1000
Did 1k for Generation and Population 300 frames
Wont do that again
Puitato — 16:19
.
@gurrkee where are u 😭
Puitato — 16:28
0.288,-0.99,-0.03,0.068,-0.566,-0.343,0.106,-1.69,-0.347,-0.149,-1.391,-0.281,0.364,-1.347,-0.441,0.232,-0.835,-0.057,-0.062,-1.051,-0.225,0.082,-1.527,-0.429
0.361,-1.091,-0.118,0.02,-0.668,-0.458,0.001,-1.783,-0.419,-0.264,-1.597,-0.381,0.277,-1.44,-0.497,0.159,-0.993,-0.118,-0.161,-1.182,-0.333,-0.041,-1.609,-0.498
0.309,-1.16,-0.223,-0.07,-0.787,-0.41,-0.097,-1.854,-0.434,-0.345,-1.729,-0.492,0.166,-1.553,-0.487,0.012,-1.091,-0.21,-0.326,-1.267,-0.419,-0.112,-1.743,-0.498
0.356,-1.241,-0.333,-0.161,-0.937,-0.395,-0.13,-1.97,-0.448,-0.375,-1.815,-0.472,0.091,-1.68,-0.452,-0.133,-1.262,-0.282,-0.363,-1.403,-0.468,-0.206,-1.832,-0.5
0.377,-1.313,-0.446,-0.296,-0.986,-0.361,-0.243,-1.962,-0.439,-0.376,-1.929,-0.494,-0.017,-1.752,-0.486,-0.221,-1.305,-0.391,-0.368,-1.551,-0.489,-0.126,-1.933,-0.486
0.375,-1.347,-0.482,-0.32,-1.123,-0.362,-0.361,-1.861,-0.491,-0.355,-1.965,-0.467,-0.107,-1.851,-0.463,-0.361,-1.442,-0.318,-0.338,-1.659,-0.497,-0.065,-1.964,-0.469
Expand
message.txt
49 KB
-0.209,-0.815,-0.226,0.286,-1.469,-0.445,0.344,-0.752,-0.335,0.329,-1.274,-0.055,-0.3,-1.493,-0.443,-0.152,-1.038,-0.265,-0.303,-0.963,-0.26,0.294,-1.973,-0.49
-0.354,-0.912,-0.329,0.212,-1.532,-0.44,0.269,-0.888,-0.409,0.243,-1.416,-0.156,-0.374,-1.586,-0.477,-0.318,-1.113,-0.355,-0.326,-1.072,-0.323,0.191,-1.957,-0.478
-0.373,-0.967,-0.437,0.105,-1.675,-0.444,0.14,-1.006,-0.391,0.143,-1.475,-0.268,-0.335,-1.687,-0.469,-0.349,-1.216,-0.451,-0.312,-1.188,-0.418,0.084,-1.977,-0.48
-0.369,-1.023,-0.499,-0.0,-1.803,-0.486,0.045,-1.111,-0.353,0.079,-1.564,-0.38,-0.363,-1.757,-0.499,-0.35,-1.354,-0.498,-0.371,-1.254,-0.471,-0.01,-1.998,-0.441
-0.365,-1.099,-0.466,-0.092,-1.876,-0.486,-0.037,-1.245,-0.321,-0.057,-1.615,-0.491,-0.378,-1.874,-0.491,-0.379,-1.512,-0.477,-0.361,-1.324,-0.454,-0.08,-1.956,-0.455
-0.369,-1.198,-0.445,-0.173,-1.98,-0.479,-0.136,-1.351,-0.352,-0.2,-1.706,-0.488,-0.337,-1.979,-0.481,-0.38,-1.615,-0.472,-0.377,-1.491,-0.485,-0.185,-1.954,-0.498
Expand
message.txt
49 KB
Puitato — 16:37
0.054,-1.789,-0.248,0.037,-1.446,-0.417,0.078,-0.713,-0.422,-0.025,-0.615,-0.348,0.339,-0.635,-0.489,0.141,-0.984,-0.141,-0.14,-1.445,-0.125,0.35,-1.129,-0.467
-0.123,-1.854,-0.357,-0.102,-1.561,-0.479,-0.003,-0.809,-0.46,-0.117,-0.677,-0.445,0.248,-0.763,-0.488,0.017,-1.066,-0.25,-0.261,-1.564,-0.23,0.232,-1.224,-0.491
-0.213,-1.91,-0.444,-0.196,-1.632,-0.454,0.012,-0.938,-0.478,-0.163,-0.766,-0.446,0.121,-0.845,-0.499,-0.115,-1.218,-0.319,-0.327,-1.628,-0.308,0.121,-1.321,-0.48
-0.253,-1.994,-0.483,-0.326,-1.726,-0.495,0.007,-1.054,-0.5,-0.262,-0.865,-0.448,0.021,-0.866,-0.499,-0.214,-1.36,-0.392,-0.377,-1.739,-0.379,0.033,-1.398,-0.493
-0.379,-1.973,-0.463,-0.369,-1.92,-0.499,0.005,-1.151,-0.479,-0.365,-0.972,-0.491,-0.074,-1.043,-0.454,-0.317,-1.506,-0.442,-0.333,-1.807,-0.486,-0.07,-1.502,-0.5
-0.364,-1.997,-0.481,-0.369,-1.988,-0.472,0.026,-1.232,-0.493,-0.363,-1.119,-0.466,-0.169,-1.153,-0.491,-0.379,-1.628,-0.467,-0.372,-1.887,-0.46,-0.162,-1.607,-0.447
Expand
message.txt
49 KB
matt. — 16:40
Target output is  [-0.377 -1.342 -0.5   -0.373 -1.993 -0.498 -0.357 -1.65  -0.496 -0.379
 -1.995 -0.437 -0.377 -1.897 -0.477 -0.375 -1.179 -0.497 -0.366 -1.588
 -0.496 -0.379 -1.998 -0.282]

Neural Network actual output is  [-0.01782343 -1.41800313 -0.38039553  0.13935875 -2.18010099 -0.37372566
  0.12047757 -2.03755685 -0.2948136  -0.0935214  -2.2408699  -0.38887332
  0.03923999 -1.35306062 -0.20196621 -0.060447   -1.61305828 -0.38170726
 -0.00729051 -0.90005655 -0.39388624 -0.19772656 -1.52439899 -0.30869014] there is an error (not MSQE) of  [-0.35917657  0.07600313 -0.11960447 -0.51235875  0.18710099 -0.12427434
 -0.47747757  0.38755685 -0.2011864  -0.2854786   0.2458699  -0.04812668
 -0.41623999 -0.54393938 -0.27503379 -0.314553    0.43405828 -0.11529274
 -0.35870949 -0.68794345 -0.10211376 -0.18127344 -0.47360101  0.02669014]
Puitato — 16:42
import random
import math
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2
Expand
message.txt
9 KB
matt. — 16:43
Image
gurrkee — 16:45
fitness += ((abs(reference[i] - candidate[i]-change[i]))*100)**2
Puitato — 16:45
-0.344,-1.202,-0.082,-0.273,-0.614,-0.332,0.101,-0.767,-0.361,-0.359,-0.838,-0.444,0.119,-0.793,-0.428,-0.356,-0.952,-0.092,0.057,-1.223,-0.191,0.006,-1.539,-0.178
-0.375,-1.217,-0.18,-0.351,-0.666,-0.43,0.018,-0.894,-0.462,-0.375,-0.932,-0.494,-0.002,-0.974,-0.439,-0.358,-1.084,-0.206,0.003,-1.327,-0.319,-0.113,-1.632,-0.232
-0.367,-1.274,-0.262,-0.363,-0.781,-0.461,-0.058,-0.992,-0.497,-0.31,-1.067,-0.495,-0.107,-1.073,-0.488,-0.357,-1.148,-0.148,-0.098,-1.437,-0.408,-0.189,-1.744,-0.355
-0.361,-1.348,-0.362,-0.343,-0.903,-0.485,-0.154,-1.083,-0.416,-0.368,-1.138,-0.485,-0.235,-1.153,-0.469,-0.346,-1.248,-0.066,-0.182,-1.538,-0.494,-0.295,-1.862,-0.453
-0.36,-1.481,-0.482,-0.372,-1.034,-0.499,-0.283,-1.18,-0.484,-0.376,-1.255,-0.476,-0.307,-1.249,-0.495,-0.373,-1.379,-0.023,-0.334,-1.631,-0.496,-0.364,-1.956,-0.495
-0.365,-1.583,-0.472,-0.358,-1.076,-0.495,-0.374,-1.279,-0.48,-0.356,-1.353,-0.459,-0.363,-1.298,-0.491,-0.351,-1.402,-0.003,-0.297,-1.558,-0.486,-0.303,-1.959,-0.5
Expand
message.txt
49 KB
Puitato — 16:57
import matplotlib.pyplot as plt
from spider_plot import plot_spider_pose

def test_spider_plot():
    """
    Generates a single 'full extension' frame for the spider
    so you can check that the plot_spider_pose function
    plots correctly.
    """
    # 8 legs * 3 joints = 24 angles
    # Coxa: 0 (centered), Femur: -1.0, Tibia: -0.5
    test_frame = []
    for leg in range(8):
        test_frame.append(0.0)    # Coxa
        test_frame.append(-1.0)   # Femur
        test_frame.append(-0.5)   # Tibia

    # Plot the frame
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])
    ax.set_zlim([-2, 2])

    plot_spider_pose(ax, test_frame)
    ax.set_title("Test Spider Plot: Full Extension Frame")
    plt.show()

test_spider_plot() 
0.107,-0.749,-0.268,0.144,-1.782,-0.051,-0.286,-1.451,-0.283,-0.068,-1.088,-0.245,0.204,-1.553,-0.495,-0.245,-1.944,-0.377,-0.333,-1.985,-0.0,-0.373,-1.04,-0.351
-0.03,-0.747,-0.389,-0.075,-1.772,-0.171,-0.192,-1.597,-0.345,-0.226,-1.165,-0.413,0.05,-1.501,-0.46,-0.241,-1.927,-0.42,-0.376,-1.93,-0.003,-0.267,-1.174,-0.396
-0.116,-0.848,-0.477,-0.222,-1.904,-0.254,-0.26,-1.759,-0.473,-0.301,-1.271,-0.444,0.023,-1.58,-0.468,-0.351,-1.957,-0.421,-0.358,-1.983,-0.039,-0.353,-1.136,-0.433
-0.246,-0.949,-0.483,-0.23,-1.877,-0.341,-0.321,-1.854,-0.442,-0.266,-1.415,-0.465,0.019,-1.784,-0.476,-0.331,-1.964,-0.357,-0.294,-1.919,-0.061,-0.355,-1.189,-0.469
-0.368,-1.001,-0.456,-0.318,-1.79,-0.483,-0.187,-1.98,-0.489,-0.34,-1.453,-0.386,-0.251,-1.969,-0.462,-0.338,-1.947,-0.429,-0.34,-1.95,-0.025,-0.333,-1.232,-0.386
-0.325,-1.098,-0.442,-0.354,-1.909,-0.473,-0.195,-1.959,-0.452,-0.288,-1.617,-0.359,-0.253,-1.891,-0.446,-0.334,-1.972,-0.31,-0.191,-1.72,-0.089,-0.351,-1.452,-0.481... (97 KB left)
Expand
message.txt
147 KB
gurrkee — 17:13
change = [random.choice([-0.1,0.1]) for _ in range(24)]
gurrkee — 17:35
import random
import math
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2
Expand
message.txt
9 KB
﻿
import random
import math
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from spider_plot import plot_spider_pose, forward_leg_kinematics2

best_fitness = []

# =========================== #
# CONSTANTS BOUNDARIES        #
# =========================== #

coxa_boundary = (-0.38, 0.38)
femur_boundary = (-2, -0.5)
tibia_boundary = (-0.5, 0)

joint_boundaries = [
    coxa_boundary,
    femur_boundary,
    tibia_boundary
]


def generate_frame():
    # ============================================================ #
    # Generates a single RANDOM frame inside of our set boundaries #
    # ============================================================ #

    frame = []

    for _ in range(8):
        # Instead of random.uniform(*coxa_boundary)
        frame.append(round(random.uniform(coxa_boundary[0], coxa_boundary[1]), 3))
        frame.append(round(random.uniform(femur_boundary[0], femur_boundary[1]), 3))
        frame.append(round(random.uniform(tibia_boundary[0], tibia_boundary[1]), 3))

    return frame


def fitness_function(reference, candidate, change):
    # ========================================================================================================== #
    # Evaluates how close a proposed next frame (candidate) is to the last frame (reference) + a change (change) #
    # Change makes sure to favor frames that are different from the last frame                                   #
    # ========================================================================================================== #

    fitness = 0
    for i in range(len(reference)):
        fitness += (abs(reference[i] - candidate[i] - change[i])*100)**2

    return fitness


def roulette_selection(ranked_population):
    # =============================================================================================================================== #
    # This selects random individuals of the current populations.                                                                     #
    # While a higher fitness equals to a higher chance to be selected, the process is still random, as all individuals have a chance. #
    # =============================================================================================================================== #

    sum = 0
    for i in ranked_population:
        sum += 1 / (1 + i[0]) ** 4

    roulette_wheel = []
    prev = 0
    for i in ranked_population:
        value = 1 / (1 + (i[0]) ** 4)
        roulette_wheel.append([prev + (value) / sum, i[1]])
        prev += (value) / sum

    selected = []
    for _ in range(len(ranked_population)):
        rand = random.random()
        for a in range(len(roulette_wheel)):
            if roulette_wheel[a][0] > rand:
                selected.append(roulette_wheel[a][1])
                break

    return selected


def crossover(selected):
    # =============================================================================================== #
    # This function crosses two parent frames at a random crossover point to make two child frames.   #
    # The two children have nothing in common:                                                        #
    # E.g.: [p1, p2, p3, p4, p5] + [q1, q2, q3, q4, q5] => [p1,p2, q3, q4, q5] + [q1, q2, p3, p4, p5] #
    # =============================================================================================== #

    out_population = []

    for i in range(0, len(selected), 2):

        parent1 = selected[i]

        if i + 1 < len(
                selected):  # this is so that if the selected list in odd, the last parent would get paired with a random other parent.
            parent2 = selected[i + 1]
        else:
            parent2 = random.choice(selected)

        crossover_point = random.randint(1, len(parent1) - 1)

        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

        out_population.append(child1)
        out_population.append(child2)

    return out_population


def mutate(population):
    # ====================================================================================== #
    # This goes through the entire population and their angles and mutates their values to a #
    # random value inside the boundaries with a chance of 0.2%                               #
    # ====================================================================================== #

    mutation_rate = 0.002

    for inv in range(len(population)):
        for i in range(len(population[inv])):
            if random.random() < mutation_rate:
                boundary = joint_boundaries[i % 3]

                min_val = boundary[0]
                max_val = boundary[1]

                population[inv][i] = round(random.uniform(min_val, max_val), 3)

    return population


def change_vector(latest_frame, last_change):
    change = []

    change_direction_prob = 0.025  # probability of a direction change
    change_scale = 0.2

    boundary_flat = [
        coxa_boundary[0], coxa_boundary[1],
        femur_boundary[0], femur_boundary[1],
        tibia_boundary[0], tibia_boundary[1]
    ]

    # Determines if the direction of change should stay the same.
    for i in range(len(last_change)):
        b_index = i % 3

        if random.random() > change_direction_prob and boundary_flat[b_index * 2] < latest_frame[i] < boundary_flat[b_index * 2 + 1]:
            change.append(last_change[i])
            
        else:
            if last_change[i] > 0:
                a = -1
            else:
                a = 1

            change.append(random.random() * change_scale * a)

    return change


def geneticA(latest_frame, last_change, size=500, generations = 500):
    # ================================================== #
    # This is the main function of the genetic Algorithm #
    # ================================================== #
    change = change_vector(latest_frame, last_change)

    population = []
    for _ in range(size):
        population.append(generate_frame())

    while generations > 1:
        generations -= 1

        rated_population = []
        for frame in population:
            fitness = fitness_function(latest_frame, frame, change)
            rated_population.append([fitness, frame])

        selected = roulette_selection(rated_population)

        population = crossover(selected)
        population = mutate(population)

    best = [10000, []]
    for frame in population:
        if best[0] > fitness_function(latest_frame, frame, change):
            best[0] = fitness_function(latest_frame, frame, change)
            best[1] = frame

    print("best", ["full", best[0]])
    best_fitness.append(["full", best[0]])
    return best[1], change


def animate_frames(frames, speed = 200):
    # ============================================================================== #
    # This is code to visualize the frames and has nothing to do with the actual GA. #
    # ============================================================================== #
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    def update(i):
        plot_spider_pose(ax, frames[i])
        return []

    ani = FuncAnimation(fig, update, frames=len(frames), speed=200)
    plt.show()


def main(nn=False):
    #How fast should the Animation run for?
    speed = 200
    #How many frames should the Animation have?
    amount_frames = 100
    
    latest_frame = generate_frame()
    total_frames = [latest_frame]

    change = [random.choice([-0.1,0.1]) for _ in range(24)]


    while len(total_frames) < amount_frames:
        print("progress", len(total_frames))
        new_frame, change = geneticA(latest_frame, change, 200, 200)
        total_frames.append(new_frame)
        latest_frame = new_frame
    print("total", total_frames)

    filename = 'output_data.csv'

    try:
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(total_frames)

        print(f"✅ Successfully wrote data to {filename}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

    print(best_fitness)

    if nn:
        return total_frames

    animate_frames(total_frames, speed)


main()
message.txt
9 KB
