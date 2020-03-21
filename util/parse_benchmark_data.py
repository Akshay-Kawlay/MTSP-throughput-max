
import random

def parse(filepath):
    with open(filepath, 'r') as f:      # loading cities
        data = f.readlines()
        i = 0
        lat_list = []
        lon_list = []
        for line in data:
            arr = line.strip('\n').strip(' ').split(' ')
            lat_list.append(arr[1]); lon_list.append(arr[2]); 
    filename = '../data/cities_rat99'
    with open(filename+"_60min_sell_duration.txt", 'w') as f:    # loading salesmen
        sd = 0
        for i in range(len(lat_list)):
            sd = 60            
            # sd = get_sell_duration()            
            line = lat_list[i]+", "+lon_list[i]+", "+str(sd)+"\n"
            f.write(line)

def get_sell_duration():
    prob = random.uniform(0, 1)
    if prob <= 0.33:
        return 60
    elif prob <= 0.66:
        return 120
    else:
        return 180

parse("../data/cities_rat99.txt")