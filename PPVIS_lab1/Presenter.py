from View import View
from Model.Model import Model
from abc import abstractmethod

class IPresenter:

    @abstractmethod
    def addObject(self, *args):
        pass

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def getMap(self):
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def save(self):
        pass


class Presenter(IPresenter):
    def __init__(self, size: int = 15, datapath: str = "world.json") -> None:
        self.dataPath = datapath
        self._view: View = View(self)
        self._model: Model = Model(size = size)
        try:
            self._model.load(self.dataPath)
        except FileNotFoundError:
            print("Wrong datapath")
            raise SystemExit
        self._view.run()
    
    def addObject(self, *args) -> None:
        self._model.addObject(*args)

    def step(self) -> None:
        self._model.makeStep()

    def getMap(self) -> list:
        return self._model.getMap()
    
    def generate(self)  -> None:
        self._model.generate()

    def save(self):
        self._model.save(self.dataPath)
    

if __name__ == "__main__":
    p = Presenter()