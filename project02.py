from tqdm import tqdm
import random
import os

from simulation import Simulation

from rant import RandomAnt
from base import BaselineAnt

if __name__ == "__main__":
    win_matrix = [0 for _ in range(40)]  
    filename = "sim_strght_pref.txt"

    while True:
        for i in range(30):
            pref_strght_A = random.randint(1,40)
            pref_strght_B = random.randint(1,40)

            simulation = Simulation(BaselineAnt, BaselineAnt,pref_strght_A, pref_strght_B, logfile="project02.rec")   
        
            simulation.loadArena("arena01.txt")

            for t in tqdm(range(10000)):
                simulation.tick()
            print(simulation.foodCount)

            if simulation.foodCount[0] > simulation.foodCount[1]:
                win_matrix[pref_strght_A-1] += abs(simulation.foodCount[0] - simulation.foodCount[1])
                win_matrix[pref_strght_B-1] -= abs(simulation.foodCount[0] - simulation.foodCount[1])
            elif simulation.foodCount[1] > simulation.foodCount[0]:
                win_matrix[pref_strght_B-1] += abs(simulation.foodCount[0] - simulation.foodCount[1])
                win_matrix[pref_strght_A-1] -= abs(simulation.foodCount[0] - simulation.foodCount[1])
            else:
                pass

            simulation.shutdown()
            print(i)

        # Step 1: Check if file exists and read existing list
        if os.path.exists(filename):
            with open(filename, "r") as f:
                line = f.readline().strip()
                if line:
                    existing_list = [int(x) for x in line.split(',')]
                else:
                    existing_list = [0] * 40
        else:
            existing_list = [0] * 40

        # Step 2: Add new_list to existing_list element-wise
        updated_list = [a + b for a, b in zip(existing_list, win_matrix)]

        # Step 3: Write the updated list back to the file
        with open(filename, "w") as f:
            f.write(','.join(str(x) for x in updated_list))

        print("Updated list saved to", filename)

        # print(win_matrix)