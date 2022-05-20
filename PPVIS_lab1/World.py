from Model import Model
import click
import os
from time import sleep
os.system("color")


dataPath = "world.json"


@click.group()
def start():
    pass


@start.command('generate')
def generate():
    """Generate new world"""
    world.generate()
    close()


@start.command("make_step")
def makeStep():
    world.makeStep()
    close()

@start.command("make_several_steps")
@click.option('-n', '--number', default=-1, help = "Num > 0")
def makeSeveralSteps(number):
    print("\033[H\033[J ")
    for _ in range(number):
        print(world)
        sleep(0.5)
        world.makeStep()
        print("\033[H\033[J ")
        
        
    close()

@start.command("add_object")
@click.option('-o', '--object', default="Ground", help = "Plant, Ground, Herbivore or Predator")
@click.option('-x', '--xcoord', default=0, help = "from 0 to 14")
@click.option('-y', '--ycoord', default=0, help = "from 0 to 14")
def addObject(object, xcoord, ycoord):
    world.addObject(object, xcoord, ycoord)
    close()

@start.command("show")
def show():
    close()


def close():
    print(world)
    world.save(dataPath)


if __name__ == "__main__":
    world = Model()
    #world.generate()
    #world.save(dataPath)
    world.load(dataPath)
    start()
    