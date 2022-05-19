from View import View
from Model import Model
class World: #presenter
    def __init__(self):
        self.view = View(self)
        self.model = Model()

    def makeStep(self):
        self.model.makeStep()

