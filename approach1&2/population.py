from route import *

class Population:
    routes = []

    def __init__ (self, populationSize, initialise):
        self.populationSize = populationSize
        if initialise:
            for i in range(populationSize):
                newRoute = Route()
                self.routes.append(newRoute)
        else:
            self.routes = [[] for i in range(self.populationSize)]

    def saveRoute (self, index, route):
        self.routes[index] = route

    def getRoute (self, index):
        return self.routes[index]

    def getFittest (self):
        fittest = self.routes[0]

        for i in range(1, self.populationSize):
            if fittest.getFitness() <= self.getRoute(i).getFitness():
                fittest = self.getRoute(i)

        return fittest

    def populationSize(self):
        return int(self.populationSize)

    def equals(self, pop):
        self.routes = pop.routes

    def getFitnessHelper(self, route):
        return route.getFitness()

    def sortByFitness(self):
        self.routes.sort(key=self.getFitnessHelper, reverse=True)

    def prune(self):
        self.routes = self.routes[:self.populationSize/2]
        self.populationSize = self.populationSize / 2