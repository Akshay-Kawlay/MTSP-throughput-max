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

from salesman import *
from city import *

'''Inputs'''
city_list = []
salesman_list = []
dispatch_location = [43.653225, -79.383186]
traffic_factor = 1/80   #Assuming car runs at a constant 80 km/hr speed.


def load_data():
    with open('../data/cities.txt', 'r') as f:      # loading cities
        data = f.readlines()
        i = 0
        for line in data:
            arr = line.strip('\n').split(', ')
            lat = arr[0]; lon = arr[1]; sell_duration = arr[2]
            city_list.append(City(i, [lat,lon] ,sell_duration))
            i+=1
    with open('../data/salesmen.txt', 'r') as f:    #loading salesmen
        data = f.readlines()
        i = 0
        for line in data:
            work_time = line.strip('\n')
            print(work_time)
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

def main():            
    load_data()
    # print_loaded_cities_and_salesmen()



main()