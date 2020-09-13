'''
Code taken from rochakgupta repository
Github Reference : https://github.com/rochakgupta/aco-tsp.git
Reference : http://www.theprojectspot.com/tutorial-post/ant-colony-optimization-for-hackers/10
'''
import random
import math
import numpy as np
from aco_tsp import *

from galogic import *
import config
import NSGAII


import matplotlib.pyplot as plt


#-------------------------ACO-TSP-------------------------

def load_data(filename):
    global depot
    cities = []
    isdepot = 1
    with open(filename, 'r') as f:
        data = f.readlines()
        for line in data:
            arr = line.strip('\n').split(', ')
            x = int(arr[0]); y = int(arr[1])
            # arr = line.strip('\n').split(' ')
            # x = int(arr[1]); y = int(arr[2])
            if isdepot:         # first pair is depot by default
                depot = np.array([x,y])
                config.depot = depot
                isdepot = 0
            else:
                cities.append([x,y])


    print("loading data complete")
    return cities


def get_distance_from_depot(elem):
    return math.sqrt((elem[0] - depot[0])**2 + (elem[1] - depot[1])**2)

def euclidean_distance(one, two):
        return math.sqrt((one[0] - two[0])**2 + (one[1] - two[1])**2)


_nodes = load_data("benchmarks/cities_eil51_60min_sell_duration.txt")
# _nodes = load_data("benchmarks/eil101.txt")

config.nodes = _nodes
config.node_num = len(_nodes)

_colony_size = 5
_steps = 400        

max_min = SolveTSPUsingACO(mode='MaxMin', colony_size=_colony_size, steps=_steps, nodes=_nodes)
max_min.run()
max_min.plot()
plt.scatter(depot[0], depot[1])
plt.show()

gnd_truth_route = max_min.get_global_best_tour()
print(gnd_truth_route)
print(len(gnd_truth_route))
config.gnd_truth_tsp = gnd_truth_route

# load distance list of gnd_truth_tsp
gnd_truth_distance = []
for i in range(len(config.gnd_truth_tsp)-1):
    node1 = config.nodes[config.gnd_truth_tsp[i]]
    node2 = config.nodes[config.gnd_truth_tsp[i+1]]
    dist = euclidean_distance(node1, node2)
    gnd_truth_distance.append(dist)

config.gnd_truth_dist_list = gnd_truth_distance

#load ground truth distance from depot list
temp = []
for i in range(len(config.gnd_truth_tsp)):
    node1 = config.nodes[config.gnd_truth_tsp[i]]
    dist = euclidean_distance(config.depot, node1)
    temp.append(dist)

config.gnd_truth_dist_from_depot = temp
# print(config.gnd_truth_dist_list)
# print(len(config.gnd_truth_dist_list))
# print(config.gnd_truth_dist_from_depot)
# print(len(config.gnd_truth_dist_from_depot))

#----------------------------------------------------------------------

#----------------------GA-Subsequence----------------------------------

pop = Population(config.population, True)

print ('Initial Route: ', pop.getFittest().get_route())
print ('Initial distance: ' + str(pop.getFittest().getDistance()))
print ('Initial Jobs: ' + str(pop.getFittest().getTotalJobs()))
print ('Initial capacity wastage: ' + str(pop.getFittest().getCapacityWastage()))
yaxis = []
xaxis = []
prev_fitness = 0 
for i in range(200):
    pop = GA.evolvePopulation(pop)
    fittest = pop.getFittest().getFitness()
    yaxis.append(fittest)
    xaxis.append(i)
    if fittest <= prev_fitness:     #approaching plateau or leaving optimal, increase exploration (randomness), decrease exploitation (mutation) 
        GA.updateMutateProbability(-0.01)
    elif fittest > prev_fitness:    # enourage more exploitation
        GA.updateMutateProbability(0.15)
    prev_fitness = fittest


soln = pop.getFittest()
print ('Final distance: ' + str(soln.getDistance()))
print ('Total Jobs: ' + str(soln.getTotalJobs()))
print ('Final capacity wastage: ' + str(soln.getCapacityWastage()))
print ('Final Route: ', soln.get_route())
fig = plt.figure()
path_x = []; path_y = []

# plt.plot(xaxis, yaxis, 'r-')
# plt.show()

# ---------------------------NSGA-II Output--------------------------------------

function1_list = []
function2_list = []
for i in range(pop.populationSize):
    final_route = pop.getRoute(i)
    function1_list.append(final_route.getTotalJobs())
    function2_list.append(-1*final_route.getDistance())

optimal_pareto_front = NSGAII.NSGAII_main(function1_list, function2_list, True)
print("Pareto optimal solutions :")

pareto_solutions = []
max_jobs = -1
max_soln = None
for index in optimal_pareto_front[0]:
    temp = [pop.getRoute(index).getDistance(), pop.getRoute(index).getTotalJobs(), pop.getRoute(index).getCapacityWastage()]
    if temp not in pareto_solutions:    # no duplicates
        pareto_solutions.append(temp)
        if max_jobs < pop.getRoute(index).getTotalJobs():
            max_soln = pop.getRoute(index)

print("")

for par in pareto_solutions:
    print ('Final distance: ' + str(par[0]))
    print ('Total Jobs: ' + str(par[1]))
    print ('Final capacity wastage: ' + str(par[2]))
    print(" ")
plt.show()
   
# plt.plot(path_x, path_y)
# plt.scatter(path_x, path_y)

# plt.plot(xaxis, yaxis, 'r-')
# plt.show()
plt.scatter(config.depot[0], config.depot[1], color="k", s=50)
for i in range(config.node_num):
    plt.scatter(config.nodes[i][0], config.nodes[i][1], color="b", s=30)

soln_route = soln.get_route()

for [start, end] in soln_route:
    x = [depot[0]]
    y = [depot[1]]
    for i in range(start, end+1):
        temp = config.gnd_truth_tsp[i]
        x.append(config.nodes[temp][0])
        y.append(config.nodes[temp][1])
    x.append(depot[0])
    y.append(depot[1])
    plt.plot(x, y, linewidth=1)
plt.title("ACO+GA")
for id in config.gnd_truth_tsp:
    plt.annotate(str(id), config.nodes[id], size=8)
plt.show()

#----------------------------------EOF--------------------------------------------
