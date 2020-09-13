'''
Code taken from rochakgupta repository
Github Reference : https://github.com/rochakgupta/aco-tsp.git
Reference : http://www.theprojectspot.com/tutorial-post/ant-colony-optimization-for-hackers/10
'''
import random
import math
import numpy as np
from aco_tsp import *
from kmeans import *

depot = []
# capacity = 100

def load_data(filename):
    global depot
    cities = []
    isdepot = 1
    with open(filename, 'r') as f:
        data = f.readlines()
        for line in data:
            # arr = line.strip('\n').split(', ')
            # x = int(arr[0]); y = int(arr[1])
            arr = line.strip('\n').split(' ')
            x = int(arr[1]); y = int(arr[2])
            if isdepot:         # first pair is depot by default
                depot = np.array([x,y])
                isdepot = 0
            else:
                cities.append([x,y])


    print("loading data complete")
    return cities


def get_distance_from_depot(elem):
    return math.sqrt((elem[0] - depot[0])**2 + (elem[1] - depot[1])**2)

_nodes = load_data("benchmarks/eil101.txt")

# print(_nodes)
num_salesmen = 5
nod = np.array(_nodes)
km = K_Means(num_salesmen)
km.fit(nod)

km.add_depot(depot)
# print(km.classes)


_colony_size = 5
_steps = 200
capacity = 120
time_dist_factor = 10   
total_dist_sum = 0
total_jobs_sum = 0
capacity_wastage = 0
for c_id in km.classes:
    cities_base = list(km.classes[c_id])
    min_cost = 999999999999999999999
    cities_base.sort(key=get_distance_from_depot)
    # print(cities_base)
    prev_aco = None
    prev_cost = None
    rem_cap = 0
    for i in range(2, len(cities_base)):
        cities = cities_base[:i]
        aco = SolveTSPUsingACO(mode='MaxMin', colony_size=_colony_size, steps=_steps, nodes=cities)
        aco.run()
        cost = aco.get_best_total_distance() + (i-1)*time_dist_factor   # here we assume each job takes same amount of time, future work - variable time per job
        if cost > capacity:
            break
        prev_aco = aco
    total_dist_sum += prev_aco.get_best_total_distance()
    total_jobs_sum += prev_aco.get_num_nodes() - 1  # don't count depot
    capacity_wastage += capacity - (prev_aco.get_best_total_distance() + (prev_aco.get_num_nodes() - 1)*time_dist_factor)
    prev_aco.plot()

print("TOTAL DISTANCE", total_dist_sum)
print("TOTAL JOBS COMPLETED", total_jobs_sum)
print("CAPACITY WASTAGE", str(capacity_wastage))
print("CAPACITY WASTAGE PERCENT = %.2f" % (capacity_wastage/(capacity*num_salesmen)*100))

colors = 5*["r", "c", "k", "g", "b", "y", "m"]

for classification in km.classes:
    color = colors[classification]
    for features in km.classes[classification]:
        plt.scatter(features[0], features[1], color = color,s = 30)

plt.show()


# --------------------------------------------------------------------------------------------------------

# _nodes = [(random.uniform(-400, 400), random.uniform(-400, 400)) for _ in range(0, 15)]
# acs = SolveTSPUsingACO(mode='ACS', colony_size=_colony_size, steps=_steps, nodes=_nodes)
# acs.run()
# acs.plot()
# elitist = SolveTSPUsingACO(mode='Elitist', colony_size=_colony_size, steps=_steps, nodes=_nodes)
# elitist.run()
# elitist.plot()

# max_min = SolveTSPUsingACO(mode='MaxMin', colony_size=_colony_size, steps=_steps, nodes=_nodes)
# max_min.run()
# max_min.plot()

# Plotting
# colors = 10*["r", "c", "k", "g", "b"]

# for centroid in km.centroids:
#     plt.scatter(km.centroids[centroid][0], km.centroids[centroid][1], s = 130, marker = "x")

# for classification in km.classes:
#     color = colors[classification]
#     for features in km.classes[classification]:
#         plt.scatter(features[0], features[1], color = color,s = 30)

# plt.show()