from locale import normalize
from random import randint, choice
from math import ceil
from abc import ABC

class Object(ABC):    
    sign: str = ""
    def __str__(self) -> str:
        return self.sign
    
class Animal(Object, ABC):
    def __init__(self) -> None:
        #changeable vars for simulation
        self.minEnergyForRepr: int = 30
        self.energyCostForRepr: int = 20
        self.energy: int = 20
        self.age: int = 0
        self.deathAge: int = 20
        self.stepDistance: int = 1
        self.goal: str = "Herbivore"
        self.energyFromFood: int = 5 

    def __getSurround(self, Map, x, y) -> None:
        view = [list(map(lambda x: type(x).__name__, row)) for row in Map]
        size = self.mapSize
        for row in range(len(view)):
            view[row] = view[row]*3
        view = view*3
        rounds = view[size + x - 1: size + x + 2]
        self.round  = [i[size + y - 1: size + y + 2] for i in rounds]
        view = view[size//2 + x: int(size*1.5) + x]
        self.view = [i[size//2 + y: int(size*1.5) + y] for i in view]
    
    def __normalizeMove(self, x, y) -> None:
        if self.stepX + x >= self.mapSize:
            self.stepX -= self.mapSize
        if self.stepX + x < 0:
            self.stepX += self.mapSize
        if self.stepY + y >= self.mapSize:
            self.stepY -= self.mapSize
        if self.stepY + y < 0:
            self.stepY += self.mapSize

    def __editMove(self, Map, x, y) -> None:
        possible = []
        if not isinstance(Map[self.stepX + x][self.stepY + y], (eval(self.goal), Ground)):
            for iter1, row in enumerate(self.round):
                for iter2, record in enumerate(row):
                    if iter1 != 1 and iter2 != 1:
                        if record == "Ground":
                            possible.append((iter1, iter2))     
            if possible:
                rand = choice(possible)
                self.stepX = rand[0] - 1
                self.stepY = rand[1] - 1
                self.__normalizeMove(x, y)
            else:
                self.stepX = 0
                self.stepY = 0


    def step(self, Map, x, y) -> list:
        self.mapSize = len(Map)
        self.__getSurround(Map, x, y)
        distances = []
        for iter1, row in enumerate(self.view):
            for iter2, record in enumerate(row):
                if record == self.goal:
                    distances.append((iter1 - ceil(self.mapSize/2), iter2 - ceil(self.mapSize/2)))
        if distances:
            closest = sorted(distances, key = lambda c: ((c[0])**2 + (c[1])**2))[0]
            if abs(closest[0]) >= self.stepDistance:
                self.stepX = self.stepDistance * abs(closest[0]) // (closest[0])
            else: 
                self.stepX = closest[0]

            if abs(closest[1])>=self.stepDistance:
                self.stepY = self.stepDistance * abs(closest[1]) // (closest[1])
            else: 
                self.stepY = closest[1]
        else:
            self.stepX = randint(-self.stepDistance, self.stepDistance)
            self.stepY = randint(-self.stepDistance, self.stepDistance)
        
        self.__normalizeMove(x, y)

        self.__editMove(Map, x, y)
        
        return [self.stepX, self.stepY]
        


class Predator(Animal):
    def __init__(self):
        super().__init__()
        self.sign = "\033[41m#\033[40m \033[0m"
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

