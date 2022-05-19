from random import randint
class Object:
    def __init__(self):
        self.sign=""
    def __str__(self):
        return self.sign
    
class Animal(Object):
    def __init__(self):
        self.energy = 20
        self.age = 0
        self.deathAge = 40


class Predator(Animal):
    def __init__(self):
        super().__init__()
        self.sign="\033[41m#\033[40m \033[0m"
    def step(self, Map):
        return [randint(-1,1), randint(-1,1)]

class Herbivore(Animal):
    def __init__(self):
        super().__init__()
        self.sign="\033[45m@\033[40m \033[0m"
    def step(self, Map):
        return [randint(-1,1), randint(-1,1)]
    
class Plant(Object):
    def __init__(self):
        self.sign="\033[42m$\033[40m \033[0m"
        
class Ground(Object):
    def __init__(self):
        self.sign="\033[40m. \033[0m"
        