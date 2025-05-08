from tqdm import tqdm
import random

from simulation import Simulation

from rant import RandomAnt
from base import BaselineAnt

if __name__ == "__main__":
    win_matrix = [[0 for _ in range(6)] for _ in range(8)] # [pref_direc][pref_pher]

    for i in range(480):
        pref_direc_A = random.randint(1,8)
        pref_pher_A = random.randint(1,6)
        pref_direc_B = random.randint(1,8)
        pref_pher_B = random.randint(1,6)

        simulation = Simulation(BaselineAnt, BaselineAnt,[pref_direc_A,pref_pher_A], [pref_direc_B,pref_pher_B], logfile="project02.rec")   
    
        simulation.loadArena("arena01.txt")

        for t in tqdm(range(10000)):
            simulation.tick()
        print(simulation.foodCount)

        if simulation.foodCount[0] > simulation.foodCount[1]:
            win_matrix[pref_direc_A-1][pref_pher_A-1] += abs(simulation.foodCount[0] - simulation.foodCount[1])
        elif simulation.foodCount[1] > simulation.foodCount[0]:
            win_matrix[pref_direc_B-1][pref_pher_B-1] += abs(simulation.foodCount[0] - simulation.foodCount[1])
        else:
            pass

        simulation.shutdown()
        print(i)
    print(win_matrix)