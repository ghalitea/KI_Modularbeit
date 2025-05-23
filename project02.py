from tqdm import tqdm
import random
import os

from simulation import Simulation

from rant import RandomAnt
from base import BaselineAnt
from enemant import EnemyAnt

if __name__ == "__main__":
    N = 60  # List length

    won_points = []  
    times_played = []  
    filename = "sim_direc_pref_base.txt"

    while True:
        won_points = [0 for _ in range(N)]  
        times_played = [0 for _ in range(N)]  

        for i in range(30):
            pref_A = random.randint(1,N)
            pref_B = random.randint(1,N)
            times_played[pref_A-1] +=1
            times_played[pref_B-1] +=1

            simulation = Simulation(BaselineAnt, BaselineAnt,pref_direc=(pref_A, pref_B), logfile="project02.rec")   
        
            simulation.loadArena("arena01.txt")

            for t in tqdm(range(10000)):
                simulation.tick()
            print(simulation.foodCount)

            if simulation.foodCount[0] > simulation.foodCount[1]:
                won_points[pref_A-1] += abs(simulation.foodCount[0] - simulation.foodCount[1])
                won_points[pref_B-1] -= abs(simulation.foodCount[0] - simulation.foodCount[1])
            elif simulation.foodCount[1] > simulation.foodCount[0]:
                won_points[pref_A-1] -= abs(simulation.foodCount[0] - simulation.foodCount[1])
                won_points[pref_B-1] += abs(simulation.foodCount[0] - simulation.foodCount[1])
            else:
                pass

            simulation.shutdown()
            print(i)


        

        # Step 1: Read existing lists (initialize if missing)
        if os.path.exists(filename):
            with open(filename, "r") as f:
                lines = [line.strip() for line in f.readlines()]
                existing_won_points = [int(x) for x in lines[0].split(',')] if len(lines) > 0 and lines[0] else [0] * N
                existing_times_played = [int(x) for x in lines[1].split(',')] if len(lines) > 1 and lines[1] else [0] * N
        else:
            existing_won_points = [0] * N
            existing_times_played = [0] * N

        # Step 2: Update the first two lists (cumulative sum)
        updated_won_points = [a + b for a, b in zip(existing_won_points, won_points)]
        updated_times_played = [a + b for a, b in zip(existing_times_played, times_played)]

        # Step 3: Calculate the third list (ratios, handle division by zero)
        ratios = [
            (wp / tp if tp != 0 else 0)
            for wp, tp in zip(updated_won_points, updated_times_played)
        ]

        # Step 4: Write all three lists back to the file
        with open(filename, "w") as f:
            f.write(','.join(str(x) for x in updated_won_points) + '\n')
            f.write(','.join(str(x) for x in updated_times_played) + '\n')
            f.write(','.join(f"{x:.4f}" for x in ratios) + '\n')  # 4 decimal places

        print("Updated lists saved to", filename)

