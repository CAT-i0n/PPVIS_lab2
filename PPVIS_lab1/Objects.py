from random import randint
from copy import deepcopy
class Object:
    def __init__(self):
        self.sign=""
    def __str__(self):
        return self.sign
    
class Animal(Object):
    def __init__(self):
        self.isRepr = False # reproduction
        self.energyForRepr = 30
        self.energy = 20
        self.age = 0
        self.deathAge = 20
        self.stepDistance = 1
        self.goal = "Herbivore"
    def step(self, Map, x, y):
        print(self.goal)
        view = [list(map(lambda x: type(x).__name__, row)) for row in Map]
        size = len(Map)
        for row in range(len(view)):
            view[row] = view[row]*3
        view = view*3
        round = view[size + x - 1: size + x + 2]
        self.round  = [i[size + y - 1: size + y + 2] for i in round]
        view = view[size//2 + x: int(size*1.5) + x]
        self.view = [i[size//2 + y: int(size*1.5) + y] for i in view]
        distances = []
        for iter1, row in enumerate(self.view):
            for iter2, record in enumerate(row):
                if record == self.goal:
                    distances.append((iter1 - len(Map)//2 - 1, iter2 - len(Map)//2 - 1))
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
        print([stepX, stepY])
        return [stepX, stepY]
        


class Predator(Animal):
    def __init__(self):
        super().__init__()
        self.sign="\033[41m#\033[40m \033[0m"
        self.stepDistance = 2
        

class Herbivore(Animal):
    def __init__(self):
        super().__init__()
        self.sign="\033[45m@\033[40m \033[0m"
        self.goal = "Plant"
    #def step(self, Map, x, y):
     #   super().step(Map, x, y)
      #  return [randint(-1,1), randint(-1,1)]
    
class Plant(Object):
    def __init__(self):
        self.sign="\033[42m$\033[40m \033[0m"
        
class Ground(Object):
    def __init__(self):
        self.sign="\033[40m. \033[0m"
        