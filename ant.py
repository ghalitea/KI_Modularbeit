
class Ant:
    def __init__(self, x, y, team, simulation):
        self.x = x
        self.y = y
        self.team = team
        self.simulation = simulation
        self.hasFood = False
        self.directions = [(0,0), (-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down
        self.direction = (0, 0)
        self.energy = 1
    
    def act(self):
        pass

    def move(self):
        if self.energy < 1:
            return

        if not self.direction in self.directions:
            return
        
        dx, dy = self.direction

        nx = self.x + dx
        ny = self.y + dy

        if ((nx >= 0) and (ny >= 0) and (nx < self.simulation.gridWidth) and (ny < self.simulation.gridHeight) and (self.simulation.obstacleGrid[nx][ny] == 0)):
            self.x = nx
            self.y = ny
            self.energy -= 1
    
    def senseFood(self):
        return [self.simulation.foodGrid[self.x + dx][self.y + dy] for (dx,dy) in self.directions]

    def takeFood(self):
        if (self.simulation.foodGrid[self.x][self.y] > 0 and not self.hasFood):  
            self.hasFood = True
            self.simulation.foodGrid[self.x][self.y] -= 1  

            return True
        return False
    
    def dropFood(self):
        if (self.hasFood):
            self.simulation.foodGrid[self.x][self.y] += 1
            self.hasFood = False
    
    def senseOwnPheromone(self):
        return [self.simulation.pheromoneGrid[self.team][self.x + dx][self.y + dy] for (dx,dy) in self.directions]
    
    def senseOtherPheromone(self):
        return [self.simulation.pheromoneGrid[1 - self.team][self.x + dx][self.y + dy] for (dx,dy) in self.directions]

    def dropPheromone(self):
        self.simulation.pheromoneGrid[self.team][self.x][self.y] = 1.0

    def atOwnNest(self):
        return self.simulation.nestGrid[self.team][self.x][self.y] > 0
    
    def atOtherNest(self):
        return self.simulation.nestGrid[1 - self.team][self.x][self.y] > 0