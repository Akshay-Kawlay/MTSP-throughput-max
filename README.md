# MTSP-throughput-max
This is a variation of Multi Travelling Salesman Problem with an additional objective of maximizing throughput (number of cities visited by all salesmen)

# Defining the problem
A group of salesmen have to visit a list of cities/locations. 
Each city needs to be visited only by one salesman. A city becomes visited after the salesman sells their goods in that city. And each city has a ```sell duration``` (the expected amount of time it will take a salesman to sell their goods; the sell duration is a property of city and is different for different cities but same for all saleman visiting that city). 
Each salesman has fixed ```work time``` that they will work during.
The location is defined using latitude, longitude (lat,lon) numbers and a ```traffic_factor``` constant used to convert the lat,lon distance between two cities into time taken to drive from one to other.

# Objective
There are two main objectives here. 
First is same as the multi travelling saleman problem - `minimize the total distance travelled by all salesmen`
Second is to `maximize the total number of cities visited by all salesmen` in their fixed work time

# Implementation details

**Class City

*city_id - unique identifier (integer/number)*

*location - [lat, lon] (list of double of fixed size two)*

*sell_duration - (integer/number between 0 to 1440)*

**Class Salesman

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
