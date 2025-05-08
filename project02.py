from tqdm import tqdm

from simulation import Simulation

from rant import RandomAnt
from base import BaselineAnt

if __name__ == "__main__":
    simulation = Simulation(BaselineAnt, RandomAnt, logfile="project02.rec")   
  
    simulation.loadArena("arena01.txt")

    for t in tqdm(range(10000)):
        simulation.tick()
    print(simulation.foodCount)

    simulation.shutdown()