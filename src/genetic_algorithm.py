'''
Solution : dictionary of salesman id --> list of city ids
1. Initialize population
2. Crossover, Mutation
3. Selection - elitist (later adopt simulated annealing to select bad solutions)
4. Fitness - weighted sum of total distance and jobs completed
5. Termination : Repeat till time limit or fitness level achieved or iterations completed

Approach 1
Step 1 : Run mtsp as normally
Step 2 : From the solution, apply capacity constraints and select the subsequences of list of cities for each tech 
         such that number of cities visited is maximized

Approach 2
Step 1 : Run clustering (K-Means) algorithm on city dataset. Number of clusters = number of salesman
         Modify K-Means such that it accomodates for the capacity constraint
Step 2 : Assign each cluster to a salesman, run TSP for each salesman in that cluster
'''

import random

# global constants
P_SIZE = 10

def initialize_population(city_list, salesman_list):
    '''
    returns list of solutions
    solution --> {salesman id -> list of city ids}
    '''
    population = []
    # for i in range(P_SIZE):
    #     for j in range(len(city_list)):
            

    return []

def perform_crossover(population):
    '''
    returns list of solutions
    solution --> {salesman id -> list of city ids}
    '''
    return []

def mutate(population):
    '''
    returns list of solutions
    solution --> {salesman id -> list of city ids}
    '''
    return []

def selection(new_population):
    '''
    Select only P_SIZE solutions from new_population
    '''
    return []

def run_genetic_algorithm(epoch, cx_p):
    best_solution = {}; population = []; new_population = []

    population = initialize_population()
    cx_probability = 0
    for i in range(epoch):
        cx_probability = random.uniform(0, 1)
        if cx_probability >= cx_p:      #crossover
            new_population = perform_crossover(population)
        else:                           #mutation
            new_population = mutate(population)
        population = selection(new_population)

    return best_solution