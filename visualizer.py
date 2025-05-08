import pygame
import pickle

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)

LIGHT_BLUE = (128, 128, 255)
BLUE = (0, 0, 192)
DARK_BLUE = (0, 0, 128)

LIGHT_RED = (255, 128, 128)
RED = (192, 0, 0)
DARK_RED = (128, 0, 0)

GRAY = (128, 128, 128)

class Visualizer:
    def __init__(self, logfile, ticks, drawPheromones, speed, stopAt=-1):        
        self.speed = speed
        self.stopAt = stopAt
        
        self.drawPheromones = drawPheromones

        self.gridWidth = 32
        self.gridHeight = 32
        self.teamA = 0
        self.teamB = 1

        self.cellSize = 16
        self.screenWidth = self.gridWidth * self.cellSize
        self.screenHeight = self.gridHeight * self.cellSize 

        self.ticks = ticks
        self.currentTick = 0

        pygame.init()
        pygame.font.init() 
        self.font = pygame.font.SysFont('Arial', 16)
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Ant Simulation")
        self.clock = pygame.time.Clock()

        self.logfile = open(logfile, 'rb')

    def draw(self):
        if self.currentTick >= self.ticks:
            return

        # Load next frame from logfile
        foodGrid = pickle.load(self.logfile)
        obstacleGrid = pickle.load(self.logfile)
        nestGrid = pickle.load(self.logfile)
        pheromoneGrid = pickle.load(self.logfile)
        ants = pickle.load(self.logfile)
        foodCount = pickle.load(self.logfile)

        # Draw the environment
        self.screen.fill(WHITE)
        
        # Draw obstacles
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                if obstacleGrid[x][y] >= 1:  # Food
                    pygame.draw.rect(self.screen, GRAY, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))

        # Draw pheromones
        if self.drawPheromones in {self.teamA, self.teamB}:
            for x in range(self.gridWidth):
                for y in range(self.gridHeight):
                    pheromoneLevel = pheromoneGrid[self.drawPheromones][x][y]
                    if pheromoneLevel > 0:
                        intensity = int(pheromoneLevel * 255)
                        pygame.draw.rect(self.screen, (intensity, intensity, 0), (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))
        
         # Draw nest (bottom-left corner)
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                if nestGrid[self.teamA][x][y] > 0: 
                    pygame.draw.rect(self.screen, DARK_BLUE, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))
                if nestGrid[self.teamB][x][y] > 0: 
                    pygame.draw.rect(self.screen, DARK_RED, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))

        # Draw food
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                if foodGrid[x][y] >= 1:  # Food
                    pygame.draw.rect(self.screen, GREEN, (x * self.cellSize, y * self.cellSize, self.cellSize, self.cellSize))

        # Draw ants
        for team in [self.teamA, self.teamB]:
            for ant in ants[team]:
                color = None
                x, y, hasFood = ant
                if (team == self.teamA):
                    color = BLUE if hasFood else LIGHT_BLUE
                else:
                    color = RED if hasFood else LIGHT_RED
                pygame.draw.circle(self.screen, color, (x * self.cellSize + self.cellSize // 2, y * self.cellSize + self.cellSize // 2), self.cellSize // 2)
        
        text_surface = self.font.render('TICK: ' + str(self.currentTick) + ' | TEAM_A: ' + str(foodCount[self.teamA]) + ' | TEAM_B: ' + str(foodCount[self.teamB]), True, (0, 0, 0))
        self.screen.blit(text_surface, (self.gridWidth * self.cellSize // 4,0))

        pygame.display.flip()
        self.currentTick += 1

    def run(self):
        running = True
        update = True
        while running:
            if self.currentTick == self.stopAt:
                update = False

            self.clock.tick(self.speed)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        update = not update 
                    if event.key == pygame.K_PLUS:
                        self.draw()
                    
            # Draw everything
            if update:
                self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    visualizer = Visualizer("project02.rec", 10000, drawPheromones=0, speed=200, stopAt=-1)
    visualizer.run()
