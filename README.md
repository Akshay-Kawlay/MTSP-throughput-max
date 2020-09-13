# MTSP-throughput-max
This is a variation of Multi Travelling Salesman Problem with an additional objective of maximizing throughput (number of cities visited by all salesmen)

# Defining the problem
A group of salesmen have to visit a list of cities/locations. 

Each city needs to be visited only by one salesman. A city becomes visited after the salesman sells their goods in that city. And each city has a ```sell duration``` (the expected amount of time it will take a salesman to sell their goods; the sell duration is a property of city and is different for different cities but same for all saleman visiting that city). 

Each salesman has fixed ```work time``` capacity that they will work during.

The location is defined using latitude, longitude (lat,lon) numbers and a ```traffic_factor``` constant used to convert the lat,lon distance between two cities into time taken to drive from one to other.

# Objective
There are two main objectives here.

First is same as the multi travelling saleman problem - `minimize the total distance travelled by all salesmen`

Second is to `maximize the total number of cities visited by all salesmen` in their fixed work time

# Implementation details

Class City

*city_id - unique identifier (integer/number)*

*location - [lat, lon] (list of double of fixed size two)*

*sell_duration - (integer/number between 0 to 1440)*

Class Salesman

*salesman_id - unique identifier (integer/number)*

*work_time - (integer between 0 to 1440)*

Assume: all Salesman start at same location - ```dispatch_location```

```
Input: 
1. list of Salesman
2. list of City
3. dispatch_location
4. traffic_factor
```

```
Output: 
1. for each salesman -> list of City it visited (dictionary/hashmap)
2. total distance travelled (integer/number)
3. total cities visited (integer/number).
```

# Algorithms

## Greedy w.r.t time
In this approach, we pick the first salesman in the list and choose to send him to the closest(in terms of distance) city. Then from there he goes to the next city that is closest to his current location and this continues. We also keep track of his time spent and stop once the time exceeds his `work time` capacity. We account for travel time from one city to another as well as city sell duration.
Once the salesman is timed out, we move to the next from the list and continue the same above process. This greedy approach only focuses on city distance and not city sell duration.

## Approach 1: Ant Colony with Kmeans
Kmeans algorithm is run first to create clusters of closely positioned locations. Then for each cluster, Ant Colony Optimization (ACO) is used to solve for single salesman TSP.

## Approach 2: Ant Colony with Genetic Algorithm
Ant colony is used to solve TSP (single salesman) on the location set. The resulting path is assumed to be the ground truth optimal. Next, genetic algorithm is used to search for the optimal subpath from the ground truth that fits in salesman work time capacity such that total capacity wastage of all salesmen is minimized and number of locations visited is maximized. The expectation is that subpath of an optimal path would also be close to optimal if not optimal. This approach performs better than above two.
