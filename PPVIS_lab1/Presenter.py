from View import View
from Model import Model
class Presenter:
    def __init__(self, size = 15):
        self.dataPath = "world.json"
        self.view = View(self)
        self.model = Model(size = size)
        self.model.load(self.dataPath)
        self.view.run()
    

    def step(self):
        self.model.makeStep()

    def getMap(self):
        return self.model.getMap()
    
    def generate(self):
        self.model.generate()

    def save(self):
        self.model.save(self.dataPath)
    

