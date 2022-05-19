from Objects import Plant, Ground, Herbivore, Predator
from random import choice
class Model:
    def __init__(self):
        #changeable vars
        self.size = 10
        self.prob_of_entities = [0,5, 0.2, 0.2, 0.1]
        self.entities = [Ground, Plant, Herbivore, Predator]
        #world generation
        self.world = [[_ for i in range(self.size)] for _ in range(self.size)]
    def makeStep(self):
        pass