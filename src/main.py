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

'''Inputs'''
city_list = []
salesman_list = []
dispatch_location = [43.653225, -79.383186]
traffic_factor = 1/80   #Assuming car runs at a constant 80 km/hr speed.

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
            lat = float(arr[0]); lon = float(arr[1]); sell_duration = int(arr[2])
            city_list.append(City(i, [lat,lon] ,sell_duration))
            i+=1
    with open('../data/salesmen.txt', 'r') as f:    #loading salesmen
        data = f.readlines()
        i = 0
        for line in data:
            work_time = line.strip('\n')
            #print(work_time)
            salesman_list.append(Salesman(i, work_time))
            i+=1

def print_loaded_cities_and_salesmen():
    for city in city_list:
        print(city.get_id())
        print(city.get_location())
        print(city.get_sell_duration())
    for salesman in salesman_list:
        print(salesman.get_id())
        print(salesman.get_work_time())

def get_distance(first, second):        # slow, need to improve
    latlon1 = first.get_location()
    latlon2 = second.get_location()
    R = 6373.0  # radius of earth

    lat1 = latlon1[0]
    lon1 = latlon1[1]
    lat2 = latlon2[0]
    lon2 = latlon2[1]

    dlon = float(lon2) - float(lon1)
    dlat = float(lat2) - float(lat1)

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

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
        distance += get_distance(start_city, city_list[cities[0]])
        for i in range(len(cities)-1):
            distance += get_distance(city_list[cities[i]], city_list[cities[i+1]])
        distance += get_distance(city_list[cities[len(cities)-1]], start_city)
    print("Total distance", distance)

def run_algorithm():
    '''
    Approximation algorithm 
    '''

    return {}

def main():            
    load_data()
    solution = run_algorithm()
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