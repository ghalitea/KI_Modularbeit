from ant import Ant
import random

class BaselineAnt(Ant):
    def __init__(self, x, y, team, simulation):
        super().__init__(x, y, team, simulation)

    def act(self):
        pheremones = self.senseOwnPheromone()
        food = self.senseFood()
        pref_direc = 4
        pref_pher = 6

        # am eigenenen Nest
        if self.atOwnNest():
            if self.hasFood: self.dropFood()
            self.direction = self.directions[random.randint(1, 4)]
            self.move()

        # Handlungen, wenn kein Futter dabei
        elif not self.hasFood: 
            weights = [0, 1, 1, 1, 1]
            # Wenn essen gefunden, direkt hin laufen
            if not all(x == 0 for x in self.senseFood()) and ((self.x > 5 or self.y > 5) if self.team == 0 else (self.x < 26 or self.y < 26)):
                self.direction = self.directions[[i for i, x in enumerate(food) if x > 0][0]]
            else:
                # Richtung rechts unten bevorzugen (abhänging von Team)
                if ((self.x < 9 or self.y < 9) if self.team == 0 else (self.x > 22 or self.y > 22)): 
                    weights = [w + d for w,d in zip(weights, [0,0,1*pref_direc,0,1*pref_direc] if self.team == 0 else [0,1*pref_direc,0,1*pref_direc,0])]
                # Pfade mit Pheromonen bevorzugen
                if not all(x == 0 for x in pheremones) and ((self.x > 5 or self.y > 5) if self.team == 0 else (self.x < 26 or self.y < 26)): 
                    weights = [w + int(p*pref_pher*2) for w,p in zip(weights, pheremones)]
                # Gerade aus bevorzugen
                weights[self.directions.index(self.direction)] *= 24
                # Nicht die ganze Zeit gegen die äußere Wand rennen
                if (self.x == 1 and self.direction == (-1,0)) or (self.x == 30 and self.direction == (1,0)) or (self.y == 1 and self.direction == (0,-1)) or (self.y == 30 and self.direction == (0,1)):
                    self.direction = (self.direction[0]*(-1), self.direction[1]*(-1))
                else:
                    self.direction = random.choices(self.directions, weights, k=1)[0]
                
            self.move()

        # Handlungen wenn Futter dabei
        elif self.hasFood:
            weights = [0, 1, 1, 1, 1]
            # Richtung links oben bevorzugen (abhänging von Team)
            if ((self.x > 11 or self.y > 5) if self.team == 0 else (self.x < 20 or self.y < 25)): 
                weights = [w + d for w,d in zip(weights, [0,1*pref_direc,0,1*pref_direc,0] if self.team == 0 else [0,0,1*pref_direc,0,1*pref_direc])]
            # Sicher stellen, dass sie net in der Ecke stecken bleiben
            elif ((5 <= self.x <= 11 and self.y <= 5) if self.team == 0 else (25 >= self.x >= 20 and self.y >= 25)):
                weights = [w + d for w,d in zip(weights, [0,1*pref_direc,0,0,1*pref_direc] if self.team == 0 else [0,0,1*pref_direc,1*pref_direc,0])]
            # Pfade mit Pheromonen bevorzugen
            if not all(x == 0 for x in pheremones) and ((self.x > 5 or self.y > 5) if self.team == 0 else (self.x < 26 or self.y < 26)): 
                weights = [w + int(p*pref_pher) for w,p in zip(weights, pheremones)]
            self.direction = random.choices(self.directions, weights, k=1)[0]
            self.dropPheromone()
            self.move()
        self.takeFood()
        