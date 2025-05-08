from simulation import Simulation
from ant import Ant
from tqdm import tqdm
from queue import PriorityQueue


class AStarAlgorythm:
    def __init__(self, start, goal, grid):
        self.start = start
        self.goal = goal
        self.grid = grid

    def getSuccessors(self, node):
        x, y = node
        suc = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]):
                if self.grid[nx][ny] != 1:
                    suc.append((nx, ny))
        return suc

    def computePath(self, current, pred):
        path = [current]
        while pred[current] is not None:
            current = pred[current]
            path.append(current)
        path.reverse()
        return path

    def getH(self, node):
        return abs(node[0] - self.goal[0]) + abs(node[1] - self.goal[1])

    def astar(self):
        open = PriorityQueue()
        open.put((self.getH(self.start), 0, self.start))

        predecessor = {self.start: None}
        closed = set()
        best_g = {self.start: 0}

        while not open.empty():
            f, g, current = open.get()
            if current in closed:
                continue
            if current == self.goal:
                return self.computePath(current, predecessor)
            closed.add(current)
            for successor in self.getSuccessors(current):
                if successor in closed:
                    continue
                tentative_g = g + 1
                if successor not in best_g or tentative_g < best_g[successor]:
                    predecessor[successor] = current
                    best_g[successor] = tentative_g
                    f_score = tentative_g + self.getH(successor)
                    open.put((f_score, tentative_g, successor))
        return None  # Kein Pfad gefunden
    
# A Star Node = (f, g, (x,y)), predecessor = {node: predesessor}
# Heuristik = diff(goal - position)


class SearchBasedAnt(Ant):
    def __init__(self, x, y, team, simulation):
        super().__init__(x, y, team, simulation)
        self.nestPosition = (5,1)
        self.foodPosition = (7,25)
        self.path = []
        self.onWay = 'Food'

    def act(self):
        if self.onWay == 'Food':
            if self.path == []: self.search(self.foodPosition)
            if len(self.path) > 1:
                self.direction = (self.path[1][0] - self.path[0][0], self.path[1][1] - self.path[0][1])
                self.path.pop(0)
                # print(self.direction)
                self.move()
            else: 
                self.takeFood()
                self.search(self.nestPosition)
                self.onWay = 'Nest'
        elif self.onWay == 'Nest':
            if len(self.path) > 1:
                self.direction = (self.path[1][0] - self.path[0][0], self.path[1][1] - self.path[0][1])
                self.path.pop(0)
                # print(self.direction)
                self.move()


    def search(self, goal):
        # print(simulation.obstacleGrid)
        Search = AStarAlgorythm((self.x, self.y), goal, simulation.obstacleGrid)
        self.path = Search.astar()
        # print(self.path)



if __name__ == "__main__":
    simulation = Simulation(SearchBasedAnt, SearchBasedAnt, logfile="project01.rec")   
  
    simulation.loadArena("single01.txt")

    for t in tqdm(range(100)):
        simulation.tick()
    
    print(simulation.foodCount)

    simulation.shutdown()