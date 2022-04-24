class Object:
    def __init__(self):
        self.sign=""
    def __str__(self):
        return self.sign
    
class Animal(Object):
    pass

class Predator(Animal):
    def __init__(self):
        self.sign="\033[41m#\033[47m \033[0m"

class Herbivore(Animal):
    def __init__(self):
        self.sign="\033[45m@\033[47m \033[0m"
    
class Plant(Object):
    def __init__(self):
        self.sign="\033[42m$\033[47m \033[0m"
        
class Ground(Object):
    def __init__(self):
        self.sign="\033[47m. \033[0m"
        