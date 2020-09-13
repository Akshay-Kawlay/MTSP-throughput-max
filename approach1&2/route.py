import config
import random
import math

class Route:

    def __init__ (self, route = None):
        self.route = []
        self.fitness = 0
        self.distance = 0
        self.capWaste = 0
        self.jobs = 0
        if route == None:
            #generate random route subsequence
            for _ in range(config.num_salesmen):
                r = random.randint(0,len(config.nodes)-4)   #margin to avoid out of range error
                while (self.isVisited(r)):
                    r = random.randint(0,len(config.nodes)-4)
                cost = config.gnd_truth_dist_from_depot[r] + config.time_dist_factor
                start = r
                while ((cost + config.gnd_truth_dist_list[r] + config.time_dist_factor + config.gnd_truth_dist_from_depot[r+1] < config.capacity) and (not self.isVisited(r))):
                    cost += config.gnd_truth_dist_list[r] + config.time_dist_factor
                    if (self.isVisited(r+1)):
                        break
                    if r >= config.node_num - 2:
                        break
                    # if r >= 10:
                    #     break
                    r+=1
                if cost + config.gnd_truth_dist_from_depot[r] > config.capacity:
                    self.route.append([start, r-1])
                    self.jobs += r-1 - start + 1
                    self.capWaste += config.capacity - cost - config.gnd_truth_dist_from_depot[r-1] + config.gnd_truth_dist_list[r] + config.time_dist_factor
                else:
                    self.route.append([start, r])
                    self.jobs += r - start + 1
                    self.capWaste += config.capacity - cost - config.gnd_truth_dist_from_depot[r]
            # if(self.getCapacityWastage() < 0):
            #     print("ERROR CAPACITY")
        else:
            self.route = route
            # if(self.getCapacityWastage() < 0):
            #     print("ERROR CAPACITY")
            #     print(self.route)
            #     exit()

    def isVisited(self, r):
        for [start, end] in self.route:
            if r >= start and r <= end:
                return True
        return False

    def get_route(self):
        return self.route
    
    def getFitness(self):
        if self.fitness == 0:
            self.fitness = (self.getTotalJobs())
        return self.fitness

    def getDistance(self):
        if self.distance == 0:
            routeDistance = 0
            for subroute in self.route:
                routeDistance += self.getSubrouteDistance(subroute)
            self.distance = routeDistance
        return self.distance

    def getSubrouteDistance(self, subroute):
        start = subroute[0]
        end = subroute[1]
        depotDistance = config.gnd_truth_dist_from_depot[start]+config.gnd_truth_dist_from_depot[end]
        distance = 0
        for i in range(start, end):
            distance += config.gnd_truth_dist_list[i]
        return depotDistance + distance

    def isSubrouteValid(self, subroute):
        start = subroute[0]
        end = subroute[1]
        if start > end or start < 0 or end > config.node_num -1:
            return False
        if int(self.isVisited(start)) + int(self.isVisited(end)) > 1:    # checks if subroute does not clash with others
            return False
        job_count = end - start + 1
        return config.capacity > (self.getSubrouteDistance(subroute) + job_count*config.time_dist_factor)

    def getTotalJobs(self):
        if self.jobs == 0:
            for [start, end] in self.route:
                self.jobs += end - start + 1
        return self.jobs

    def getCapacityWastage(self):
        if self.capWaste == 0:
            dist = 0
            for subroute in self.route:
                dist = self.getSubrouteDistance(subroute)
                # if config.capacity < dist + ((subroute[1] - subroute[0] + 1)*config.time_dist_factor):
                #     print("EOORROROROROR")
                #     print(config.capacity - dist - (subroute[1] - subroute[0] + 1)*config.time_dist_factor)
                self.capWaste += config.capacity - dist - (subroute[1] - subroute[0] + 1)*config.time_dist_factor
        return self.capWaste

    def routeSize(self):
        size = len(self.route)
        return size

