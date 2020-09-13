from population import *
from route import *
import config
import NSGAII

class GA:
    mutationRate = 0.65
    tournamentSize = 10
    elitism = True
    runningAvg = 0

    @classmethod
    def evolvePopulation(cls, pop):
        newPopulation = Population(2*pop.populationSize, False)
        #copy over old population
        for i in range(0, pop.populationSize):
            newPopulation.saveRoute(i, pop.getRoute(i))

        # elitismOffset = 0
        # if cls.elitism:
        #     newPopulation.saveRoute(0, pop.getFittest())
        #     elitismOffset = 1
        for i in range(pop.populationSize, 2*pop.populationSize):
            parent1 = cls.tournamentSelection(pop)
            # parent2 = cls.tournamentSelection(pop)
            # child = cls.crossover(parent1, parent2)
            if random.random() < cls.mutationRate:
                child = cls.mutate(parent1)
            else:
                child = Route()
            # child = Route()
            newPopulation.saveRoute(i, child)

        # for i in range(elitismOffset, newPopulation.populationSize):
        #     cls.mutate(newPopulation.getRoute(i))

        #pareto optimization - total jobs and total distance
        function1_list = []
        function2_list = []
        for i in range(newPopulation.populationSize):
            final_route = newPopulation.getRoute(i)
            function1_list.append(final_route.getTotalJobs())
            function2_list.append(-1*final_route.getDistance())
        pareto_sorted_order = NSGAII.NSGAII_main(function1_list, function2_list, False)
        # print(pareto_sorted_order)
        i = 0
        pruned_pop = Population(pop.populationSize, False)
        for front in pareto_sorted_order:
            for route_index in front:
                temp_route = newPopulation.getRoute(route_index)
                pruned_pop.saveRoute(i, temp_route)
                # print("i = %d"%i)
                i+=1
                if i > config.population - 1:
                    break
            if i > config.population - 1:
                break

        #single objective optimization - total jobs
        newPopulation.sortByFitness()
        newPopulation.prune()

        return pruned_pop

    @classmethod
    def updateMutateProbability(cls, prob):
        if cls.mutationRate + prob >= 0 and cls.mutationRate + prob < 1:
            cls.mutationRate += prob
        # print("mutation prob = %f" %cls.mutationRate)

    @classmethod
    def mutate (cls, route):
        child_route = []
        flag = False
        for [start, end] in route.get_route():
            subroute = [start,end]
            if random.random() < cls.mutationRate:
                if random.random() < 0.5: # incremental mutation
                    if (route.isSubrouteValid([start+1, end+1])):
                        subroute = [start+1, end+1]
                        flag = True
                    elif (route.isSubrouteValid([start+1, end])):     # will increase capacity wastage (hill climbing)
                        subroute = [start+1, end]
                    else:
                        subroute = [start, end]     # mutation leads to invalid solution hence, skip mutation
                    # subroute = [start, end]
                else:   # decremental mutation
                    # subroute = [start, end]
                    if (route.isSubrouteValid([start-1, end])):
                        subroute = [start-1, end]
                        flag = True
                    elif (route.isSubrouteValid([start-1, end-1])):
                        subroute = [start-1, end-1]
                        flag = True
                    elif (route.isSubrouteValid([start, end-1])):      # will increase capacity wastage (hill climbing)
                        subroute = [start, end-1]
                    else:
                        subroute = [start, end]     # mutation leads to invalid solution hence, skip mutation
            else:   # no mutation
                subroute = [start,end]
            child_route.append(subroute)
        # print(route)
        # print(route)
            # if flag:
            #     print("Mutated")
        child = Route(child_route)
        return child

    @classmethod
    def tournamentSelection (cls, pop):
        tournament = Population(cls.tournamentSize, False)

        for i in range(cls.tournamentSize):
            randomInt = random.randint(0, pop.populationSize-1)
            tournament.saveRoute(i, pop.getRoute(randomInt))

        fittest = tournament.getFittest()
        return fittest
