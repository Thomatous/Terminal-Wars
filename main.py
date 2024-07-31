import os
from termcolor import colored
from src.world.world import World
from src.simulator import Simulator
from src.player.base_player import BasePlayer

if __name__ == "__main__":
    world = World(20, 20)

    while world.generating:
        world.wave_function_collapse()
        print(world)
        os.system('cls' if os.name == 'nt' else 'clear')

    print(world)
    print("Generated world!")

    simulator = Simulator(world,
                          [BasePlayer(health=10, sprite=colored("AA", "red")),
                           BasePlayer(health=13, sprite=colored("GG", "cyan")),
                           BasePlayer(health=15, sprite=colored("CC", "magenta"))])
    simulator.simulate()

