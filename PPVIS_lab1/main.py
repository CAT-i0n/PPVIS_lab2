import click
import os
from Presenter import Presenter

@click.group()
def run():
    pass

@run.command("gui")
def gui() -> None:
    datapath = "world.json"
    p = Presenter(datapath = datapath)
    p.run()

@run.command("cli")
def cli() -> None:
    print(">>>", end=" ")
    command: str = input()
    os.system("python CLI.py " + command)

if __name__ == "__main__":
    run()