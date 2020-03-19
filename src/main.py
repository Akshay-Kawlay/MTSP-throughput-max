# MIT License

# Copyright (c) 2019 Akshay-Kawlay

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from math import sin, cos, sqrt, atan2, radians
from salesman import *
from city import *
from genetic_algorithm import *

'''Inputs'''
city_list = []
salesman_list = []
dispatch_location = [43.653225, -79.383186]     # [lat, lon]
traffic_factor = 1.0/60.0   # Assuming car runs at a constant 80 km/hr speed.

'''Outputs'''
salesman_to_cities = {}     # salesman_id -> list of city_ids visited
total_distance = NotImplemented
total_cities_visited = NotImplemented


def load_data():
    with open('../data/cities.txt', 'r') as f:      # loading cities
        data = f.readlines()
        i = 0
        for line in data:
            arr = line.strip('\n').split(', ')
            lat = float(arr[0]); lon = float(arr[1]); sell_duration = float(arr[2])
            city_list.append(City(i, [lat,lon] ,sell_duration))
            i+=1
    with open('../data/salesmen.txt', 'r') as f:    # loading salesmen
        data = f.readlines()
        i = 0
        for line in data:
            work_time = line.strip('\n')
            #print(work_time)
            salesman_list.append(Salesman(i, work_time))
            i+=1

def compute_cost_matrix():
    '''
    creates an asymmetric matrix of travel time between all pairs of cities
    Includes sell duration of cities
    '''
    n = len(city_list)
    cost_matrix = [[-1 for i in range(n)] for j in range(n)]

    #get travel time with sell duration
    for i in range(n):
        for j in range(n):
            sell_duration = city_list[j].get_sell_duration()
            cost_matrix[i][j] = traffic_factor*get_distance(city_list[i], city_list[j]) +  sell_duration
    # print(cost_matrix)

    return cost_matrix

def print_loaded_cities_and_salesmen():
    for city in city_list:
        print(city.get_id())
        print(city.get_location())
        print(city.get_sell_duration())
    for salesman in salesman_list:
        print(salesman.get_id())
        print(salesman.get_work_time())

def get_distance(first, second):        # slow, need to improve
    '''
    first (type : City)
    second (type : City)
    return the distance between first city and second city
    '''
    latlon1 = first.get_location()
    latlon2 = second.get_location()
    R = 6373.0  # radius of earth

    lat1 = radians(latlon1[0])
    lon1 = radians(latlon1[1])
    lat2 = radians(latlon2[0])
    lon2 = radians(latlon2[1])

    dlon = float(lon2) - float(lon1)
    dlat = float(lat2) - float(lat1)

    a = sin(dlat / 2.0)**2.0 + cos(lat1) * cos(lat2) * sin(dlon / 2.0)**2.0
    c = 2.0 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def calculate_results(solution):
    num_cities_visited = 0
    
    global dispatch_location

    if len(solution) <= 0:
        print("Error: Solution Empty")
        return
    
    #calculate total cities visited
    for s_id in solution:
        num_cities_visited += len(solution[s_id])
    print("Total city throughput", num_cities_visited)
    
    #calculate distance
    distance = 0
    start_city = City(-1, dispatch_location, 0)
    for s_id in solution:
        cities = solution[s_id]
        if len(cities) <= 0:
            continue
        distance += get_distance(start_city, city_list[cities[0]])
        for i in range(len(cities)-1):
            distance += get_distance(city_list[cities[i]], city_list[cities[i+1]])
        distance += get_distance(city_list[cities[len(cities)-1]], start_city)
    print("Total distance", distance)

def run_greedy_algorithm(cost_matrix):
    '''
    Choosing closest city (smallest distance) first
    '''
    global salesman_to_cities
    # set all cities to not visited
    for city in city_list:
        city.visited = False

    # initialize salesman_to_city
    for salesman in salesman_list:
        salesman_to_cities[salesman.get_id()] = []
    
    # return_dist = 0
    next_city = 0
    start_city = City(-1, dispatch_location, 0)
    for salesman in salesman_list:
        current_city = start_city
        capacity = float(salesman.get_work_time())
        while(capacity > 0.0):
            min_time = float("inf")
            for i in range(len(city_list)):     # find the closest unvisited city
                if not city_list[i].visited:
                    #return_dist = get_distance(city_list[i], start_city)
                    if current_city.get_id() < 0:       # starting location
                        cost = get_distance(current_city, city_list[i])*traffic_factor + city_list[i].get_sell_duration()
                    else:
                        cost = cost_matrix[current_city.get_id()][city_list[i].get_id()]

                    if cost < min_time:
                        min_time = cost
                        next_city = city_list[i]

            if capacity > min_time:
                capacity -= min_time
                next_city.visited = True
                current_city = next_city
                salesman_to_cities[salesman.get_id()].append(next_city.get_id())
            else:
                break

    print(salesman_to_cities)
    return salesman_to_cities

def run_smallest_first_algorithm():
    '''
    Choosing smallest sell duration city first and map them to decending order of salesmen capacity
    This algorithm's goal is to generate maximum sales and does not consider travel cost
    '''
    global salesman_to_cities
    # set all cities to not visited
    for city in city_list:
        city.visited = False

    # initialize salesman_to_city
    for salesman in salesman_list:
        salesman_to_cities[salesman.get_id()] = []

    sorted_city_list = sorted(city_list, key=lambda x: x.sell_duration, reverse=False)
    sorted_salesman_list = sorted(salesman_list, key=lambda x: x.work_time, reverse=False)
    cur_salesman_id = 0
    capacity = float(sorted_salesman_list[cur_salesman_id].get_work_time())
    for city in sorted_city_list:
        if (capacity > city.sell_duration):
            salesman_to_cities[cur_salesman_id].append(city.get_id())
            capacity -= city.sell_duration
        else:
            cur_salesman_id += 1
            if cur_salesman_id >= len(sorted_salesman_list):
                break
            capacity = float(sorted_salesman_list[cur_salesman_id].get_work_time())
        # print(city.sell_duration)
    print(salesman_to_cities)
    return salesman_to_cities

# def run_mtsp_simulated_annealing():
#     '''
#     Solved only mtsp problem. Does not consider salesman capacity and city sell duration
#     Returns solution by simulated annealing
#     '''
#     m = len(salesman_list)  # number of agents
#     temp = 10000            # initial temperature
#     coolingRate = 0.003
#     while (temp > 1):
        
    

def main():
    load_data()
    cost_matrix = compute_cost_matrix()
    solution = run_greedy_algorithm(cost_matrix)
    # solution = run_smallest_first_algorithm()
    calculate_results(solution)
    # print_loaded_cities_and_salesmen()

def test():
    load_data()
    solution = {}
    solution['1'] = [1,20,30]
    solution['2'] = [2,3,4]
    calculate_results(solution)

main()
# test()