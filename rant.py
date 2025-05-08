from ant import Ant
import random

class RandomAnt(Ant):
    def __init__(self, x, y, team, simulation):
        super().__init__(x, y, team, simulation)

    def act(self):
        if self.atOwnNest():
            if self.hasFood:
                self.dropFood()
            self.direction = self.getRandDirection()
            self.move()
        elif not all(x == 0 for x in self.senseFood()) and not self.hasFood: 
            food = self.senseFood()
            self.direction = self.directions[[i for i, x in enumerate(food) if x > 0][0]]
            self.move()
        else:
            self.direction = self.getRandDirection()
            self.move()
        self.takeFood()
    

    def getRandDirection(self):
        return self.directions[random.randint(1, 4)]