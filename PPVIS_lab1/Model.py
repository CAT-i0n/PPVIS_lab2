from Objects import Plant, Ground, Herbivore, Predator
from random import random
from functools import reduce
import json
class Model:
    def __init__(self):
        #changeable vars for generation
        self.size = 15
        self.probabilityOfEntities = [0.91, 0.03, 0.03, 0.03]
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
                if isinstance(entity, (Predator, Herbivore)):
                    if entity not in madeStep:
                        move = entity.step()
                        move = [move[0] + iter1, move[1] + iter2] 
                        if move[0] >= self.size:
                            move[0] -= self.size
                        if move[0] < 0:
                            move[0] += self.size
                        if move[1] >= self.size:
                            move[1] -= self.size
                        if move[1] < 0:
                            move[1] += self.size
                        self.Map[iter1][iter2], self.Map[move[0]][move[1]] = self.Map[move[0]][move[1]], entity
                        entity.energy -= 1
                        madeStep.append(entity)



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

