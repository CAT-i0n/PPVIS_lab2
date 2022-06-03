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
    def save(self):
        pass

    @abstractmethod 
    def run():
        pass


class Presenter(IPresenter):
    def __init__(self, datapath: str, size: int = 15) -> None:
        self.dataPath = datapath
        self._view: View = View(self)
        
        self._model: Model = Model(size = size)
        try:
            self._model.load(self.dataPath)
        except FileNotFoundError:
            print("Wrong datapath")
            raise SystemExit
    
    def addObject(self, *args) -> None:
        self._model.addObject(*args)
        self._view.Map = self.__getMap()

    def step(self) -> None:
        self._model.makeStep()
        self._view.Map = self.__getMap()

    def __getMap(self) -> list:
        return self._model.getMap()
    
    def generate(self)  -> None:
        self._model.generate()
        self._view.Map = self.__getMap()

    def save(self):
        self._model.save(self.dataPath)

    def run(self):
        self._view.Map = self.__getMap()
        self._view.run()
        
    

if __name__ == "__main__":
    datapath = "world.json"
    p = Presenter(datapath = datapath)
    p.run()