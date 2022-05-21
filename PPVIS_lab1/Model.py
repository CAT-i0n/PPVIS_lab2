from Objects import Plant, Ground, Herbivore, Predator
from random import random, randint
from functools import reduce
import json

class Model:
    def __init__(self, size = 20):
        #changeable vars for generation
        self.size = size
        self.probabilityOfEntities = [0.90, 0.045, 0.045, 0.01]
        self.entities = [Ground, Plant, Herbivore, Predator]
    
    def generate(self):
        self.Map = []
        for _ in range(self.size):
            row = []
            for _ in range(self.size):
                randProb = random() #from 0 to 1
                for num, prob in enumerate(self.probabilityOfEntities):
                    if reduce(lambda x,y:x+y, self.probabilityOfEntities[:num + 1]) > randProb:
                        row.append(self.entities[num]())
                        break
            self.Map.append(row)

    def save(self, dataPath):
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
        with open("world.json", "w") as file:
            json.dump(saveList, file)

    def load(self, dataPath):
        with open(dataPath) as file:
            data = json.load(file)
        for iter1, row in enumerate(data):
            for iter2, record in enumerate(row):
                entity = eval(record["name"])()
                if isinstance(entity, (Predator, Herbivore)):
                    entity.age = int(record["age"])
                    entity.energy = int(record["energy"])
                data[iter1][iter2] = entity
        self.Map = data


    def makeStep(self):
        madeStep = []
        for iter1, row in enumerate(self.Map):
            for iter2, entity in enumerate(row):
                if isinstance(entity, (Predator, Herbivore)) and entity not in madeStep:
                    move = entity.step(self.Map, iter1, iter2)
                    move = [move[0] + iter1, move[1] + iter2] 
                    if isinstance(entity, Predator) and isinstance(self.Map[move[0]][move[1]], Herbivore):
                        entity.energy += entity.energyFromFood
                        self.Map[move[0]][move[1]] = entity
                        self.Map[iter1][iter2] = Ground()
                    elif isinstance(entity, Herbivore) and isinstance(self.Map[move[0]][move[1]], Plant):
                        entity.energy += entity.energyFromFood
                        self.Map[move[0]][move[1]] = entity
                        self.Map[iter1][iter2] = Ground() 
                    else:
                        if isinstance(self.Map[move[0]][move[1]], Ground):
                            self.Map[iter1][iter2], self.Map[move[0]][move[1]] = self.Map[move[0]][move[1]], entity
                    entity.energy -= 1
                    entity.age += 1
                    madeStep.append(entity)
                if isinstance(entity, Ground):
                    if randint(0, 30) == 0:
                        self.Map[iter1][iter2] = Plant() 
        for iter1, row in enumerate(self.Map):
            for iter2, entity in enumerate(row):
                if isinstance(entity, (Predator, Herbivore)):
                    if entity.energy >= entity.minEnergyForRepr:
                        x, y = iter1, iter2
                        for reprX, reprY in (x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y-1),(x-1,y+1),(x+1,y-1):
                            if reprX >= self.size:
                                reprX -= self.size
                            if reprX < 0:
                                reprX += self.size
                            if reprY >= self.size:
                                reprY -= self.size
                            if reprY < 0:
                                reprY += self.size
                            if isinstance(self.Map[reprX][reprY], Ground):
                                self.Map[reprX][reprY] = type(entity)()
                                self.Map[iter1][iter2].energy -= entity.energyCostForRepr
                                break
                    if entity.age >= entity.deathAge or entity.energy<=0:
                        self.Map[iter1][iter2] = Ground()


    def addObject(self, object, x, y):
        entity = eval(object)()
        self.Map[x][y] = entity
    
    def __str__(self):
        rez = ""
        for row in self.Map:
            for entity in row:
                rez+=entity.sign
            rez+="\n"
        return rez

    def getMap(self):
        return [list(map(lambda x: type(x).__name__, row)) for row in self.Map]
