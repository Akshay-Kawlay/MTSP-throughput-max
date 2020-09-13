
#-----------------problem parameters-----------------------
depot = []
capacity = 120
time_dist_factor = 10      # time per job converted to distance 
num_salesmen = 5
# ---------------------------------------------------------
population = 50

nodes = []
node_num = 0
gnd_truth_tsp = []
gnd_truth_dist_list = []        # i-th element is distance between i-th and i+1 th element of gnd_truth_tsp
gnd_truth_dist_from_depot = []  # i-th element is distance of i-th element of gnd_truth_tsp from depot


def print_error(msg):
    print("ERROR: "+msg)
    exit()