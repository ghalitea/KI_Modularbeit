from ant import Ant
import random

class BaselineAnt(Ant):
    def __init__(self, x, y, team, simulation):
        super().__init__(x, y, team, simulation)

    def act(self):
        pheremones = self.senseOwnPheromone()
        food = self.senseFood()
        pref_direc = 2
        pref_pher = 3

        # am eigenenen Nest
        if self.atOwnNest():
            if self.hasFood: self.dropFood()
            self.direction = self.directions[random.randint(1, 4)]
            self.move()

        # Handlungen, wenn kein Futter dabei
        elif not self.hasFood: 
            weights = [0, 1, 1, 1, 1]
            # Wenn essen gefunden, direkt hin laufen
            if not all(x == 0 for x in self.senseFood()) and ((self.x > 6 or self.y > 6) if self.team == 0 else (self.x < 27 or self.y < 27)):
                self.direction = self.directions[[i for i, x in enumerate(food) if x > 0][0]]
            else:
                # Richtung rechts unten bevorzugen (abhänging von Team)
                if ((self.x < 23 and self.y < 23) if self.team == 0 else (self.x > 10 and self.y > 10)): 
                    weights = [w + d for w,d in zip(weights, [0,0,1*pref_direc,0,1*pref_direc] if self.team == 0 else [0,1*pref_direc,0,1*pref_direc,0])]
                # Pfade mit Pheromonen bevorzugen
                if not all(x == 0 for x in pheremones) and ((self.x > 6 or self.y > 6) if self.team == 0 else (self.x < 27 or self.y < 27)): 
                    weights = [w + int(p*pref_pher) for w,p in zip(weights, pheremones)]
                self.direction = random.choices(self.directions, weights, k=1)[0]
            self.move()

        # Handlungen wenn Futter dabei
        elif self.hasFood:
            weights = [0, 1, 1, 1, 1]
            # Richtung links oben bevorzugen (abhänging von Team)
            if ((self.x > 12 or self.y > 8) if self.team == 0 else (self.x < 21 or self.y < 25)): 
                weights = [w + d for w,d in zip(weights, [0,1*pref_direc,0,1*pref_direc,0] if self.team == 0 else [0,0,1*pref_direc,0,1*pref_direc])]
            # Sicher stellen, dass sie net in der Ecke stecken bleiben
            elif (8 <= self.x <= 12 and self.y <= 8):
                weights = [w + d for w,d in zip(weights, [0,1*pref_direc,0,0,1*pref_direc] if self.team == 0 else [0,0,1*pref_direc,1*pref_direc,0])]
            # Pfade mit Pheromonen bevorzugen
            if not all(x == 0 for x in pheremones) and ((self.x > 6 or self.y > 6) if self.team == 0 else (self.x < 27 or self.y < 27)): 
                weights = [w + int(p*pref_pher) for w,p in zip(weights, pheremones)]
            self.direction = random.choices(self.directions, weights, k=1)[0]
            self.dropPheromone()
            self.move()
        self.takeFood()
        