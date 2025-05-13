import pickle

class Simulation:
    def __init__(self, antA, antB, pref_strght=(24,24), pref_direc=(4,4), pref_pher=(6,6), logfile=None):
        self.gridWidth = 32
        self.gridHeight = 32

        self.pheromoneDecay = 0.99
        self.pheromoneThreshold = 0.01
        self.ants = [] 

        # 2 Teams
        self.antA = antA
        self.antB = antB
        self.teamA = 0
        self.teamB = 1

        self.pref_strght = pref_strght
        self.pref_direc = pref_direc
        self.pref_pher = pref_pher

        # Create the grids
        self.foodGrid = [[0 for _ in range(self.gridWidth)] for _ in range(self.gridHeight)]
        self.obstacleGrid = [[0 for _ in range(self.gridWidth)] for _ in range(self.gridHeight)]
        self.nestGrid = [[[0 for _ in range(self.gridWidth)] for _ in range(self.gridHeight)], [[0 for _ in range(self.gridWidth)] for _ in range(self.gridHeight)]]
        self.pheromoneGrid = [[[0.0 for _ in range(self.gridWidth)] for _ in range(self.gridHeight)], [[0.0 for _ in range(self.gridWidth)] for _ in range(self.gridHeight)]]
        
        self.foodCount = [0, 0]

        if logfile:
            self.logfile = open(logfile, 'wb')
        else:
            self.logfile = None

    def loadArena(self, path):
        file = open(path, "r")
        x = 0
        y = 0
        while True:
            line = file.readline()
            if not line:
                break
            for c in line:
                if c == 'A':
                    self.nestGrid[self.teamA][x][y] = 1
                elif c == 'B':
                    self.nestGrid[self.teamB][x][y] = 1
                elif c == 'a':
                    self.ants.append(self.antA(x, y, self.teamA, self))
                    if hasattr(self.antA, 'set_pref_strght'):self.ants[-1].set_pref_strght(self.pref_strght[0])
                    if hasattr(self.antA, 'set_pref_direc'):self.ants[-1].set_pref_direc(self.pref_direc[0])
                    if hasattr(self.antA, 'set_pref_pher'):self.ants[-1].set_pref_pher(self.pref_pher[0])
                elif c == 'b':
                    self.ants.append(self.antB(x, y, self.teamB, self))
                    if hasattr(self.antB, 'set_pref_strght'):self.ants[-1].set_pref_strght(self.pref_strght[1])
                    if hasattr(self.antB, 'set_pref_direc'):self.ants[-1].set_pref_direc(self.pref_direc[1])
                    if hasattr(self.antB, 'set_pref_pher'):self.ants[-1].set_pref_pher(self.pref_pher[1])
                elif c == '#':
                    self.obstacleGrid[x][y] = 1
                elif c.isdigit():
                    self.foodGrid[x][y] = int(c)
                x += 1
            y += 1
            x = 0
        file.close()

    def updatePheromones(self):
        for i in range(self.gridWidth):
            for j in range(self.gridHeight):
                self.pheromoneGrid[self.teamA][i][j] *= self.pheromoneDecay
                self.pheromoneGrid[self.teamB][i][j] *= self.pheromoneDecay
                if (self.pheromoneGrid[self.teamA][i][j] < self.pheromoneThreshold):  
                    self.pheromoneGrid[self.teamA][i][j] = 0.0
                if (self.pheromoneGrid[self.teamB][i][j] < self.pheromoneThreshold):  
                    self.pheromoneGrid[self.teamB][i][j] = 0.0
    
    def updateFoodCounts(self):
        self.foodCount = [0, 0]
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                self.foodCount[self.teamA] += self.nestGrid[self.teamA][x][y] * self.foodGrid[x][y]
                self.foodCount[self.teamB] += self.nestGrid[self.teamB][x][y] * self.foodGrid[x][y]

    def updateLogFile(self):
        if not self.logfile:
            return
        
        pickle.dump(self.foodGrid, self.logfile)
        pickle.dump(self.obstacleGrid, self.logfile)
        pickle.dump(self.nestGrid, self.logfile)
        pickle.dump(self.pheromoneGrid, self.logfile)

        ants = [[],[]]
        for ant in self.ants:
            ants[ant.team].append((ant.x, ant.y, ant.hasFood))
        pickle.dump(ants, self.logfile)

        pickle.dump(self.foodCount, self.logfile)


    def tick(self):
         # Update ants
        for ant in self.ants:
            ant.energy = 1 # replenish energy
            ant.act()        
            
        # Update pheromones
        self.updatePheromones()

        # Update food counts
        self.updateFoodCounts()

        # Write current state to logfile
        self.updateLogFile()

    def shutdown(self):
        if self.logfile:
            self.logfile.close()