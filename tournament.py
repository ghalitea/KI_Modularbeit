from tqdm import tqdm

from simulation import Simulation
from rant import RandomAnt
from base import BaselineAnt

def tournament(participants, matches, switch, time, arena, log):
    plan = []
    scores = { p: 0 for p in participants }
    for a in range(0, len(participants)):
        for b in range(a, len(participants)):
            if not a == b:
                for m in range(matches):
                    plan.append((participants[a], participants[b], m))
                    if switch:
                        plan.append((participants[b], participants[a], matches + m))

    for game in tqdm(plan):
        A, B, m = game
        name = A.__name__ + '_vs_' + B.__name__ + '_' + str(m) + '.rec'
        
        if not log:
            name = None

        simulation = Simulation(A, B, name)
        simulation.loadArena(arena)
        for t in range(time):
            simulation.tick()
        result = simulation.foodCount
        if result[0] > result[1]:
            scores[A] += 1
        elif result[1] > result[0]:
            scores[B] += 1
        simulation.shutdown()

    scores_view = [ (score, participant.__name__) for participant,score in scores.items() ]
    scores_view.sort(reverse=True) 
    for score,participant in scores_view:
        print(participant + ' : ' + str(score))


if __name__ == "__main__":
    tournament([BaselineAnt, RandomAnt], 5, True, 10000, "arena01.txt", False)