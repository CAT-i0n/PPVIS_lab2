from random import randint, choice
from math import ceil
class Object:
    def __init__(self):
        self.sign=""
    def __str__(self):
        return self.sign
    
class Animal(Object):
    def __init__(self):
        self.minEnergyForRepr = 30
        self.energyCostForRepr = 20
        self.energy = 20
        self.age = 0
        self.deathAge = 20
        self.stepDistance = 1
        self.goal = "Herbivore"
        self.energyFromFood = 5
    def step(self, Map, x, y):
        view = [list(map(lambda x: type(x).__name__, row)) for row in Map]
        size = len(Map)
        for row in range(len(view)):
            view[row] = view[row]*3
        view = view*3
        rounds = view[size + x - 1: size + x + 2]
        self.round  = [i[size + y - 1: size + y + 2] for i in rounds]
        view = view[size//2 + x: int(size*1.5) + x]
        self.view = [i[size//2 + y: int(size*1.5) + y] for i in view]
        
        distances = []
        for iter1, row in enumerate(self.view):
            for iter2, record in enumerate(row):
                if record == self.goal:
                    distances.append((iter1 - ceil(len(Map)/2), iter2 - ceil(len(Map)/2)))
        if distances:
            closest = sorted(distances, key = lambda c: ((c[0])**2 + (c[1])**2))[0]
            if abs(closest[0]) >= self.stepDistance:
                stepX = self.stepDistance * abs(closest[0]) // (closest[0])
            else: 
                stepX = closest[0]

            if abs(closest[1])>=self.stepDistance:
                stepY = self.stepDistance * abs(closest[1]) // (closest[1])
            else: 
                stepY = closest[1]
        else:
            stepX = randint(-self.stepDistance, self.stepDistance)
            stepY = randint(-self.stepDistance, self.stepDistance)
        
        if stepX + x >= len(Map):
            stepX -= len(Map)
        if stepX + x < 0:
            stepX += len(Map)
        if stepY + y >= len(Map):
            stepY -= len(Map)
        if stepY + y < 0:
            stepY += len(Map)

        possible = []
        if not isinstance(Map[stepX + x][stepY + y], (eval(self.goal), Ground)):
            for iter1, row in enumerate(self.round):
                for iter2, record in enumerate(row):
                    if iter1 != 1 and iter2 != 1:
                        if record == "Ground":
                            possible.append((iter1, iter2))     
            if possible:
                rand = choice(possible)
                stepX = rand[0] - 1
                stepY = rand[1] - 1
                if stepX + x >= len(Map):
                    stepX -= len(Map)
                if stepX + x < 0:
                    stepX += len(Map)
                if stepY + y >= len(Map):
                    stepY -= len(Map)
                if stepY + y < 0:
                    stepY += len(Map)
            else:
                stepX = 0
                stepY = 0
        return [stepX, stepY]
        


class Predator(Animal):
    def __init__(self):
        super().__init__()
        self.sign="\033[41m#\033[40m \033[0m"
        self.goal = "Herbivore"
        self.deathAge = 30
        self.stepDistance = 1 #2
        self.minEnergyForRepr = 35
        self.energyCostForRepr = 25
        

class Herbivore(Animal):
    def __init__(self):
        super().__init__()
        self.sign="\033[45m@\033[40m \033[0m"
        self.goal = "Plant"
        self.stepDistance = 1
        self.minEnergyForRepr = 25
        self.energyCostForRepr = 15
    
class Plant(Object):
    def __init__(self):
        self.sign="\033[42m$\033[40m \033[0m"
        
class Ground(Object):
    def __init__(self):
        self.sign="\033[40m. \033[0m"

