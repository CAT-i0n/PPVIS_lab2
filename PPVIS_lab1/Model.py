from Objects import Plant, Ground, Herbivore, Predator
from random import random, randint
from functools import reduce
import json

class Model:
    def __init__(self, size: int = 15) -> None:
        #changeable vars for generation
        self._size: int = size
        self._probabilityOfEntities: tuple = (0.90, 0.045, 0.045, 0.01)
        self._entities: tuple = (Ground, Plant, Herbivore, Predator)
    
    def generate(self) -> None:
        self.Map = []
        for _ in range(self._size):
            row = []
            for _ in range(self._size):
                randProb = random() #from 0 to 1
                for num, prob in enumerate(self._probabilityOfEntities):
                    if reduce(lambda x,y:x+y, self._probabilityOfEntities[:num + 1]) > randProb:
                        row.append(self._entities[num]())
                        break
            self.Map.append(row)

    def save(self, dataPath: str) -> None:
        saveList = []
        for row in self.Map:
            saveRow = []
            for entity in row:
                if isinstance(entity, (Predator, Herbivore)):
                    saveRow.append({"name" : type(entity).__name__,
                                    "energy" : entity.energy,
                                    "age" : entity.age})
                else: 
                    saveRow.append({"name" : type(entity).__name__})
            saveList.append(saveRow)
        with open(dataPath, "w") as file:
            json.dump(saveList, file)

    def load(self, dataPath: str) -> None:
        with open(dataPath) as file:
            data = json.load(file)
        for rowIter, row in enumerate(data):
            for columnIter, record in enumerate(row):
                entity = eval(record["name"])()
                if isinstance(entity, (Predator, Herbivore)):
                    entity.age = int(record["age"])
                    entity.energy = int(record["energy"])
                data[rowIter][columnIter] = entity
        self.Map = data


    def makeStep(self) -> None:
        madeStep = []
        for rowIter, row in enumerate(self.Map):
            for columnIter, entity in enumerate(row):
                if isinstance(entity, (Predator, Herbivore)) and entity not in madeStep:
                    move = entity.step(self.Map, rowIter, columnIter)
                    move = [move[0] + rowIter, move[1] + columnIter] 
                    if isinstance(self.Map[move[0]][move[1]], eval(entity.goal)):
                        entity.energy += entity.energyFromFood
                        self.Map[move[0]][move[1]] = entity
                        self.Map[rowIter][columnIter] = Ground()
                    else:
                        if isinstance(self.Map[move[0]][move[1]], Ground):
                            self.Map[rowIter][columnIter] = self.Map[move[0]][move[1]]
                            self.Map[move[0]][move[1]] = entity
                    entity.energy -= 1
                    entity.age += 1
                    madeStep.append(entity)
                if isinstance(entity, Ground):
                    if randint(0, 30) == 0:
                        self.Map[rowIter][columnIter] = Plant() 
        self.__deathAndBirth()


    def __deathAndBirth(self) -> None:
        for rowIter, row in enumerate(self.Map):
            for columnIter, entity in enumerate(row):
                if isinstance(entity, (Predator, Herbivore)):
                    if entity.energy >= entity.minEnergyForRepr:
                        x, y = rowIter, columnIter
                        for reprX, reprY in (x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y-1),(x-1,y+1),(x+1,y-1):
                            if reprX >= self._size:
                                reprX -= self._size
                            if reprX < 0:
                                reprX += self._size
                            if reprY >= self._size:
                                reprY -= self._size
                            if reprY < 0:
                                reprY += self._size
                            if isinstance(self.Map[reprX][reprY], Ground):
                                self.Map[reprX][reprY] = type(entity)()
                                self.Map[rowIter][columnIter].energy -= entity.energyCostForRepr
                                break
                    if entity.age >= entity.deathAge or entity.energy<=0:
                        self.Map[rowIter][columnIter] = Ground()


    def addObject(self, object: str, x: int, y: int)-> None:
        entity = eval(object)()
        self.Map[x][y] = entity
    
    def __str__(self):
        rez = ""
        for row in self.Map:
            for entity in row:
                rez+=entity.sign
            rez+="\n"
        return rez

    def getMap(self)-> list:
        return [list(map(lambda x: type(x).__name__, row)) for row in self.Map]
