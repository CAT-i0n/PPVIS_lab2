import click
import os
from Presenter import Presenter

@click.group()
def run():
    pass

@run.command("gui")
def gui():
    p = Presenter()

@run.command("cli")
def cli():
    print(">>>", end=" ")
    command = input()
    os.system("python CLI.py " + command)

if __name__ == "__main__":
    run()