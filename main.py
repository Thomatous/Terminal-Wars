import os
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

    simulator = Simulator(world, [BasePlayer(), BasePlayer(), BasePlayer()])
    simulator.simulate()

